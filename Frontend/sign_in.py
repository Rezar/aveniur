import streamlit as st
from StreamlitGauth.google_auth import Google_auth

def main():
    client_id = "CLIENT_ID"
    client_secret = "CLIENT_SECRET"
    redirect_uri = "http://localhost:8501/home.py"

    login = Google_auth(clientId=client_id, clientSecret=client_secret, redirect_uri=redirect_uri)

    if login == "authenticated":
        st.experimental_set_query_params(authenticated="true")
        st.rerun()
    else:
        st.warning("Login failed")

if __name__ == "__main__":
    main()

# import streamlit as st
# from StreamlitGauth.google_auth import Google_auth
# from home import home_content  # Importing the function to display the home content

# def main():
#     client_id = "166960327947-gslpqkh5091ppc7paa4fj05sokjktv37.apps.googleusercontent.com"
#     client_secret = "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"
#     redirect_uri = "http://localhost:8501"

#     # Initialize session state for authentication
#     if 'authenticated' not in st.session_state:
#         st.session_state['authenticated'] = False

#     login = Google_auth(clientId=client_id, clientSecret=client_secret, redirect_uri=redirect_uri)

#     if login == "authenticated":
#         # Go to home tab after successful authentication
#         st.query_params(tab="home")
#         st.query_params["page"] = "home"
#         st.success("Login Successful")
#         home_content()
#     else:
#         # st.warning("Login failed")
#         st.title("Sign In")
#         st.write("Please sign in using your Google account.")

# if __name__ == "__main__":
#     main()