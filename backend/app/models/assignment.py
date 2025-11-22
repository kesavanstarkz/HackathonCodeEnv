from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    domain = Column(String, nullable=False)  # fullstack / data / aiml
    difficulty = Column(String, nullable=False)  # easy, medium, hard
    problem_type = Column(String, default="coding")  # coding or sql
    
    # For coding problems
    language = Column(String, nullable=True)  # python or javascript
    test_input = Column(Text, nullable=True)
    expected_output = Column(Text, nullable=True)
    
    # For SQL problems
    sql_schema = Column(Text, nullable=True)  # SQL to create tables/schema
    sql_query = Column(Text, nullable=True)  # Expected SQL query solution (for reference)

