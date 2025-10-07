import psycopg2
import os

# --- Database configuration from environment variables ---
DB_HOST = os.getenv("DB_HOST", "postgres-db")
DB_NAME = os.getenv("DB_NAME", "goalsdb")
DB_USER = os.getenv("DB_USER", "flaskuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "flaskpass")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    """Establish and return a PostgreSQL connection."""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def init_db():
    """Initialize the database and create the goals table if not exists."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            goal TEXT NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_goals():
    """Retrieve all goals."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, goal FROM goals")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "goal": r[1]} for r in rows]

def add_goal(goal_text):
    """Add a new goal."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO goals (goal) VALUES (%s)", (goal_text,))
    conn.commit()
    cursor.close()
    conn.close()

def delete_goal(goal_id):
    """Delete a goal by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = %s", (goal_id,))
    conn.commit()
    cursor.close()
    conn.close()