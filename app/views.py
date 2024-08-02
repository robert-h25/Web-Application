from flask import redirect, render_template, flash, request, url_for, session
from app import app,db,admin
from flask_admin.contrib.sqla import ModelView
from app.forms import AddRecord ,LoginForm, ChangePassword
from app.models import Record, User
import json

admin.add_view(ModelView(Record, db.session))
admin.add_view(ModelView(User, db.session))

#initialising flask-login
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user,current_user
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
#todo: add error log when wrong data is submitted
#homepage
@app.route('/', methods=['GET','POST'])
def home():

    home = {'description':'The home of records.'}

    return render_template('home.html', title='BasePage',home=home)

#add record
@app.route('/addrecord', methods=['GET', 'POST'])
#check if logged in
@login_required
def addRecord():
    form = AddRecord()
    
    #add to user records and log
    if form.validate_on_submit():
        record = Record(name = form.ArtistName.data, genre = form.Genres.data, album_name=form.AlbumName.data, release_date=form.ReleaseDate.data)
        #link to user id in the association table
        userid = session["id"]
        user = db.session.query(User).filter_by(id = userid).first() 
        record.owner.append(user)
        db.session.add(record)
        db.session.commit()
        app.logger.info("%s by %s has been added to the database",record.name,record.album_name)
        flash("Music added successfully")
        

    return render_template('addrecord.html',title= 'Add Record', form=form)

#adding a user
@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = LoginForm()
   
    if form.validate_on_submit():
        #check if user is in the db and log
        exists = db.session.query(User.id).filter_by(username =form.Username.data).first() is not None
        if ( exists == True):
            app.logger.warning("%s is already a user",form.Username.data)
            flash("User has been added before. Please enter a new Username.")
            return render_template('adduser.html',title= 'Add User',form=form)
        #if not add to db and log
        user = User(username=form.Username.data, password=form.Password.data)
        app.logger.info('%s has been added to the database', form.Username.data)
        db.session.add(user)
        db.session.commit()

        flash("Added user successfully")

    return render_template('adduser.html',title= 'Add User',form=form)

#user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        #check if user and password is correct and log
        user = User.query.filter_by(username = form.Username.data).first()
        if (user.password == form.Password.data):
            login_user(user)           
            app.logger.info('%s logged in',form.Username.data)
            #id = db.session.query(User).filter(User.username == form.Username.data).first()
            id = current_user.get_id()
            print(id)
            #create json serialisable

            session['id'] = id
            flash("Login Successful")
            return render_template('login.html',title= 'Login',form=form)
        else:
            app.logger.error("Invalid login detected")
            flash("Incorrect Password or Username, try again")
    return render_template('login.html',title= 'login',form=form)

#user logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    #log logout
    logout_user()
    #delete session id
    session.pop('id',None)
    flash("Successfully logged out")
    return redirect(url_for('home'))

#change user password
@app.route('/changepassword', methods=['GET','POST'])
def password():
    form = ChangePassword()
    if form.validate_on_submit():
        #check username and old password are correct
        #update password and log
        user = User.query.filter_by(username = form.Username.data).first()
        if (user.password == form.OldPassword.data):
            user.password = form.NewPassword.data
            app.logger.info('%s has changed password', user.username)
            db.session.add(user)
            db.session.commit()
            flash("Password changed successfully!")
            return render_template('changepassword.html',title= 'Change Password',form=form)
        else:
            app.logger.error("Invalid change of a user's password")
            flash("Incorrect Password or Username, try again")
    return render_template('changepassword.html',title= 'Change Password',form=form)

    
#view records
@app.route('/viewrecord', methods=['GET', 'POST'])
@login_required
def viewRecord():
    #view records by user id
    userid = session['id']
    #query by user id   
    user = User.query.filter_by(id = userid).first()
    records = Record.query.order_by(Record.id).all()
    return render_template('viewrecord.html',title= 'View Records', records=user.records)





