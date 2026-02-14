from app.test.helpers import admin_login, register_user, login_user
from datetime import timezone, datetime


def test_enroll_success(client):
    token = admin_login(client)
    ## create course
    payload = {
        "title": "Introduction Tech",
        "course_code": "Tech-101",
        "capacity": 2,
        "is_active": True,
    }
    respone = client.post(
        "/api/v1/course",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    course_id = respone.json()["id"]

    ##create student
    student = register_user(
        client,
        "another student",
        "anotherstudent@example.com",
        "student",
        True,
        "string",
    )
    student_id = student["id"]

    ## enroll a course
    user_token = login_user(client, "anotherstudent@example.com", "string")

    enroll_payload = {
        "user_id": student_id,
        "course_id": course_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    res = client.post(
        "/api/v1/enrollment/",
        json=enroll_payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert res.status_code == 201


def test_get_all_enroll(client):
    token = admin_login(client)
    response = client.get(
        "/api/v1/enrollment/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert isinstance(response.json()["data"], list)


def test_get_course_enroll_by_id(client):
    token = admin_login(client)
    response = client.get(
        "/api/v1/enrollment/",
        headers={"Authorization": f"Bearer {token}"},
    )
    course_id = response.json()["data"][0]["course_id"]
    res = client.get(
        f"/api/v1/enrollment/{course_id}/enrollment",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "success"
    assert isinstance(res.json()["data"], list)


def test_enroll_course_not_active(client):
    token = admin_login(client)
    ## create course
    payload = {
        "title": "Introduction Software development",
        "course_code": "ISD-101",
        "capacity": 2,
        "is_active": False,
    }
    respone = client.post(
        "/api/v1/course",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    course_id = respone.json()["id"]

    ##create student
    student = register_user(
        client,
        "David",
        "David@example.com",
        "student",
        True,
        "string",
    )
    student_id = student["id"]
    ## enroll a course
    user_token = login_user(client, "anotherstudent@example.com", "string")

    enroll_payload = {
        "user_id": student_id,
        "course_id": course_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    res = client.post(
        "/api/v1/enrollment/",
        json=enroll_payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    print(res.json())
    assert res.status_code == 409
    assert res.json()["detail"] == "course is not active"


def test_enroll_course_full(client):
    token = admin_login(client)

    ## create course
    payload = {
        "title": "Introduction Software",
        "course_code": "IS-101",
        "capacity": 1,
        "is_active": True,
    }
    respone = client.post(
        "/api/v1/course",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    course_id = respone.json()["id"]

    ## first user
    ##create student
    student = register_user(
        client,
        "Abia",
        "Abia@example.com",
        "student",
        True,
        "string",
    )
    student_id = student["id"]
    ## enroll a course
    user_token = login_user(client, "anotherstudent@example.com", "string")

    enroll_payload = {
        "user_id": student_id,
        "course_id": course_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    client.post(
        "/api/v1/enrollment/",
        json=enroll_payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    ## second user
    ##create student
    student = register_user(
        client,
        "Daniel",
        "daniel@example.com",
        "student",
        True,
        "string",
    )
    user2 = student["id"]
    ## enroll a course
    user2_token = login_user(client, "anotherstudent@example.com", "string")

    enroll_payload = {
        "user_id": user2,
        "course_id": course_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    res = client.post(
        "/api/v1/enrollment/",
        json=enroll_payload,
        headers={"Authorization": f"Bearer {user2_token}"},
    )

    assert res.status_code == 409
    assert res.json()["detail"] == "Course is full"


def test_enroll_already_enrolled(client):
    token = admin_login(client)
    ## create course
    payload = {
        "title": "Introduction Software and ICT",
        "course_code": "ISI-101",
        "capacity": 1,
        "is_active": True,
    }
    respone = client.post(
        "/api/v1/course",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )
    course_id = respone.json()["id"]
    student = register_user(
        client,
        "Sophia",
        "Sohia@example.com",
        "student",
        True,
        "string",
    )
    student_id = student["id"]
    ## enroll a course
    user_token = login_user(client, "anotherstudent@example.com", "string")

    enroll_payload = {
        "user_id": student_id,
        "course_id": course_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    client.post(
        "/api/v1/enrollment/",
        json=enroll_payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    res = client.post(
        "/api/v1/enrollment/",
        json=enroll_payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert res.status_code == 409


# def test_remove_enrollment(client):
#     token = admin_login(client)
#     ## create course
#     payload = {
#         "title": "Introduction Software and Facebook",
#         "course_code": "ISF-101",
#         "capacity": 1,
#         "is_active": True,
#     }
#     respone = client.post(
#         "/api/v1/course",
#         json=payload,
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     course_id = respone.json()["id"]
#     student = register_user(
#         client,
#         "Sohpy",
#         "sohpy@example.com",
#         "student",
#         True,
#         "string",
#     )
#     student_id = student["id"]
#     ## enroll a course
#     user_token = login_user(client, "anotherstudent@example.com", "string")

#     enroll_payload = {
#         "user_id": student_id,
#         "course_id": course_id,
#         "created_at": datetime.utcnow().isoformat(),
#     }
#     client.post(
#         "/api/v1/enrollment/",
#         json=enroll_payload,
#         headers={"Authorization": f"Bearer {user_token}"},
#     )
#     res = client.post(
#         f"/api/v1/enrollment/{student_id}/remove",
#         params={
#             "course_id":str(course_id)
#         },
#         headers={"Authorization": f"Bearer {token}"},
#     )
#     print(res.request.url)
#     assert res.status_code == 200
