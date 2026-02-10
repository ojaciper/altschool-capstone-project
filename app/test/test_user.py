
from app.test.test_auth import test_login, test_signup

def test_get_current_user(client):
    test_signup(client)
    token = test_login(client)
    
    response = client.get("/api/v1/user/me", headers={"Authorization":f"Bearer {token}"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
    
def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/user")
    assert response.status_code == 401
    
def test_get_user_by_email_success(client):
    token = test_login(client)
    response = client.get("/api/v1/user/user@example.com", headers={"Authorization":f"bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"]=="user@example.com"
    
def test_get_user_by_email_not_found(client):
        token = test_login(client)
        response = client.get("/api/v1/user/use@example.com", headers={"Authorization":f"bearer {token}"})
        assert response.status_code == 404

    