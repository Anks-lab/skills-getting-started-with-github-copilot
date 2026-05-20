import pytest
from httpx import AsyncClient
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_duplicate():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        # First signup
        response1 = await ac.post(f"/activities/{activity}/signup", params={"email": test_email})
        # Duplicate signup
        response2 = await ac.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_unregister_participant():
    # Arrange
    test_email = "removeuser@mergington.edu"
    activity = "Programming Class"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Sign up first
        await ac.post(f"/activities/{activity}/signup", params={"email": test_email})
        # Act
        response = await ac.delete(f"/activities/{activity}/unregister", params={"email": test_email})
        # Try to remove again (should fail)
        response2 = await ac.delete(f"/activities/{activity}/unregister", params={"email": test_email})
    # Assert
    assert response.status_code == 200
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]
