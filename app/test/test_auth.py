def test_signup(client):
    payload = {
        "full_name": "string",
        "email": "user@example.com",
        "role": "student",
        "is_active": True,
        "password": "string",
    }
    respons = client.post("/api/v1/auth/signup", json=payload)
    assert respons.status_code == 201
    
def test_email_aready_exist(client):
    payload = {
        "full_name": "string",
        "email": "user@example.com",
        "role": "student",
        "is_active": True,
        "password": "string",
    }
    respons = client.post("/api/v1/auth/signup", json=payload)
    assert respons.status_code == 400
    
# def test_internal_server_error(client):
#     payload = {
#         "full_name": "string",
#         "email": "user@example.com",
#         "role": "student",
#         "is_active": True,
#         "password": "string",
#     }
#     respons = client.post("/api/v1/auth/signup", json=payload)
#     assert respons.status_code == 500
    
def test_login(client):
    payload = {
        "username": "user@example.com",
        "password": "string",
    }
    respons = client.post("/api/v1/auth/login", data=payload)
    assert respons.status_code in [200,403]
    response_data = respons.json()
    assert   "access_token" in response_data
    assert response_data['token_type'] == "bearer"

    
    
    
def test_wrong_details(client):
    payload = {
        "username": "use@example.com",
        "password": "strin",
    }
    respons = client.post("/api/v1/auth/login", data=payload)
    assert respons.status_code == 401

def test_account_not_active(client):
    payload = {
        "username": "user@example.com",
        "password": "string",
    }
    respons = client.post("/api/v1/auth/login", data=payload)
    print(respons.status_code)
    assert respons.status_code in [200,403]