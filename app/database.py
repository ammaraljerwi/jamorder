from sqlalchemy import text
import streamlit as st

# Create a connection to the database
def create_connection():
    conn = st.connection("orders_db", type="sql")
    return conn

# Create the database schema
def init_db():
    conn = create_connection()
    with conn.session as cursor:
        # Create tables if they do not exist
        cursor.execute(text("""
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        )

        cursor.execute(text("""
            CREATE TABLE IF NOT EXISTS Orders (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                paid BOOLEAN NOT NULL DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES Users(id)
            )
        """))

        cursor.execute(text("""
            CREATE TABLE IF NOT EXISTS OrderItems (
                id SERIAL PRIMARY KEY,
                order_id INT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                size TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES Orders(id)
            )
        """))

        cursor.execute(
            text("""
                CREATE TABLE IF NOT EXISTS Products (
                    id SERIAL PRIMARY KEY,
                    product_name TEXT NOT NULL,
                    size TEXT NOT NULL
                    )
                """
                )
            )

        cursor.execute(
                text("""
                    CREATE TABLE IF NOT EXISTS Inventory (
                        id SERIAL PRIMARY KEY,
                        product_id INT NOT NULL,
                        quantity INT NOT NULL DEFAULT 0,
                        FOREIGN KEY (product_id) REFERENCES Products(id)
                        )
                    """)
                    )
        
        cursor.commit()
