import streamlit as st
import pandas as pd

from app.models import get_items_counts

st.header("Total Item Counts")

# Get item counts
status = st.selectbox("Status", ["All", "Pending", "Fulfilled"])
item_counts = get_items_counts(status=status.lower())
if item_counts:
    df = pd.DataFrame(item_counts, columns=["Product", "Size", "Count"])
    pivot = pd.pivot_table(df, values="Count", index="Size", columns="Product", fill_value=0)
    st.write(pivot)
else:
    st.write("No items available.")


