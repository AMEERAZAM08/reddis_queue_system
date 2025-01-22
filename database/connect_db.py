import psycopg2
from psycopg2.extras import DictCursor
import os

# Database parameters from environment variables
db_params = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

def get_db_connection():
    return psycopg2.connect(**db_params, cursor_factory=DictCursor)
