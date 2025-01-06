import streamlit as st

from app.database import init_db

st.title("Jam Order Tracker")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.write("## Login")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        if password == st.secrets["frontpage_password"]:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")

def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
# Initialize the database

if st.session_state.logged_in:
    init_db()
    pg = st.navigation(
        {"Logout": [logout_page],
         "Orders": [st.Page("app/pages/add_orders.py", title="Add Orders"),
                    st.Page("app/pages/manage_orders.py", title="Manage Orders")],
         "Products": [st.Page("app/pages/manage_products.py", title="Manage Products"),
                      st.Page("app/pages/manage_batch.py", title="Manage Batches"),
                      st.Page("app/pages/manage_inventory.py", title="Manage Inventory")],
         }
    )
else:
    pg = st.navigation({"Login": [login_page]})


pg.run()