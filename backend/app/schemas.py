from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    domain: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TestCaseInput(BaseModel):
    """For SQL or Coding test case"""
    input: Optional[str] = None  # For coding problems
    expected_output: Optional[str] = None  # For coding problems
    sql_query: Optional[str] = None  # For SQL problems
    expected_result: Optional[str] = None  # For SQL problems (JSON string)
    hidden: bool = False

class AssignmentCreate(BaseModel):
    title: str
    description: str
    domain: str
    difficulty: str
    problem_type: str = "coding"  # "coding" or "sql"
    
    # For coding problems
    language: Optional[str] = None  # python or javascript
    test_input: Optional[str] = None
    expected_output: Optional[str] = None
    
    # For SQL problems
    sql_schema: Optional[str] = None
    sql_query: Optional[str] = None
    test_cases: Optional[List[TestCaseInput]] = None

class SQLSubmission(BaseModel):
    assignment_id: int
    sql_query: str

class CodeSubmission(BaseModel):
    assignment_id: int
    code: str
