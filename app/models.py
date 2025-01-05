from app.database import create_connection

# Add a product
def add_product(product_name, size):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Products (product_name, size) VALUES (?, ?)", (product_name, size))
    conn.commit()
    conn.close()

# Remove a product
def remove_product(product_name, size):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Products WHERE product_name = ? AND size = ?", (product_name, size))
    conn.commit()
    conn.close()

# Retrieve all products
def get_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_name, size FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products

# Add a user
def add_user(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

# Add an order and order items
def add_order(user_name, items):
    conn = create_connection()
    cursor = conn.cursor()

    # Get or create user
    cursor.execute("SELECT id FROM Users WHERE name = ?", (user_name,))
    user = cursor.fetchone()
    if not user:
        add_user(user_name)
        cursor.execute("SELECT id FROM Users WHERE name = ?", (user_name,))
        user = cursor.fetchone()

    user_id = user[0]
    
    # Create order
    cursor.execute("INSERT INTO Orders (user_id) VALUES (?)", (user_id,))
    order_id = cursor.lastrowid

    # Add order items
    for item in items:
        cursor.execute(
            "INSERT INTO OrderItems (order_id, product, quantity, size) VALUES (?, ?, ?, ?)",
            (order_id, item['product'], item['quantity'], item['size'])
        )

    conn.commit()
    conn.close()

# Retrieve orders
def get_orders():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Orders.id, Users.name, Orders.status 
        FROM Orders 
        JOIN Users ON Orders.user_id = Users.id
    """)
    orders = cursor.fetchall()

    # Retrieve order items for each order
    orders_with_items = []
    for order in orders:
        order_id, user_name, status = order
        cursor.execute("SELECT product, quantity, size FROM OrderItems WHERE order_id = ?", (order_id,))
        items = cursor.fetchall()
        orders_with_items.append((order_id, user_name, status, items))

    conn.close()
    return orders_with_items

def get_pending_orders():
    conn = create_connection()
    cursor = conn.cursor()
    
# Mark order as fulfilled
def fulfill_order(order_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Orders SET status = 'fulfilled' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()