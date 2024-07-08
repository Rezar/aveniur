import streamlit as st
import warnings

st.logo("images/lavenir.PNG")

# Dummy credentials for demonstration purposes
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def main():
    # Ignore all warnings
    warnings.filterwarnings("ignore")

    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        st.experimental_rerun()  # Rerun to navigate to home if already authenticated
    else:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state['authenticated'] = True
                st.success("Login successful")
                st.experimental_rerun()  # Rerun to update the session state and navigate to home
            else:
                st.warning("Invalid username or password")

if __name__ == "__main__":
    main()
