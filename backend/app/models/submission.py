from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    code = Column(String)
    status = Column(String)      # pass / fail
    output = Column(String)
    score = Column(Integer)
