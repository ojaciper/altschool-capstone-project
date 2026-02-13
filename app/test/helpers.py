def register_user(client,full_name:str,email: str, role:str, is_active: bool,password: str):
    payload = {
        "full_name": full_name,
        "email": email,
        "role": role,
        "is_active":is_active,
        "password": password
    }
    respons = client.post("/api/v1/auth/signup", json=payload)
    return respons.json()


def login_user(client,username:str, password:str):
    payload = {
        "username":username,
        "password":password
    }
    respons = client.post("/api/v1/auth/login", data=payload)
    return respons.json()["access_token"]

def admin_login(client):
    register_user(client,"admin user", "admin@gmail.com","admin",True,"admin")
    return login_user(client, "admin@gmail.com", "admin")
