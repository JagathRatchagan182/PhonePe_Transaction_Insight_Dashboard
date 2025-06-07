# db_connect.py

from sqlalchemy import create_engine

# Replace with your actual PostgreSQL credentials
USERNAME = 'postgres'
PASSWORD = 'Admin'
HOST = 'localhost'
PORT = '5432'
DATABASE = 'phonepe_db1'

# Creating the engine (connection string)
engine = create_engine(f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')
print("Connected to DB!")

