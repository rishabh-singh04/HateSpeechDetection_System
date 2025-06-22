# scripts/check_db.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import SessionLocal
from app.db.models.policy import PolicyDocument

def check_db():
    db = SessionLocal()
    try:
        count = db.query(PolicyDocument).count()
        print(f"Database has {count} policies")
        if count > 0:
            print("Sample policy:", db.query(PolicyDocument).first().name)
    finally:
        db.close()

if __name__ == "__main__":
    check_db()