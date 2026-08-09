import os
import ssl
from sqlalchemy import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:abc123.@localhost:3306/cv_generator"
)

connect_args = {}
if os.getenv("DB_SSL", "false").lower() == "true":
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ssl_context

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True, pool_recycle=280)