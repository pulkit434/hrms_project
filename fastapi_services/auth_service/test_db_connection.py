from sqlalchemy import create_engine

DATABASE_URL = "postgresql://ashim.sharma@localhost:5432/hrms_db"  # No password

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Connected to PostgreSQL successfully!")
except Exception as e:
    print(f"❌ Error: {e}")