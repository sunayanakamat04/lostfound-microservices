from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI(
    title="Lost & Found - User Service",
    description="User management microservice",
    version="1.0.0"
)


def get_connection():
    return mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="",
        database="college_lost_found"
    )


# Data model for creating a user
class UserCreate(BaseModel):
    fullname: str
    usn: str
    department: str
    email: str
    mobile: str
    password: str
    role: str = "student"


# 1. GET - All users
@app.get("/users")
def get_users():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, fullname
        FROM users
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "count": len(users),
        "users": users
    }


# 2. GET - User details by ID
@app.get("/users/{user_id}")
def get_user(user_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, fullname, usn, department,
               email, mobile, role, created_at
        FROM users
        WHERE id = %s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# 3. POST - Create a new user
@app.post("/users")
def create_user(user: UserCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users
        (fullname, usn, department, email, mobile, password, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user.fullname,
        user.usn,
        user.department,
        user.email,
        user.mobile,
        user.password,
        user.role
    ))

    conn.commit()

    new_user_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "message": "User created successfully",
        "user_id": new_user_id
    }
