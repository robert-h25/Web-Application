from flask_wtf import FlaskForm
from wtforms import DateField, StringField, HiddenField
from wtforms.validators import DataRequired

#form to get data from the user

class AddRecord(FlaskForm):
    id_field = HiddenField()
    ReleaseDate = DateField('ReleaseDate', validators=[DataRequired()])
    ArtistName = StringField('ArtistName', validators=[DataRequired()])
    Genres = StringField('Genres', validators=[DataRequired()])
    AlbumName = StringField('AlbumName', validators=[DataRequired()])
    

class LoginForm(FlaskForm):
    id_field = HiddenField()
    Username = StringField('Username', validators=[DataRequired()])
    Password = StringField('Password', validators=[DataRequired()])

class ChangePassword(FlaskForm):
    id_field = HiddenField()
    Username = StringField('Username', validators=[DataRequired()])
    OldPassword = StringField('Old Password', validators=[DataRequired()])  
    NewPassword = StringField('New Password', validators=[DataRequired()])  