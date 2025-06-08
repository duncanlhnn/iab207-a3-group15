from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os, uuid

from extensions import db
from models import User, Event, Comment, Booking
from forms import RegisterForm, LoginForm, EventForm, CommentForm, BookingForm

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    search_query = request.args.get('search')
    category = request.args.get('category')
    events = Event.query.filter_by(status='open')

    if search_query:
        events = events.filter(Event.title.ilike(f'%{search_query}%'))
    if category:
        events = events.filter(Event.artist_info.ilike(f'%{category}%'))

    events = events.order_by(Event.date.asc()).all()
    return render_template('index.html', events=events)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            password=form.password.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('routes.index'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html', form=form)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('routes.index'))

@routes.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            image = form.image.data
            filename = secure_filename(f"{uuid.uuid4().hex}_{image.filename}")
            image_folder = os.path.join('static', 'images')
            os.makedirs(image_folder, exist_ok=True)
            image.save(os.path.join(image_folder, filename))

        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data.strftime('%Y-%m-%d'),
            start_time=form.start_time.data.strftime('%H:%M'),
            end_time=form.end_time.data.strftime('%H:%M'),
            location=form.location.data,
            ticket_price=form.ticket_price.data,
            ticket_amount=form.ticket_amount.data,
            status=form.status.data,
            artist_info=form.artist_info.data,
            image=f'images/{filename}' if filename else None,
            user_id=current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('routes.index'))
    return render_template('create.html', form=form)

@routes.route('/edit/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)

    form = EventForm(
        title=event.title,
        description=event.description,
        date=event.date,
        start_time=event.start_time,
        end_time=event.end_time,
        location=event.location,
        ticket_price=event.ticket_price,
        ticket_amount=event.ticket_amount,
        status=event.status,
        artist_info=event.artist_info
    )

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.location = form.location.data
        event.ticket_price = form.ticket_price.data
        event.ticket_amount = form.ticket_amount.data
        event.status = form.status.data
        event.artist_info = form.artist_info.data

        if form.image.data:
            image = form.image.data
            filename = secure_filename(f"{uuid.uuid4().hex}_{image.filename}")
            image_folder = os.path.join('static', 'images')
            os.makedirs(image_folder, exist_ok=True)
            image.save(os.path.join(image_folder, filename))
            event.image = f'images/{filename}'

        db.session.commit()
        flash('Event updated.')
        return redirect(url_for('routes.event_detail', event_id=event.id))

    return render_template('create.html', form=form, event=event)

@routes.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    form = CommentForm()
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted.desc()).all()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            event_id=event_id,
            date_posted=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted.')
        return redirect(url_for('routes.event_detail', event_id=event_id))

    return render_template('event.html', event=event, comments=comments, form=form)

@routes.route('/book/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity <= 0 or quantity > event.ticket_amount:
            flash('Invalid ticket quantity.')
        else:
            order_id = f"ORD{uuid.uuid4().hex[:6].upper()}"
            booking = Booking(
                order_id=order_id,
                user_id=current_user.id,
                event_id=event_id,
                quantity=quantity,
                booking_time=datetime.utcnow()
            )
            event.ticket_amount -= quantity
            db.session.add(booking)
            db.session.commit()
            flash(f'Booking confirmed! Your Order ID is {order_id}.')
            return redirect(url_for('routes.bookings'))

    return render_template('book.html', event=event, form=form)

@routes.route('/bookings')
@login_required
def bookings():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('booking.html', bookings=user_bookings)

@routes.route('/cancel/<int:event_id>')
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    event.status = 'cancelled'
    db.session.commit()
    flash('Event cancelled.')
    return redirect(url_for('routes.event_detail', event_id=event.id))

@routes.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@routes.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@routes.route('/about')
def about():
    return render_template('about.html')
