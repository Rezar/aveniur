import streamlit as st
import warnings
import base64
from home import show_dashboard

# Suppress pyplot global use warning
st.set_option('deprecation.showPyplotGlobalUse', False)
warnings.filterwarnings("ignore")

# Function to encode images to base64
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Dummy credentials for demonstration purposes
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

def main():
    # Ignore all warnings
    st.logo("images/lavenir.PNG")
    warnings.filterwarnings("ignore")

    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if st.session_state['authenticated']:
        show_dashboard()  # Navigate to home if already authenticated
    else:
        set_background('./images/background.png')
        
        st.title("L'Avenir Holdings inc Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state['authenticated'] = True
                st.success("Login successful")
                st.experimental_rerun()  # Rerun to update the session state and navigate to home
            else:
                st.warning("Invalid username or password")

# def show_dashboard():
#     st.write("Welcome to the dashboard!")

if __name__ == "__main__":
    main()

# import streamlit as st
# from StreamlitGauth.google_auth import Google_auth
# import warnings

# st.logo("images/lavenir.PNG")

# def main():
#     # Ignore all warnings
#     warnings.filterwarnings("ignore")
    
#     client_id = "166960327947-gslpqkh5091ppc7paa4fj05sokjktv37.apps.googleusercontent.com"
#     client_secret = "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"
#     base_url = "http://localhost:8501/"
#     redirect_uri = base_url+"home"

#     login = Google_auth(clientId=client_id, clientSecret=client_secret, redirect_uri=redirect_uri)

#     # Initialize session state for authentication
#     if 'authenticated' not in st.session_state:
#         st.session_state['authenticated'] = False

#     if login == "authenticated":
#         st.session_state.authenticated = True
#         st.rerun()  # Rerun to update the session state and navigate to home
#     elif login == "login_failed":
#         st.warning("Login failed")
#         st.session_state.authenticated = False
#     else:
#         st.warning("Please Login..")

# if __name__ == "__main__":
#     main()


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