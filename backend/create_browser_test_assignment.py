#!/usr/bin/env python
"""
Create a small Python coding assignment via the backend API so you can solve it in the browser.
This script logs in as admin (existing admin credentials in create_sample script), creates the assignment,
and prints the assignment id and details.

Run:
    python create_browser_test_assignment.py

"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "adminpass")

# If your setup uses different admin creds, set the env vars or edit these constants.

# 1. Ensure admin exists (register may fail if already exists)
print("1. Ensuring admin user exists (register)...")
resp = requests.post(f"{BASE}/auth/register", json={
    "name": "Admin User",
    "email": ADMIN_EMAIL,
    "password": ADMIN_PASSWORD,
    "role": "admin",
    "domain": "general"
})
print("   Register status:", resp.status_code)

# 2. Login as admin
print("2. Logging in as admin...")
resp = requests.post(f"{BASE}/auth/login", json={
    "email": ADMIN_EMAIL,
    "password": ADMIN_PASSWORD
})
if resp.status_code != 200:
    print("   Login failed:", resp.status_code, resp.text)
    raise SystemExit(1)

token = resp.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}
print("   Logged in, token length:", len(token))

# 3. Create assignment
print("3. Creating Python assignment 'Sum Two Numbers'...")
assignment_payload = {
    "title": "Sum Two Numbers",
    "description": "Read two integers from input (separated by space or newline) and print their sum.",
    "problem_type": "coding",
    "language": "python",
    "domain": "general",
    "difficulty": "easy",
    "test_cases": [
        {"input": "1 2", "expected_output": "3"},
        {"input": "10 20", "expected_output": "30"},
        {"input": "-5 5", "expected_output": "0"},
        {"input": "123 456", "expected_output": "579"}
    ]
}
resp = requests.post(f"{BASE}/assignments/create", json=assignment_payload, headers=headers)
print("   Create status:", resp.status_code)
print(resp.json())

if resp.status_code == 200:
    assignment_id = resp.json().get("id")
    print(f"\nAssignment created successfully. ID: {assignment_id}")
    print(f"Open the frontend at http://localhost:5173 and login as a non-admin user to attempt assignment {assignment_id}.")
else:
    print("Assignment creation failed. Response:", resp.text)

print("Done.")
