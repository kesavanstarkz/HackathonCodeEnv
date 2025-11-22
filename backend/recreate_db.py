from app.database import Base, engine
from app.models import User, Assignment, Submission, TestCase

# Drop all existing tables
Base.metadata.drop_all(bind=engine)
print("✅ Dropped all tables")

# Create all tables with correct schema
Base.metadata.create_all(bind=engine)
print("✅ Created all tables with correct schema")

print("\nTables created:")
print("- users")
print("- assignments")
print("- submissions")
print("- testcases")
