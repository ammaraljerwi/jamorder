from sqlalchemy import text
from app.database import create_connection

# Add a product
def add_product(product_name, size):
    conn = create_connection()
    with conn.session as session:
        session.execute(
            text("INSERT INTO Products (product_name, size) VALUES (:product_name, :size)"),
            [{"product_name": product_name, "size": size}])
        session.commit()

# Remove a product
def remove_product(product_name, size):
    conn = create_connection()
    with conn.session as session:
        session.execute(
            text("DELETE FROM Products WHERE product_name = :product_name AND size = :size"), 
            [{"product_name": product_name, "size": size}])
        session.commit()

# Retrieve all products
def get_products():
    conn = create_connection()
    with conn.session as session:
        products = session.execute(text("SELECT product_name, size FROM Products")).fetchall()
    # products = conn.query("SELECT product_name, size FROM Products")
    # products = cursor.fetchall()
    # conn.close()
    return products

# Add a user
def add_user(name):
    conn = create_connection()
    with conn.session as session:
        session.execute(
            text("INSERT INTO Users (name) VALUES (:name)"),
            [{"name": name}])
        session.commit()

# Add an order and order items
def add_order(user_name, items):
    conn = create_connection()

    with conn.session as session:
        # Get or create user
        user = session.execute(
            text("SELECT id FROM Users WHERE name = :name"),
            [{"name": user_name}]).fetchone()
        if not user:
            add_user(user_name)
            user = session.execute(
                text("SELECT id FROM Users WHERE name = :name"),
                [{"name": user_name}]).fetchone()

        user_id = user[0]
        
        # Create order
        session.execute(
            text("INSERT INTO Orders (user_id) VALUES (:user_id)"),
            [{"user_id": user_id}])
        order_id = session.execute(text("SELECT lastval()")).fetchone()[0]

        # Add order items
        for item in items:
            session.execute(
                text("INSERT INTO OrderItems (order_id, product, quantity, size) VALUES (:order_id, :product, :quantity, :size)"),
                [{"order_id": order_id, "product": item['product'], "quantity": item['quantity'], "size": item['size']}])
        session.commit()

# Retrieve orders
VALID_STATUSES = ["pending", "fulfilled", "all"]
def get_orders(status="all"):
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")

    conn = create_connection()
    with conn.session as session:
        if status != "all":
            orders = session.execute(
                text("""
                    SELECT Orders.id, Users.name, Orders.status 
                    FROM Orders 
                    JOIN Users ON Orders.user_id = Users.id
                    WHERE Orders.status = :status
                """),
                [{"status": status}]).fetchall()
        else:
            orders = session.execute(
                text("""
                    SELECT Orders.id, Users.name, Orders.status 
                    FROM Orders 
                    JOIN Users ON Orders.user_id = Users.id
                """)).fetchall()

        # Retrieve order items for each order
        orders_with_items = []
        for order in orders:
            order_id, user_name, status = order
            items = session.execute(
                text("SELECT product, quantity, size FROM OrderItems WHERE order_id = :order_id"),
                [{"order_id": order_id}]).fetchall()
            orders_with_items.append((order_id, user_name, status, items))

    return orders_with_items

def get_items_counts(status="pending"):
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    
    conn = create_connection()
    with conn.session as session:
        if status != "all":
            items = session.execute(
                text("""
                    SELECT product, size, SUM(quantity) 
                    FROM OrderItems 
                    JOIN Orders ON OrderItems.order_id = Orders.id
                    WHERE Orders.status = :status
                    GROUP BY product, size
                """),
                [{"status": status}]).fetchall()
        else:
            items = session.execute(
                text("""
                    SELECT product, size, SUM(quantity) 
                    FROM OrderItems 
                    GROUP BY product, size
                """)).fetchall()
    
    return items


# Mark order as fulfilled
def fulfill_order(order_id):
    conn = create_connection()
    with conn.session as session:
        session.execute(
            text("UPDATE Orders SET status = 'fulfilled' WHERE id = :order_id"),
            [{"order_id": order_id}])
        session.commit()