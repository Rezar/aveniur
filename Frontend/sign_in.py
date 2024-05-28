import streamlit as st
from StreamlitGauth.google_auth import Google_auth

def main():
    client_id = "CLIENT_ID"
    client_secret = "CLIENT_SECRET"
    redirect_uri = "http://localhost:8501/sign_in.py"  # Update the redirect URI to point to sign_in.py

    login = Google_auth(clientId=client_id, clientSecret=client_secret, redirect_uri=redirect_uri)

    if login == "authenticated":
        st.success("Login Successful")
        st.experimental_set_query_params(authenticated="true")
        st.experimental_rerun()
    else:
        st.warning("Login failed")

if __name__ == "__main__":
    main()
