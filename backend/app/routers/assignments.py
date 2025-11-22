from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.assignment import Assignment
from app.models.testcase import TestCase
from app.models.submission import Submission
from app.models.user import User
from app.schemas import AssignmentCreate, SQLSubmission, CodeSubmission
from app.services.sql_executor import execute_sql_problem
from app.services.judge0_executor import Judge0Executor
from app.services.local_executor import LocalCodeExecutor
from app.services.piston_executor import PistonExecutor

router = APIRouter(prefix="/assignments")

@router.get("/")
def get_assignments(db: Session = Depends(get_db)):
    assignments = db.query(Assignment).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "domain": a.domain,
            "difficulty": a.difficulty,
            "problem_type": a.problem_type,
        }
        for a in assignments
    ]

@router.get("/{assignment_id}")
def get_assignment(assignment_id: int, db: Session = Depends(get_db)):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    test_cases = db.query(TestCase).filter(TestCase.assignment_id == assignment_id).all()
    
    return {
        "id": assignment.id,
        "title": assignment.title,
        "description": assignment.description,
        "domain": assignment.domain,
        "difficulty": assignment.difficulty,
        "problem_type": assignment.problem_type,
        "language": assignment.language,
        "sql_schema": assignment.sql_schema,
        "test_input": assignment.test_input,
        "expected_output": assignment.expected_output,
        "test_cases": [
            {
                "id": tc.id,
                "input": tc.input,
                "expected_output": tc.expected_output,
                "sql_query": tc.sql_query,
                "expected_result": tc.expected_result,
                "hidden": tc.hidden,
            }
            for tc in test_cases
        ]
    }

@router.post("/create")
def create_assignment(data: AssignmentCreate, db: Session = Depends(get_db)):
    new_assignment = Assignment(
        title=data.title,
        description=data.description,
        domain=data.domain,
        difficulty=data.difficulty,
        problem_type=data.problem_type,
        language=data.language,  # Add language for coding problems
        test_input=data.test_input,
        expected_output=data.expected_output,
        sql_schema=data.sql_schema,
        sql_query=data.sql_query,
    )

    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    # Add test cases if provided
    if data.test_cases:
        for tc in data.test_cases:
            test_case = TestCase(
                assignment_id=new_assignment.id,
                input=tc.input,
                expected_output=tc.expected_output,
                sql_query=tc.sql_query,
                expected_result=tc.expected_result,
                hidden=tc.hidden,
            )
            db.add(test_case)
        db.commit()

    return {"message": "Assignment created successfully", "id": new_assignment.id}

@router.post("/submit-sql")
def submit_sql(submission: SQLSubmission, db: Session = Depends(get_db)):
    """Submit and test SQL query"""
    assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.problem_type != "sql":
        raise HTTPException(status_code=400, detail="This assignment is not a SQL problem")
    
    # Get all test cases for this assignment
    test_cases = db.query(TestCase).filter(
        TestCase.assignment_id == submission.assignment_id,
        TestCase.expected_result != None  # Only SQL test cases with expected results
    ).all()
    
    test_cases_data = [
        {
            "expected_result": tc.expected_result,
        }
        for tc in test_cases
    ]
    
    # Execute the SQL problem
    result = execute_sql_problem(
        schema_sql=assignment.sql_schema,
        user_query=submission.sql_query,
        test_cases=test_cases_data
    )
    
    return result

@router.post("/submit-code")
def submit_code(submission: CodeSubmission, db: Session = Depends(get_db)):
    """Submit and test code (Python/JavaScript)"""
    assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    if assignment.problem_type != "coding":
        raise HTTPException(status_code=400, detail="This assignment is not a coding problem")
    
    if not assignment.language:
        raise HTTPException(status_code=400, detail="Assignment language not specified")
    
    # Get all test cases for this assignment
    test_cases = db.query(TestCase).filter(
        TestCase.assignment_id == submission.assignment_id,
        TestCase.expected_output != None  # Only coding test cases
    ).all()
    
    test_cases_data = [
        {
            "input": tc.input or "",
            "expected_output": tc.expected_output,
        }
        for tc in test_cases
    ]
    
    # Execute the coding problem using Judge0 for Python, local for JavaScript
    if assignment.language.lower() == 'python':
        # Use Judge0 for Python execution
        result = Judge0Executor.execute_coding_problem(
            language='python',
            user_code=submission.code,
            test_cases=test_cases_data
        )
        return result
    elif assignment.language.lower() == 'javascript':
        # Use Piston API for JavaScript execution
        result = PistonExecutor.execute_coding_problem(
            user_code=submission.code,
            test_cases=test_cases_data
        )
        return result
    else:
        return {"success": False, "error": f"Unsupported language: {assignment.language}"}

@router.get("/{assignment_id}/stats")
def get_assignment_stats(assignment_id: int, db: Session = Depends(get_db)):
    total_submissions = db.query(Submission).filter(Submission.assignment_id == assignment_id).count()
    passed_submissions = db.query(Submission).filter(Submission.assignment_id == assignment_id, Submission.status == "pass").count()
    failed_submissions = db.query(Submission).filter(Submission.assignment_id == assignment_id, Submission.status == "fail").count()
    unique_submitters = db.query(Submission.user_id).filter(Submission.assignment_id == assignment_id).distinct().count()
    total_users = db.query(User).count()
    remaining = total_users - unique_submitters

    return {
        "total_submissions": total_submissions,
        "passed_submissions": passed_submissions,
        "failed_submissions": failed_submissions,
        "submitted": unique_submitters,
        "remaining": remaining
    }

@router.get("/completion-stats")
def get_completion_stats(db: Session = Depends(get_db)):
    return {"completion_stats": []}
