import streamlit as st
import pandas as pd

from app.models import add_order, get_products
from app.controllers import add_item, adjust_item

st.header("Add a New Order")

# User name input
user_name = st.text_input("Customer Name")

# TODO: Refactor this into a function to display the order items
products_raw = get_products()
if not products_raw:
    st.error("No products available. Please add products in the 'Manage Products' section.")
    st.stop()

products = {}
for product, size in products_raw:
    if product not in products:
        products[product] = []
    products[product].append(size)

# Add order items
st.subheader("Order Items")
product = st.selectbox("Product", list(products.keys()))
quantity = st.number_input("Quantity", min_value=1, step=1)
size = st.selectbox("Size", products[product])

# Add item to order list
if "order_items" not in st.session_state:
    st.session_state["order_items"] = []

if st.button("Add Item"):
    st.session_state["order_items"] = add_item(st.session_state["order_items"], product, quantity, size)

# Display current items
st.write("### Current Items:")


for item in st.session_state["order_items"]:
    with st.container():
        cols = st.columns(2)
        cols[0].write(f"{item['quantity']}x {item['size']} {item['product']}")
        with cols[1]:
            quantity = st.number_input("Adjust Quantity", min_value=0, step=1, value=item['quantity'], key=(item['product'], item['size']))
            if quantity != item['quantity']:
                st.session_state["order_items"] = adjust_item(st.session_state["order_items"], item['product'], quantity, item['size'])
                st.rerun()


# Submit order
if st.button("Submit Order"):
    if user_name and st.session_state["order_items"]:
        add_order(user_name, st.session_state["order_items"])
        st.session_state["order_items"] = []
        st.success("Order submitted!")
    else:
        st.error("Please provide a customer name and at least one order item.")