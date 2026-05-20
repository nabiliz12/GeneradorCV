import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:abc123.@localhost:3306/cv_generator"
)

engine = create_engine(DATABASE_URL)