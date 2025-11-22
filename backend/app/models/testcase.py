from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from app.database import Base

class TestCase(Base):
    __tablename__ = "testcases"

    id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    
    # For coding problems
    input = Column(Text, nullable=True)  # stdin input
    expected_output = Column(Text, nullable=True)  # expected stdout
    
    # For SQL problems
    sql_query = Column(Text, nullable=True)  # test SQL query
    expected_result = Column(Text, nullable=True)  # expected result (as JSON)
    
    hidden = Column(Boolean, default=False)  # hidden test case (not shown to user)

