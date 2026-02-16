import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test getting activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Test signup for activity
def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

# Test unregister from activity
def test_unregister_from_activity():
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    # Ensure registered
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Unregister again should fail
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
    assert "not registered" in response2.json()["detail"]

# Test signup for non-existent activity
def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

# Test unregister for non-existent activity
def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
