import streamlit as st

from app.models import get_orders, fulfill_order

st.header("Manage Orders")

# Display orders
orders = get_orders()
for order_id, user_name, status, items in orders:
    st.write(f"### Order {order_id} ({status})")
    st.write(f"**Customer:** {user_name}")
    st.write("**Items:**")
    for product, quantity, size in items:
        st.write(f"- {quantity}x {size} {product}")

    # Fulfill order button
    if status == "pending":
        if st.button(f"Mark Order {order_id} as Fulfilled"):
            fulfill_order(order_id)
            st.success(f"Order {order_id} marked as fulfilled.")