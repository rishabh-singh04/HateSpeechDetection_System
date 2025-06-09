# app/db/seed.py
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

# Initialize password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_data():
    # Import inside function to avoid circular imports
    from app.db.session import SessionLocal
    from app.db.models.user import User
    from app.db.models.policy import PolicyDocument
    
    db = SessionLocal()
    
    try:
        # Sample users
        users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "hashed_password": get_password_hash("securepassword123"),
                "is_superuser": True
            },
            {
                "username": "moderator",
                "email": "moderator@example.com",
                "hashed_password": get_password_hash("modpass123"),
                "is_superuser": False
            }
        ]
        
        for user_data in users:
            if not db.query(User).filter(User.username == user_data["username"]).first():
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=user_data["hashed_password"],
                    is_superuser=user_data["is_superuser"],
                    full_name=f"{user_data['username'].title()} User"
                )
                db.add(user)
                db.commit()
                print(f"Created user: {user_data['username']}")
            else:
                print(f"User {user_data['username']} already exists")

        # Sample policies
        # policies = [
        #     {
        #         "name": "Google Hate Speech Policy",
        #         "content": open("google_policy.txt").read()
        #     },
        #     {
        #         "name": "Indian Penal Code Provisions",
        #         "content": open("indian_penal_code.txt").read() 
        #     },
        #     {
        #         "name": "Reddit Hate Speech Policy",
        #         "content": open("reddit_policy.txt").read()
        #     },
        #     {
        #         "name": "Meta Policy",
        #         "content": open("meta_policy.txt").read() 
        #     },
        #     {
        #         "name": "US Laws for Hate Speech",
        #         "content": open("us_laws.txt").read()
        #     }

        # ]
        policies = [
            {
                "name": os.path.splitext(filename)[0].replace("_", " ").title(),
                "content": open(f"app/data/policy_docs/{filename}", encoding='utf-8').read()
            }
            for filename in os.listdir("app/data/policy_docs") 
            if filename.endswith(".txt")
        ]
        
        for policy_data in policies:
            if not db.query(PolicyDocument).filter(PolicyDocument.name == policy_data["name"]).first():
                policy = PolicyDocument(
                    name=policy_data["name"],
                    content=policy_data["content"]
                )
                db.add(policy)
                db.commit()
                print(f"Created policy: {policy_data['name']}")
            else:
                print(f"Policy {policy_data['name']} already exists")
                
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()