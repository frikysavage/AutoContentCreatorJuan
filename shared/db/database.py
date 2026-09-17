from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.config.settings import settings

# In production this would be postgresql://...
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
