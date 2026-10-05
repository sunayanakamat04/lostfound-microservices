from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI(
    title="Lost & Found - Item Service",
    description="Lost and found item management microservice",
    version="1.0.0"
)


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="college_lost_found"
    )


# Data model for creating an item
class ItemCreate(BaseModel):
    item_name: str
    description: str
    location: str
    reporter_name: str
    reporter_phone: str
    report_type: str
    status: str = "open"


# 1. GET - All items
@app.get("/items")
def get_items():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, item_name, location,
               report_type, status
        FROM items
    """)

    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "count": len(items),
        "items": items
    }


# 2. GET - Item details by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM items
        WHERE id = %s
    """, (item_id,))

    item = cursor.fetchone()

    cursor.close()
    conn.close()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


# 3. POST - Create a new item
@app.post("/items")
def create_item(item: ItemCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO items
        (item_name, description, location,
         reporter_name, reporter_phone,
         report_type, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        item.item_name,
        item.description,
        item.location,
        item.reporter_name,
        item.reporter_phone,
        item.report_type,
        item.status
    ))

    conn.commit()

    new_item_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return {
        "message": "Item created successfully",
        "item_id": new_item_id
    }