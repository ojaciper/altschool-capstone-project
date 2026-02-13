from app.test.test_auth import test_login, test_signup
from app.test.helpers import register_user, login_user



def test_get_current_user(client):
    register_user(client, "string", "user@example.com", "student", True, "string")
    token = login_user(client, "user@example.com", "string")

    response = client.get(
        "/api/v1/user/me", headers={"Authorization": f"Bearer {token}"}
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_get_current_user_unauthorized(client):
    response = client.get("/api/v1/user")
    assert response.status_code == 401


def test_get_user_by_email_success(client):
    token = login_user(client, "user@example.com", "string")
    response = client.get(
        "/api/v1/user/user@example.com", headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_get_user_by_email_not_found(client):
    token = login_user(client, "user@example.com", "string")
    response = client.get(
        "/api/v1/user/use@example.com", headers={"Authorization": f"bearer {token}"}
    )
    assert response.status_code == 404


def test_get_all_users_admin_only(client):
    register_user(client, "string", "admin@gmail.com", "admin", True, "admin")
    token = login_user(client, "admin@gmail.com", "admin")

    register_user(client, "string", "user1@gmail.com", "student", True, "password")
    register_user(client, "string", "user2@gmail.com", "student", True, "password")
    register_user(client, "string", "user3@gmail.com", "student", True, "password")

    response = client.get("/api/v1/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"]) >= 2


def test_get_all_user_not_admin(client):
    register_user(client, "string", "user1@gmail.com", "student", True, "password")
    token = login_user(client, "user1@gmail.com", "password")

    response = client.get("/api/v1/user", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


# def test_activate_user_success(client):
#     admin_user = register_user(
#         client, "string", "admin@gmail.com", "admin", True, "admin"
#     )
#     admin_token = login_user(client, "admin@gmail.com", "admin")
#     user = register_user(
#         client, "string", "user10@gmail.com", "student", False, "password"
#     )
  
#     user_id= user['id']
    
#     res = client.patch(
#         f"/api/v1/user/{user_id}/activate",
#         json={"is_active": True},
#         headers={"Authorization": f"Bearer {admin_token}"},
#     )
#     assert res.status_code == 200
#     assert res.json()["is_active"] is True
