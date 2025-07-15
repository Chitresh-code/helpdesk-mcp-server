from sqlmodel import SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from server.config import settings

DATABASE_URL = settings.POSTGRES_DATABASE_URL

# Sync engine
engine = create_engine(DATABASE_URL, echo=True)

# Sync session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def init_db():
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully.")