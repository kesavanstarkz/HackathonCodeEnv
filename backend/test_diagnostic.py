import sys
import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

try:
    print("Testing Employee Dashboard Flow...")
    
    # Test 1: Get assignments (public endpoint)
    print("\n1. Testing GET /assignments/...")
    resp = client.get('/assignments/')
    print(f"   Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"   ERROR: {resp.text}")
    else:
        print(f"   Success: {len(resp.json())} assignments found")
    
    # Test 2: Login
    print("\n2. Testing POST /auth/login...")
    resp = client.post('/auth/login', json={
        'email': 'test_user2@example.com',
        'password': 'secret123'
    })
    print(f"   Status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"   ERROR: {resp.text}")
    else:
        print(f"   Success: Token obtained")
        token = resp.json().get('access_token')
        
        # Test 3: Get assignments with auth
        print("\n3. Testing GET /assignments/ (with auth)...")
        headers = {'Authorization': f'Bearer {token}'}
        resp = client.get('/assignments/', headers=headers)
        print(f"   Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"   ERROR: {resp.text}")
        else:
            assignments = resp.json()
            print(f"   Success: {len(assignments)} assignments")
            if assignments:
                print(f"   First assignment: {json.dumps(assignments[0], indent=6)}")

except Exception as e:
    print(f"\nException occurred: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n✅ Diagnostic complete")
