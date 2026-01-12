from app import app, db
from app.models import User
import uuid

def backfill():
    with app.app_context():
        users = User.query.filter(User.public_id == None).all()
        print(f"Found {len(users)} users to backfill.")
        for user in users:
            user.public_id = str(uuid.uuid4())
            print(f"Generated ID for user {user.email}")
        
        if users:
            db.session.commit()
            print("Backfill complete.")
        else:
            print("No users needed backfill.")

if __name__ == "__main__":
    backfill()
