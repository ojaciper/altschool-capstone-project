import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import SessionLocal
from app.main import app
from app.dependency import deps

SQLALCHEMY_DATABASE_URL = "sqlite:///.test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
    
)
TestinSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

@pytest.fixture(scope="session",autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db= TestinSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[deps.get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)