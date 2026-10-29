import os
os.environ["TESTING"]="1"
import pytest
from app import app, db, Url
TEST_DB = "sqlite:///test.db"
@pytest.fixture(autouse=True)
def setup_test_db():
    app.config["TESTING"]=True
    app.config["SQLALCHEMY_DATABASE_URI"]=TEST_DB
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()
def test_shorten_without_url():
   
   
    with app.test_client() as client:
        response=client.post("/shorten",json={})
        assert response.status_code==400
        assert response.json['error']=="URL is required"
def test_shorten_valid_url():
    with app.test_client() as client:
        response=client.post("/shorten",json={"url":"https://instagram.com"})
        assert response.status_code==201
        assert "short_code" in response.json
def test_redirect_to_url():
    with app.test_client() as client:
        response=client.get("/abcccc")
        assert response.status_code==404
        assert response.json['message']=="short url not found"
def test_redirect_to_url_success():
    with app.app_context():
        url = Url(
            original_url="https://instagram.com",
            short_code="mSesk6"
        )
        db.session.add(url)
        db.session.commit()
        original_url=url.original_url
    with app.test_client() as client:
        response = client.get(
            "/mSesk6",
            follow_redirects=False
        )
        assert response.status_code==302
        assert response.location==original_url
def test_urls():
    with app.test_client() as client:
        response=client.get("/urls")
        assert response.status_code==200
        assert isinstance(response.json,list)
def test_analytics():
    with app.test_client() as client:
        response=client.get("/analytics")
        assert response.status_code==200
        assert "total_urls" in response.json
        assert "total_clicks" in response.json
        assert "most_click" in response.json
def test_shorten_invalid_url():
    with app.test_client() as client:
        response=client.post("/shorten",json={"url":"not a valid url"})
        assert response.status_code==400
        assert response.json['error']=="Invalid URL"
