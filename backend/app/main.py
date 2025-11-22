from fastapi import FastAPI
from app.routers import auth, assignments, submissions, lambda_runner
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Code Assessment Backend")

app.include_router(auth.router)
app.include_router(assignments.router)
app.include_router(submissions.router)
app.include_router(lambda_runner.router)

@app.get("/")
def root():
    return {"message": "Backend is running!"}



origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)