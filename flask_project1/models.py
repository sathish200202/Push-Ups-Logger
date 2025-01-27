from . import db
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta #for postedAt
# import pytz

# IST = pytz.timezone('Asia/kolkata') #for indian time format

#model for Users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #creating id for every users.. so we use primary key
    name = db.Column(db.String(100)) #the name will be string
    email = db.Column(db.String(100), unique=True) #email also a string, but it'll be a unique
    password = db.Column(db.String(100)) #password also a string, but ne need hash the password
    Workout = db.relationship('Workout', backref='author', lazy=True) #make a relationship between user and the workout

#models for Workouts
class Workout(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    id = db.Column(db.Integer, primary_key = True)
    pushups = db.Column(db.Integer, nullable = False)
    # posted_At = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    posted_At = db.Column(db.DateTime, nullable = False, default=datetime.now(timezone.utc))
    comment = db.Column(db.String(200))