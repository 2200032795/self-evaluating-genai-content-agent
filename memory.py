import sqlite3
import json
from datetime import datetime

DB_PATH = "data/agent_memory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_memory():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS run_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            final_status TEXT,
            total_attempts INTEGER,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS failure_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            criterion TEXT,
            failure_reason TEXT,
            created_at TEXT
        )
    """)

    connection.commit()
    connection.close()

    print("Persistent memory initialized!")


def save_run(topic, final_status, total_attempts, rejection_log):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO run_history
        (topic, final_status, total_attempts, created_at)
        VALUES (?, ?, ?, ?)
    """, (
        topic,
        final_status,
        total_attempts,
        datetime.now().isoformat()
    ))

    for rejected in rejection_log:

        for criterion, details in rejected["checks"].items():

            if details["status"] == "FAIL":

                cursor.execute("""
                    INSERT INTO failure_memory
                    (topic, criterion, failure_reason, created_at)
                    VALUES (?, ?, ?, ?)
                """, (
                    topic,
                    criterion,
                    details["reason"],
                    datetime.now().isoformat()
                ))

    connection.commit()
    connection.close()

    print("Run history and failure memory saved!")


def get_previous_feedback(topic):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT criterion, failure_reason
        FROM failure_memory
        WHERE topic = ?
        ORDER BY id DESC
        LIMIT 10
    """, (topic,))

    records = cursor.fetchall()
    connection.close()

    if not records:
        return None

    feedback = "\n".join(
        f"- Improve {criterion}: {reason}"
        for criterion, reason in records
    )

    return feedback


if __name__ == "__main__":

    initialize_memory()

    print("\nMemory system is ready!")
