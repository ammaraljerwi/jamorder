import streamlit as st

from app.models import get_orders, fulfill_order, order_paid

st.header("Manage Orders")
st.write("Use this section to manage pending orders.")
# Display orders
st.write("## Pending Orders")
orders = get_orders(status="pending")

cols = st.columns(3)
for i, (order_id, user_name, status, paid, items) in enumerate(orders):
    with cols[i % 3]:
        st.write(f"### Order {order_id}")
        st.write(f"**Customer:** {user_name}")
        st.write(f"**Paid:** {paid}")
        st.write("**Items:**")
        for product, quantity, size in items:
            st.write(f"- {quantity}x {size} {product}")
        if st.button(f"Mark Order {order_id} as Fulfilled"):
            fulfill_order(order_id)
            st.success(f"Order {order_id} marked as fulfilled.")
        if not paid:
            if st.button(f"Mark Order {order_id} as Paid"):
                order_paid(order_id)
                st.success(f"Order {order_id} marked as paid.")

st.write("## Fulfilled Orders")
orders = get_orders(status="fulfilled")

cols = st.columns(3)
for i, (order_id, user_name, status, paid, items) in enumerate(orders):
    with cols[i % 3]:
        st.write(f"### Order {order_id}")
        st.write(f"**Customer:** {user_name}")
        st.write(f"**Paid:** {paid}")
        st.write("**Items:**")
        for product, quantity, size in items:
            st.write(f"- {quantity}x {size} {product}")
        if not paid:
            if st.button(f"Mark Order {order_id} as Paid"):
                order_paid(order_id)
                st.success(f"Order {order_id} marked as paid.")
