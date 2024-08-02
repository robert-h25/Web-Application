from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
import logging

#initialise flask and db
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#implement migration
migrate = Migrate(app, db, render_as_batch=True)

admin = Admin(app,template_mode='bootstrap4')

#logging config
logging.basicConfig(filename='record.log',level=logging.DEBUG,
                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from app import views, models