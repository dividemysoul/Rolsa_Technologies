from app import app, db
from app.models import User, Booking
from datetime import date
import uuid

def verify():
    with app.app_context():
        # Clean up
        Booking.query.delete()
        User.query.filter_by(email='test@example.com').delete()
        db.session.commit()

        # Create User
        u = User(email='test@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        print(f"User created: {u.id}")

        # Create Booking
        booking_number = str(uuid.uuid4().hex[:8].upper())
        b = Booking(
            user_id=u.id,
            booking_type='Solar Panels',
            booking_date=date(2025, 12, 25),
            address='123 Green Street',
            booking_number=booking_number
        )
        db.session.add(b)
        db.session.commit()
        print(f"Booking created: {b.booking_number}")

        # Verify
        fetched_b = Booking.query.filter_by(booking_number=booking_number).first()
        assert fetched_b is not None
        assert fetched_b.user_id == u.id
        assert fetched_b.booking_type == 'Solar Panels'
        assert fetched_b.address == '123 Green Street'
        print("Verification Successful!")

if __name__ == "__main__":
    verify()
