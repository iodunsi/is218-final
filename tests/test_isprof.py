# tests/test_isprof.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user_model import Base, User

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(setup_database):
    session = TestingSessionLocal()
    yield session
    session.close()

def test_is_professional_default(db_session):
    # Create a new user
    new_user = User(
        nickname="testuser",
        email="testuser@example.com",
        role="AUTHENTICATED",
        first_name="Test",
        last_name="User",
        bio="Test bio",
        profile_picture_url="http://example.com/profile.jpg",
        linkedin_profile_url="http://linkedin.com/in/testuser",
        github_profile_url="http://github.com/testuser",
        hashed_password="hashed_password"
    )
    db_session.add(new_user)
    db_session.commit()

    # Retrieve the user
    user = db_session.query(User).filter_by(nickname="testuser").first()

    # Assert that the default value of is_professional is False
    assert user.is_professional == False

def test_set_is_professional(db_session):
    # Create a new user with is_professional set to True
    new_user = User(
        nickname="professional_user",
        email="professional_user@example.com",
        role="AUTHENTICATED",
        first_name="Professional",
        last_name="User",
        bio="Professional bio",
        profile_picture_url="http://example.com/profile.jpg",
        linkedin_profile_url="http://linkedin.com/in/professionaluser",
        github_profile_url="http://github.com/professionaluser",
        hashed_password="hashed_password",
        is_professional=True
    )
    db_session.add(new_user)
    db_session.commit()

    # Retrieve the user
    user = db_session.query(User).filter_by(nickname="professional_user").first()

    # Assert that is_professional is True
    assert user.is_professional == True
