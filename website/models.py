from . import db #importing the db = SQLALCHEMY
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10001))
    date = db.Column(db.DateTime(timezone=True), default=func.now) #getting the current date and time and making it as the value
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #it depends on what the user is represented, in this case id, it can be email, phone number, etc
    #one user can have many notes
    #so everytime we look at the user_id we will know who has created the note

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True) #maximum length 150 characters, unique means no duplicate emails
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note') #making a relationship uses capital Note, while referencing foreign key doesn't, e.g user.id
    
