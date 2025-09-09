"""
Streamlit UI for PVC - Perfectly Viewable Cinemas
Imports business logic from handler.py
Allows viewing and editing CSV data.
"""
import streamlit as st
import pandas as pd
from handler import *

st.set_page_config(page_title="PVC Cinemas", layout="wide")
st.title("Perfectly Viewable Cinemas")

menu = ["Login", "Register", "Movies", "Book Ticket", "My Bookings", "Admin: Movies", "Admin: Bookings",]
tabs = st.tabs(menu)

with tabs[0]:
    st.header("User/Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_type = st.radio("Login as", ["User", "Admin"])
    if st.button("Login"):
        if login_type == "User":
            user = user_login(username, password)
            if user:
                st.success(f"Welcome, {username}!")
                st.session_state['user'] = user
                st.session_state['user_type'] = 'user'
            else:
                st.error("Invalid credentials!")
        else:
            admin = admin_login(username, password)
            if admin:
                st.success(f"Welcome, {username}! ({admin['type']} admin)")
                st.session_state['user'] = admin
                st.session_state['user_type'] = admin['type']
            else:
                st.error("Invalid admin credentials!")

with tabs[1]:
    st.header("User Registration")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    email = st.text_input("Email")
    if st.button("Register"):
        success, msg = register_user(username, password, email)
        if success:
            st.success(msg)
        else:
            st.error(msg)

with tabs[2]:
    st.header("Available Movies")
    movies = get_movies()
    showings = get_showings()
    theatres = get_theatres()
    if showings:
        df = pd.DataFrame(showings)
        df['Movie'] = df['movie_id'].map({m['movie_id']: m['title'] for m in movies})
        df['Theatre'] = df['theatre_id'].map({t['theatre_id']: t['name'] for t in theatres})
        st.dataframe(df)
    else:
        st.info("No showings available.")

with tabs[3]:
    st.header("Book a Ticket")
    user = st.session_state.get('user', None)
    if not user or st.session_state.get('user_type') != 'user':
        st.warning("Please login as a user first!")
    else:
        showings = get_showings()
        movies = get_movies()
        showing_titles = [f"{m['title']} - {s['showtime']} (ID: {s['showing_id']})" for s in showings for m in movies if m['movie_id'] == s['movie_id']]
        selected = st.selectbox("Select Showing", showing_titles)
        seats_wanted = st.number_input("Number of seats", min_value=1, value=1)
        if st.button("Book"):
            showing_id = selected.split("ID: ")[-1].replace(")", "")
            success, result = book_ticket(user['user_id'], showing_id, seats_wanted)
            if success:
                st.success(f"Booking successful! Booking ID: {result}")
            else:
                st.error(result)

with tabs[4]:
    st.header("My Bookings")
    user = st.session_state.get('user', None)
    if not user or st.session_state.get('user_type') != 'user':
        st.warning("Please login as a user first!")
    else:
        bookings = get_user_bookings(user['user_id'])
        df = pd.DataFrame(bookings)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No bookings found.")

with tabs[5]:
    st.header("Admin: Add Showing")
    admin = st.session_state.get('user', None)
    if not admin or st.session_state.get('user_type') != 'theatre':
        st.warning("Theatre admin login required.")
    else:
        movies = get_movies()
        movie_titles = [f"{m['title']} (ID: {m['movie_id']})" for m in movies]
        selected = st.selectbox("Select Movie", movie_titles)
        showtime = st.text_input("Showtime (HH:MM)")
        seats = st.text_input("Available Seats")
        if st.button("Add Showing"):
            movie_id = selected.split("ID: ")[-1].replace(")", "")
            success, msg = add_showing(movie_id, admin['theatre_id'], showtime, seats)
            if success:
                st.success(msg)
            else:
                st.error(msg)

with tabs[6]:
    st.header("Admin: Theatre Bookings")
    admin = st.session_state.get('user', None)
    if not admin or st.session_state.get('user_type') != 'theatre':
        st.warning("Theatre admin login required.")
    else:
        bookings = get_theatre_bookings(admin['theatre_id'])
        df = pd.DataFrame(bookings)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No bookings found for this theatre.")

