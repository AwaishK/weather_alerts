"""
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from app.main import app
from app.weather_alerts_api.core.views.subscription  import get_session
from app import Base
from utils.config_parser import configuration_parser

config = configuration_parser()
database_config = config["TEST_DATABASE"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{database_config['USER']}:{database_config['PASSWORD']}@localhost/{database_config['NAME']}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db

client = TestClient(app)


class TestSubscription:
    def test_create_subscription(self):
        email = "kkkkk.rathi@gmail.com"
        response = client.post(
            "/subscription",
            json={
                "email": email,
                "cityId": "1",
                "stateId": "1",
                "countryId": "1",
                "conditions": ["<0", ">100"],
                "isActive": True
            },
        )
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == email

        _id = data["id"]
        response = client.get(f"/subscription/{_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == email
    
    def test_list_subscriptions(self):
        response = client.get(f"/subscriptions")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)

    def test_read_subscription(self):
        response = client.get(f"/subscriptions")
        data = response.json()
        _id = data[0]["id"]
        response = client.get(f"/subscription/{_id}")
        assert response.status_code == 200
    
    def test_update_subscription(self):
        response = client.get(f"/subscriptions")
        data = response.json()
        _id = data[0]["id"]

        response = client.put(
            f"/subscription/{_id}",
            json={
                "email": "awaish.kumar@gmail.com",
                "cityId": "1",
                "stateId": "1",
                "countryId": "1",
                "conditions": ["<0", ">100"],
                "isActive": True
            },
        )
        assert response.status_code == 200
    
    def test_delete_subscription(self):
        response = client.get(f"/subscriptions")
        data = response.json()
        _id = data[0]["id"]

        response = client.delete(f"/subscription/{_id}")
        assert response.status_code == 200
