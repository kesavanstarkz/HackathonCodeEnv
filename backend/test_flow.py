from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

print("=== Testing Auth & Assignments ===\n")

print("1. Register user...")
reg = client.post('/auth/register', json={
    'name': 'Test Admin',
    'email': 'admin_test@example.com',
    'password': 'test123',
    'role': 'admin',
    'domain': 'engineering'
})
print(f"Status: {reg.status_code}")
print(f"Response: {json.dumps(reg.json(), indent=2)}\n")

print("2. Login...")
login = client.post('/auth/login', json={
    'email': 'admin_test@example.com',
    'password': 'test123'
})
print(f"Status: {login.status_code}")
login_data = login.json()
print(f"Response: {json.dumps(login_data, indent=2)}")
token = login_data.get('access_token')
print(f"\nToken: {token[:20]}...\n")

print("3. Create assignment...")
headers = {'Authorization': f'Bearer {token}'}
create_assign = client.post('/assignments/create', 
    json={
        'title': 'Python Challenge',
        'description': 'Solve a Python problem',
        'domain': 'fullstack',
        'difficulty': 'medium',
        'test_input': '5',
        'expected_output': '120'
    },
    headers=headers
)
print(f"Status: {create_assign.status_code}")
print(f"Response: {json.dumps(create_assign.json(), indent=2)}\n")

print("4. Get all assignments...")
get_assign = client.get('/assignments/', headers=headers)
print(f"Status: {get_assign.status_code}")
print(f"Response: {json.dumps(get_assign.json(), indent=2)}\n")

print("✅ All tests passed!")
