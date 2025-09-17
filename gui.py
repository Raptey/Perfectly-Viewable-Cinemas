import streamlit as st
from handler import CinemaSystem
from datetime import datetime

class CinemaGUI:
    def __init__(self):
        self.system = CinemaSystem()
        if 'user' not in st.session_state:
            st.session_state.user = None

    def login_page(self):
        st.title("PVC - Cinema Management System")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted and username and password:
                    success, user_info = self.system.authenticate_user(username, password)
                    if success:
                        if user_info['type'] == 'system':
                            st.error("System admin must use CLI interface")
                        else:
                            st.session_state.user = user_info
                            st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                email = st.text_input("Email")
                submitted = st.form_submit_button("Register")
                
                if submitted and new_username and new_password and email:
                    if self.system.register_user(new_username, new_password, email):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Username or email already exists.")

    def user_interface(self):
        st.title("Movie Booking System")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Browse Movies", "My Bookings"]
        )
        
        if page == "Browse Movies":
            self.show_movies_page()
        elif page == "My Bookings":
            self.show_bookings_page()
        
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()

    def theatre_admin_interface(self):
        st.title("Theatre Admin Panel")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["Add Movie/Showing", "Theatre Bookings"]
        )
        
        if page == "Add Movie/Showing":
            self.show_add_movie_page()
        elif page == "Theatre Bookings":
            self.show_theatre_bookings_page()
        
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()

    def show_movies_page(self):
        st.header("Available Movies and Showings")
        
        movies = self.system.get_movies_showings()
        
        for movie in movies:
            with st.expander(f"{movie['title']} - {movie['showtime']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Genre: {movie['genre']}")
                    st.write(f"Duration: {movie['duration']} minutes")
                    st.write(f"Available Seats: {movie['available_seats']}")
                    st.write(f"Price: ${float(movie['price']):.2f}")
                
                with col2:
                    if int(movie['available_seats']) > 0:
                        with st.form(f"booking_form_{movie['id']}"):
                            seats = st.text_input(
                                "Enter seat numbers (comma-separated, e.g., A1,A2)",
                                key=f"seats_{movie['id']}"
                            )
                            if st.form_submit_button("Book Tickets"):
                                if seats:
                                    seat_list = [s.strip() for s in seats.split(',')]
                                    booking_id = self.system.book_tickets(
                                        st.session_state.user['id'],
                                        movie['id'],
                                        seat_list
                                    )
                                    if booking_id:
                                        st.success(f"Booking successful! Booking ID: {booking_id}")
                                        st.rerun()
                                    else:
                                        st.error("Booking failed. Seats might be taken or invalid.")
                                else:
                                    st.error("Please enter seat numbers")
                    else:
                        st.error("No seats available")

    def show_bookings_page(self):
        st.header("My Bookings")
        
        bookings = self.system.get_user_bookings(st.session_state.user['id'])
        
        if not bookings:
            st.info("You have no bookings")
        else:
            for booking in bookings:
                with st.expander(f"Booking ID: {booking['booking_id']}"):
                    st.write(f"Movie ID: {booking['showing_id']}")
                    st.write(f"Seats: {booking['seat_numbers']}")
                    st.write(f"Total Price: ${float(booking['total_price']):.2f}")
                    st.write(f"Booking Date: {booking['booking_date'][:19]}")
                    
                    if st.button("Cancel Booking", key=f"cancel_{booking['booking_id']}"):
                        if self.system.cancel_booking(
                            booking['booking_id'],
                            st.session_state.user['id']
                        ):
                            st.success("Booking cancelled successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to cancel booking")

    def show_add_movie_page(self):
        st.header("Add New Movie/Showing")
        
        with st.form("add_movie_form"):
            title = st.text_input("Movie Title")
            genre = st.text_input("Genre")
            duration = st.number_input("Duration (minutes)", min_value=1, value=90)
            showtime = st.text_input("Showtime (HH:MM)")
            seats = st.number_input("Number of Seats", min_value=1, value=50)
            price = st.number_input("Ticket Price ($)", min_value=0.0, value=10.0, step=0.5)
            
            if st.form_submit_button("Add Movie/Showing"):
                if all([title, genre, showtime]):
                    if self.system.add_movie_showing(
                        title, genre, duration,
                        st.session_state.user['theatre_id'],
                        showtime, seats, price
                    ):
                        st.success("Movie/Showing added successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to add movie/showing")
                else:
                    st.error("Please fill all fields")

    def show_theatre_bookings_page(self):
        st.header("Theatre Bookings")
        
        bookings = self.system.get_theatre_bookings(st.session_state.user['theatre_id'])
        
        if not bookings:
            st.info("No bookings for your theatre")
        else:
            # Calculate total revenue
            total_revenue = sum(float(b['total_price']) for b in bookings)
            st.metric("Total Revenue", f"${total_revenue:.2f}")
            
            for booking in bookings:
                with st.expander(f"Booking ID: {booking['booking_id']}"):
                    st.write(f"User ID: {booking['user_id']}")
                    st.write(f"Movie ID: {booking['showing_id']}")
                    st.write(f"Seats: {booking['seat_numbers']}")
                    st.write(f"Total Price: ${float(booking['total_price']):.2f}")
                    st.write(f"Booking Date: {booking['booking_date'][:19]}")

def main():
    gui = CinemaGUI()
    
    if st.session_state.user is None:
        gui.login_page()
    else:
        if st.session_state.user['type'] == 'user':
            gui.user_interface()
        elif st.session_state.user['type'] == 'theatre':
            gui.theatre_admin_interface()

if __name__ == '__main__':
    main()