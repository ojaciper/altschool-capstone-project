from app.test.helpers import admin_login,login_user,register_user


def test_create_course(client):
    token = admin_login(client)
    payload = {
        "title": "Introduction Photo Editing",
        "course_code": "IPE-101",
        "capacity": 2,
        "is_active": True,
    }
    respone = client.post(
        "/api/v1/course", json=payload, headers={"Authorization": f"Bearer {token}"}
    )

    assert respone.status_code == 201
    assert respone.json()["course_code"] == "IPE-101"
    assert isinstance(respone.json(), dict)


def test_existing_course_title(client):
    token = admin_login(client)
    payload = {
        "title": "Introduction Photo Editing",
        "course_code": "IPE-101",
        "capacity": 2,
        "is_active": True,
    }
    respone = client.post(
        "/api/v1/course", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert respone.status_code == 409


def test_course_capicity_greater_than_zero(client):
    token = admin_login(client)
    payload = {
        "title": "Introduction Photo Editing",
        "course_code": "IPE-101",
        "capacity": 0,
        "is_active": True,
    }
    respone = client.post(
        "/api/v1/course", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    assert respone.status_code == 409


def test_get_active_courses(client):
    token = admin_login(client)
    payload = {
        "title": "Introduction Photo Editing",
        "course_code": "IPE-101",
        "capacity": 2,
        "is_active": True,
    }
    client.post(
        "/api/v1/course", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get(
        "/api/v1/course", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert "data" in response.json()
    
    
def test_get_course_by_id(client):
    token = admin_login(client)
    payload = {
        "title": "Introduction Photo Editing and content creating",
        "course_code": "IPECC-101",
        "capacity": 2,
        "is_active": True,
    }
    res = client.post(
        "/api/v1/course", json=payload, headers={"Authorization": f"Bearer {token}"}
    )
    print(res.json())
    course_id = res.json()["id"]
    response = client.get(
        f"/api/v1/course/{course_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_course_not_found(client):
    register_user(client, "string", "user@example.com", "student", True, "string")
    token = login_user(client, "user@example.com", "string")
    response = client.get(
        f"/api/v1/course/5ee24fea-76de-4ad0-a01e-a26837d30279", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    
def test_activate_course(client):
        token = admin_login(client)
        payload = {
        "title": "Introduction Photo Editing and content creating",
        "course_code": "IPECC-101",
        "capacity": 2,
        "is_active": True,
    }