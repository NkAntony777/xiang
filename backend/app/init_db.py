#!/usr/bin/env python3
"""
Database initialization script.
Creates all tables and optionally imports initial data.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, engine, init_db
from app.models import Ganzhi, Nayin, Xiangyi, Shensha, GanzhiShensha, Xiji, Guanxi


def main():
    print("Creating database tables...")
    init_db()
    print("Database tables created successfully!")

    # Check if data already exists
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        count = db.query(Ganzhi).count()
        if count > 0:
            print(f"Database already has {count} ganzhi records.")
        else:
            print("Database is empty. Run import script to load data.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
