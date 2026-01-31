import pytest

@pytest.mark.django_db
def test_register(api_client):
    res = api_client.post("/api/auth/register", {
        "username": "newuser",
        "email": "new@x.com",
        "password": "Password123!",
        "password_confirm": "Password123!"
    }, format="json")
    assert res.status_code in (200, 201)

@pytest.mark.django_db
def test_login(api_client, user):
    res = api_client.post("/api/auth/login", {
        "username": "user1",
        "password": "Password123!"
    }, format="json")
    assert res.status_code == 200
    data = res.json()
    # your login returns tokens.access/refresh
    assert "tokens" in data
    assert "access" in data["tokens"]

@pytest.mark.django_db
def test_me(auth_client):
    res = auth_client.get("/api/auth/me")
    assert res.status_code == 200
