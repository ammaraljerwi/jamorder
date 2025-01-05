import streamlit as st

from app.models import add_product, get_products, remove_product

st.header("Manage Products")

# Add a product
st.subheader("Add Product")
new_product = st.text_input("Product Name")
new_size = st.selectbox("Size", ["4oz", "8oz", "16oz"])
if st.button("Add Product"):
    if new_product and new_size:
        add_product(new_product, new_size)
        st.success(f"Product {new_product} ({new_size}) added!")
    else:
        st.error("Please provide both a product name and a size.")

# Remove a product
st.subheader("Remove Product")
products = get_products()
if products:
    product_to_remove = st.selectbox("Select Product to Remove", [f"{p[0]} ({p[1]})" for p in products])
    if st.button("Remove Product"):
        product_name, size = product_to_remove.split(" (")
        size = size.strip(")")
        remove_product(product_name, size)
        st.success(f"Product {product_name} ({size}) removed!")
else:
    st.write("No products available.")

# Display current products
st.subheader("Current Products")
products = get_products()
if products:
    for product, size in products:
        st.write(f"- {product} ({size})")
else:
    st.write("No products available.")