from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.lambda_service import run_code
from app.models.submission import Submission

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.post("/run")
def run_submission(payload: dict, db: Session = Depends(get_db)):
    result = run_code(payload)

    submission = Submission(
        assignment_id=payload["assignment_id"],
        user_id=payload["user_id"],
        code=payload["code"],
        status="pass" if result["passed"] else "fail",
        output=str(result["results"]),
        score=100 if result["passed"] else 0
    )
    db.add(submission)
    db.commit()

    return {"result": result}
