from extensions import db
from flask_login import UserMixin
from datetime import datetime, date, time

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))

    bookings = db.relationship('Booking', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    events = db.relationship('Event', backref='creator', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    location = db.Column(db.String(150), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_amount = db.Column(db.Integer, nullable=False)
    
    status = db.Column(db.String(20), nullable=False)
    artist_info = db.Column(db.Text)
    image = db.Column(db.String(255))
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='event', lazy=True)
    bookings = db.relationship('Booking', backref='event', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), nullable=False, unique=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.utcnow)



