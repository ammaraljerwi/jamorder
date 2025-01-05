import streamlit as st

from app.database import init_db

st.title("Jam Order Tracker")

# Initialize the database
init_db()

pg = st.navigation([st.Page("app/pages/add_orders.py", title="Add Orders"),
                    st.Page("app/pages/manage_orders.py", title="Manage Orders"),
                    st.Page("app/pages/manage_products.py", title="Manage Products")])
pg.run()