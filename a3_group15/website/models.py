from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    address = db.Column(db.String(100))

    bookings = db.relationship('Booking', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return "<User: {} {}, id: {}>".format(self.first_name, self.surname, self.id)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, default=0)
    status = db.Column(
        db.Enum('OPEN', 'SOLD_OUT', 'INACTIVE', 'CANCELLED'),
        default='OPEN'
    )
    category = db.Column(db.String(50))
    image = db.Column(db.String(400), default='default.jpg')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    bookings = db.relationship('Booking', backref='event')
    comments = db.relationship('Comment', backref='event')

    @property
    def tickets_left(self):
        return self.capacity - self.tickets_sold

    def __repr__(self):
        return "<Event: {}, id: {}>".format(self.title, self.id)
    



class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(400), nullable=False)
    posted_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment id: {}, body: {}...>".format(self.id, self.body[:10])


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Booking id: {}, qty: {}>".format(self.id, self.qty)


