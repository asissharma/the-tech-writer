# db/database.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Determine the base directory and set the database file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db", "database.sqlite")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# SQLite connection URL (using an absolute path)
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create the SQLAlchemy engine with necessary SQLite arguments
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the base class for our models
Base = declarative_base()

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize all models (create tables)
def init_models():
    Base.metadata.create_all(bind=engine)

# Function to test the database connection
def test_db_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = result.fetchall()
            return True, f"Connected successfully. Found tables: {[table[0] for table in tables]}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"
