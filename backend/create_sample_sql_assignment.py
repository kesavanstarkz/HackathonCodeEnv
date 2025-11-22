"""
Create a sample SQL assignment for testing
"""
import json
import requests

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Register and login as admin
print("1. Registering admin...")
reg = requests.post(f'{BASE_URL}/auth/register', json={
    'name': 'SQL Admin',
    'email': 'sql_admin@example.com',
    'password': 'admin123',
    'role': 'admin',
    'domain': 'data'
})
print(f"   Status: {reg.status_code}")

print("\n2. Login as admin...")
login = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'sql_admin@example.com',
    'password': 'admin123'
})
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}
print(f"   Status: {login.status_code}")

# Step 2: Create SQL assignment
print("\n3. Creating SQL Assignment...")
schema = """
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary INTEGER
);

INSERT INTO employees VALUES (1, 'Alice', 'Sales', 50000);
INSERT INTO employees VALUES (2, 'Bob', 'Engineering', 75000);
INSERT INTO employees VALUES (3, 'Charlie', 'Sales', 55000);
INSERT INTO employees VALUES (4, 'Diana', 'Engineering', 80000);
INSERT INTO employees VALUES (5, 'Eve', 'HR', 45000);
"""

# Problem: Write a query to count employees by department
# Expected output: List of departments with employee counts
test_cases = [
    {
        "description": "Must include Engineering department with count 2",
        "expected_result": json.dumps([
            {"department": "Engineering", "emp_count": 2},
            {"department": "HR", "emp_count": 1},
            {"department": "Sales", "emp_count": 2}
        ]),
        "hidden": False
    },
    {
        "description": "Results must be ordered by department name",
        "expected_result": json.dumps([
            {"department": "Engineering", "emp_count": 2},
            {"department": "HR", "emp_count": 1},
            {"department": "Sales", "emp_count": 2}
        ]),
        "hidden": False
    },
    {
        "description": "Must group correctly (Engineering has 2)",
        "expected_result": json.dumps([
            {"department": "Engineering", "emp_count": 2},
            {"department": "HR", "emp_count": 1},
            {"department": "Sales", "emp_count": 2}
        ]),
        "hidden": False
    },
    {
        "description": "Complete validation test",
        "expected_result": json.dumps([
            {"department": "Engineering", "emp_count": 2},
            {"department": "HR", "emp_count": 1},
            {"department": "Sales", "emp_count": 2}
        ]),
        "hidden": True  # Hidden test case
    }
]

assignment_data = {
    "title": "Employee Database Query",
    "description": "Write SQL queries to analyze the employee and department data. Find employee counts, departments, and salary information.",
    "domain": "data",
    "difficulty": "medium",
    "problem_type": "sql",
    "sql_schema": schema,
    "sql_query": "SELECT * FROM employees;",  # Reference solution (optional)
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
print(f"   Test Cases: {len(assignment['test_cases'])}")

# Step 4: Test with correct query
print("\n5. Testing with CORRECT SQL query...")
correct_query = "SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department ORDER BY department;"
submit_response = requests.post(f'{BASE_URL}/assignments/submit-sql', 
    json={
        'assignment_id': assignment_id,
        'sql_query': correct_query
    },
    headers=headers
)
results = submit_response.json()
print(f"   Status: {submit_response.status_code}")
print(f"   All tests passed: {results['success']}")
print(f"   Passed: {results['passed_tests']}/{results['total_tests']}")
if not results['success']:
    print(f"   Error: {results.get('user_query_error')}")

# Step 5: Test with an incorrect query
print("\n6. Testing with INCORRECT SQL query...")
incorrect_query = "SELECT * FROM employees WHERE salary > 100000;"
submit_response = requests.post(f'{BASE_URL}/assignments/submit-sql', 
    json={
        'assignment_id': assignment_id,
        'sql_query': incorrect_query
    },
    headers=headers
)
results = submit_response.json()
print(f"   Status: {submit_response.status_code}")
print(f"   All tests passed: {results['success']}")
print(f"   Passed: {results['passed_tests']}/{results['total_tests']}")

print("\n✅ SQL Assignment creation and testing complete!")
print(f"\n📝 Assignment ID: {assignment_id}")
print("You can now login as employee and attempt this assignment from the dashboard!")
