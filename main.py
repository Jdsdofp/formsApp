import streamlit as st
import streamlit_authenticator as stauth
from home import home_screen


names = ['admin']
usernames = ['admin']
passwords = ['123']

hashed_passwords = stauth.hasher(passwords).generate()

authenticator = stauth.authenticate(names, usernames, hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=30)


name, authentication_status = authenticator.login('Login','main')

if st.session_state['authentication_status']:
    home_screen()

elif st.session_state['authentication_status'] == False:
    st.error('Usuário/matricula incorreto')
