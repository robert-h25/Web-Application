import os
import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app,db,models

class test(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #testing methods
    def login(self,username,password):
        return self.app.post('/login', data=dict (username=username, password=password), follow_redirects = True)

    def password(self, username, old_password, new_password):
        return self.app.post('/changepassword', data=dict (username=username, oldpassword=old_password, newpassword=new_password), follow_redirects = True)
    
    def record(self,artist,album,genre,release_date):
        return self.app.post('/addrecord', data=dict (artistname=artist, albumname=album, genre=genre, releasedate = release_date), follow_redirects = True)
    #add tests

    #test database queries

    #test form validation and boundary cases

    #test form submission
    def test_valid_user_login(self):
        response = self.login('test','w')
        self.assertEqual(response.status_code,200)

    def test_valid_password_change(self):
        response = self.password('test','w', '123')
        self.assertEqual(response.status_code,200)

    def test_addrecord(self):
        response = self.record('artist','album', 'genre','releasedate')
        self.assertEqual(response.status_code,200)
    #test pages load
    def test_mainpage(self):
        response = self.app.get('/', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_addrecordpage(self):
        response = self.app.get('/addrecord', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_changepasswordpage(self):
        response = self.app.get('/changepassword', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_loginpage(self):
        response = self.app.get('/login', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_logoutpage(self):
        response = self.app.get('/logout', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

    def test_viewrecordpage(self):
        response = self.app.get('/viewrecord', follow_redirects = True)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
    