from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    latest_energy_calculation = db.Column(db.JSON, nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_type = db.Column(db.String(50), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=True)
    product_installed = db.Column(db.String(100), nullable=True)
    additional_info = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(200), nullable=False)
    booking_number = db.Column(db.String(20), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Booking {self.booking_number}>'

# Import other models so they are available via app.models
from .energy_data import EnergyReading, DashboardMetrics, ConsumptionBreakdown, EVChargingStatus
