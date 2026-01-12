from app import app, db
from app.models import User
import uuid

def verify():
    with app.app_context():
        # Create a test user
        email = f"test_verify_{uuid.uuid4().hex[:6]}@example.com"
        u = User(email=email)
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        
        # Reload user
        u = User.query.filter_by(email=email).first()
        if u.public_id and len(u.public_id) == 36:
            print(f"SUCCESS: User {email} has public_id: {u.public_id}")
        else:
            print(f"FAILURE: User {email} has invalid public_id: {u.public_id}")
        
        # Cleanup
        db.session.delete(u)
        db.session.commit()

if __name__ == "__main__":
    verify()
