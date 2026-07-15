import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db
from app.models.asset import Base
from app.messaging.debug_publisher import FakeEventPublisher
from app.infrastructure.messaging import get_event_publisher


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture()
def db_session():

    Base.metadata.create_all(
        bind=engine
    )

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()

        Base.metadata.drop_all(
            bind=engine
        )


@pytest.fixture()
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def fake_publisher():

    publisher = FakeEventPublisher()

    def override():
        return publisher

    app.dependency_overrides[get_event_publisher] = override

    yield publisher

    app.dependency_overrides.pop(get_event_publisher, None)