from fastapi import APIRouter

router = APIRouter(prefix="/lambda", tags=["Lambda"])

@router.get("/ping")
def ping_lambda():
    return {"message": "Lambda Router Working"}
