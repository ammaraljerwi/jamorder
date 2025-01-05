import sqlite3

from app.config import DATABASE_PATH

# Create a connection to the database
def create_connection():
    return sqlite3.connect(DATABASE_PATH)

# Create the database schema
def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Create tables if they do not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OrderItems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            size TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES Orders(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            size TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()