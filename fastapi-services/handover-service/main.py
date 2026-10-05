from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI(
    title="Lost & Found - Handover Service",
    description="Handover management microservice",
    version="1.0.0"
)


def get_connection():
    return mysql.connector.connect(
        host="host.docker.internal",
        user="root",
        password="",
        database="college_lost_found"
    )


# 1. GET - All handovers
@app.get("/handovers")
def get_handovers():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, item_name, claimant_name,
               claimant_phone, status
        FROM items
        WHERE claimant_name IS NOT NULL
    """)

    handovers = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "count": len(handovers),
        "handovers": handovers
    }


# 2. GET - Handover details by item ID
@app.get("/handovers/{item_id}")
def get_handover(item_id: int):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, item_name, claimant_name,
               claimant_phone, status
        FROM items
        WHERE id = %s
        AND claimant_name IS NOT NULL
    """, (item_id,))

    handover = cursor.fetchone()

    cursor.close()
    conn.close()

    if handover is None:
        raise HTTPException(
            status_code=404,
            detail="Handover details not found"
        )

    return handover
