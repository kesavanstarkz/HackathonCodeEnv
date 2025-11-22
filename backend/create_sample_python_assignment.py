"""
Create a sample Python coding assignment for testing
"""
import json
import requests

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Register and login as admin
print("1. Registering admin...")
reg = requests.post(f'{BASE_URL}/auth/register', json={
    'name': 'Coding Admin',
    'email': 'coding_admin@example.com',
    'password': 'admin123',
    'role': 'admin',
    'domain': 'fullstack'
})
print(f"   Status: {reg.status_code}")

print("\n2. Login as admin...")
login = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'coding_admin@example.com',
    'password': 'admin123'
})
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print(f"   Status: {login.status_code}")

# Step 2: Create Python coding assignment
print("\n3. Creating Python Coding Assignment...")

test_cases = [
    {
        "input": "5",
        "expected_output": "120",
        "hidden": False
    },
    {
        "input": "0",
        "expected_output": "1",
        "hidden": False
    },
    {
        "input": "3",
        "expected_output": "6",
        "hidden": False
    },
    {
        "input": "10",
        "expected_output": "3628800",
        "hidden": True
    }
]

assignment_data = {
    "title": "Calculate Factorial",
    "description": "Write a Python program that takes an integer N as input and prints the factorial of N. Factorial of N is the product of all positive integers less than or equal to N.",
    "domain": "fullstack",
    "difficulty": "easy",
    "problem_type": "coding",
    "language": "python",
    "test_cases": test_cases
}

response = requests.post(f'{BASE_URL}/assignments/create', json=assignment_data, headers=headers)
print(f"   Status: {response.status_code}")
assignment_response = response.json()
print(f"   Response: {json.dumps(assignment_response, indent=2)}")

assignment_id = assignment_response.get('id')

# Step 3: Get assignment details
print(f"\n4. Fetching assignment details...")
get_response = requests.get(f'{BASE_URL}/assignments/{assignment_id}', headers=headers)
assignment = get_response.json()
print(f"   Status: {get_response.status_code}")
print(f"   Assignment: {assignment['title']}")
print(f"   Problem Type: {assignment['problem_type']}")
print(f"   Language: {assignment['language']}")
print(f"   Test Cases: {len(assignment['test_cases'])}")

# Step 4: Test with correct Python code
print("\n5. Testing with CORRECT Python code...")
correct_code = """
n = int(input())
result = 1
for i in range(1, n + 1):
    result *= i
print(result)
"""

submit_response = requests.post(f'{BASE_URL}/assignments/submit-code', 
    json={
        'assignment_id': assignment_id,
        'code': correct_code
    },
    headers=headers
)
results = submit_response.json()
print(f"   Status: {submit_response.status_code}")
print(f"   All tests passed: {results['success']}")
print(f"   Passed: {results['passed_tests']}/{results['total_tests']}")
if results.get('code_error'):
    print(f"   Error: {results['code_error']}")
else:
    print("   Test Details:")
    for r in results['results']:
        status = "PASS" if r['passed'] else "FAIL"
        print(f"     Test {r['test_id']}: {status} (input={r['input']}, expected={r['expected_output']}, got={r['actual_output']})")

# Step 5: Test with incorrect Python code
print("\n6. Testing with INCORRECT Python code...")
incorrect_code = """
n = int(input())
print(n * 2)
"""

submit_response = requests.post(f'{BASE_URL}/assignments/submit-code', 
    json={
        'assignment_id': assignment_id,
        'code': incorrect_code
    },
    headers=headers
)
results = submit_response.json()
print(f"   Status: {submit_response.status_code}")
print(f"   All tests passed: {results['success']}")
print(f"   Passed: {results['passed_tests']}/{results['total_tests']}")
print("   Test Details:")
for r in results['results']:
    status = "PASS" if r['passed'] else "FAIL"
    print(f"     Test {r['test_id']}: {status} (input={r['input']}, expected={r['expected_output']}, got={r['actual_output']})")

print("\n" + "="*60)
print("Python Coding Assignment creation and testing complete!")
print("="*60)
print(f"\nAssignment ID: {assignment_id}")
print("You can now login as employee and attempt this assignment from the dashboard!")
