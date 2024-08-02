from app import db
from flask_login import UserMixin

#database model

#association table
association_table = db.Table('association_table',
    db.Column('record_id',db.Integer, db.ForeignKey('record.id')),
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'))
)

#record db
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    genre = db.Column(db.String(100), nullable = False)
    album_name = db.Column(db.String, nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    owner = db.relationship('User', secondary=association_table, backref='records')

    #initialise db columns
    def __init__(self, name,genre,album_name,release_date):
        self.name = name
        self.genre = genre
        self.album_name = album_name
        self.release_date = release_date

#users database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(10))

    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

