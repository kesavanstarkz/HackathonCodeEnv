from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('--- Register ---')
reg = client.post('/auth/register', json={'name':'Test User','email':'test_user2@example.com','password':'secret123','role':'employee','domain':'engineering'})
print(reg.status_code)
print(reg.json())

print('--- Login ---')
login = client.post('/auth/login', json={'email':'test_user2@example.com','password':'secret123'})
print(login.status_code)
print(login.json())
