# scripts/setup.py
import os
import sys
from pathlib import Path

def main():
    print("Starting full setup...")
    
    # 1. Seed database
    print("\nSeeding database...")
    os.system("python scripts/seed.py")
    
    # 2. Create embeddings
    print("\nCreating embeddings...")
    os.system("python scripts/seed_embeddings.py")
    
    # 3. Verify setup
    print("\nVerifying setup...")
    os.system("python scripts/check_db.py")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    sys.path.append(str(Path(__file__).parent.parent))
    main()