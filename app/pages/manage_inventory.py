import streamlit as st

from app.models import get_inventory, adjust_inventory

st.header("Manage Inventory")

# Current inventory
st.subheader("Current Inventory")
inventory = get_inventory()

if inventory:
    for product, size, quantity in inventory:
        with st.container():
            cols = st.columns(2)
            cols[0].write(f"{quantity}x {size} {product}")
            with cols[1]:
                new_quantity = st.number_input("Adjust Quantity", min_value=0, step=1, value=quantity, key=(product, size))
                if new_quantity != quantity:
                    adjust_inventory(product, size, new_quantity)
                    st.rerun()
