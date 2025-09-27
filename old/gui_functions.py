import streamlit as st
import handler as handler
from datetime import datetime

def initialize_session_state():
    """Initialize session state variables."""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'selected_seats' not in st.session_state:
        st.session_state.selected_seats = {}
    if 'current_movie_selection' not in st.session_state:
        st.session_state.current_movie_selection = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Browse Movies"

def force_refresh_seat_data():
    """Clear any cached seat data to force refresh."""
    if 'seat_layout_cache' in st.session_state:
        del st.session_state.seat_layout_cache
    # Clear selected seats
    st.session_state.selected_seats = {}
    st.session_state.current_movie_selection = None

def login_page():
    """Display login page."""
    st.title("PVC - Cinema Management System")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted and username and password:
                success, user_info = handler.authenticate_user(username, password)
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
                if handler.register_user(new_username, new_password, email):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed. Username or email already exists.")

def user_interface():
    """Display user interface."""
    st.title("Movie Booking System")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        if st.button("Browse Movies", icon=":material/theaters:", use_container_width=True):
            st.session_state.current_page = "Browse Movies"
            st.rerun()
        if st.button("My Bookings", icon=":material/confirmation_number:", use_container_width=True):
            st.session_state.current_page = "My Bookings"
            st.rerun()
        
        st.markdown("---")
        if st.button("Logout", type="primary", icon=":material/logout:", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # Display the selected page
    if st.session_state.current_page == "Browse Movies":
        show_movies_page()
    elif st.session_state.current_page == "My Bookings":
        show_bookings_page()

def display_seat_selection(movie):
    """Display visual seat selection grid for a movie."""
    st.markdown("---")
    st.subheader(f":material/theater_comedy: Select Seats for: {movie['title']}")
    
    # Get seat layout information
    seat_layout = handler.get_seat_layout(movie['id'])
    if not seat_layout:
        st.error("Unable to load seat layout")
        return False
    
    # Generate seat grid
    seat_grid = handler.generate_seat_grid(
        seat_layout['total_seats'], 
        seat_layout['seats_per_row']
    )
    
    # Display seat information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Seats", seat_layout['available_count'])
    with col2:
        st.metric("Total Seats", seat_layout['total_seats'])
    with col3:
        st.metric("Price per Seat", f"${float(movie['price']):.2f}")
    
    # Legend
    st.markdown("#### Legend:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟢 **Available**")
    with col2:
        st.markdown("🔴 **Booked**")
    with col3:
        st.markdown("🟡 **Selected**")
    
    # Initialize selected seats for this movie if not exists
    movie_id = movie['id']
    if movie_id not in st.session_state.selected_seats:
        st.session_state.selected_seats[movie_id] = []
    
    # Display seat grid
    st.markdown("#### Select Your Seats:")
    selected_seats = st.session_state.selected_seats[movie_id].copy()
    
    for row_index, row in enumerate(seat_grid):
        # Create columns for the row - use max 10 seats plus row label
        max_seats_in_row = max(len(r) for r in seat_grid) if seat_grid else 10
        cols = st.columns([1] + [1] * max_seats_in_row)  # Row label + seats
        
        # Row label
        with cols[0]:
            st.markdown(f"**Row {chr(65 + row_index)}**")
        
        # Seats in this row
        for seat_index, seat_id in enumerate(row):
            with cols[seat_index + 1]:
                if seat_id == "":
                    # Empty placeholder for consistent grid
                    st.markdown("&nbsp;")
                else:
                    is_booked = seat_id in seat_layout['booked_seats']
                    is_selected = seat_id in selected_seats
                    
                    if is_booked:
                        # Show booked seat (disabled)
                        st.markdown("🔴")
                        st.caption(f"{seat_id}")
                        st.caption("Booked")
                    else:
                        # Show available seat with checkbox
                        checkbox_key = f"seat_{seat_id}_{movie_id}"
                        checked = st.checkbox(
                            seat_id,
                            value=is_selected,
                            key=checkbox_key,
                            label_visibility="hidden",
                            help=f"Select seat {seat_id}"
                        )
                        
                        # Update selected seats
                        if checked and seat_id not in selected_seats:
                            selected_seats.append(seat_id)
                        elif not checked and seat_id in selected_seats:
                            selected_seats.remove(seat_id)
                        
                        # Visual indicator
                        if checked:
                            st.markdown("🟡")
                        else:
                            st.markdown("🟢")
                        st.caption(f"{seat_id}")
    
    if st.button("Cancel", icon=":material/cancel:", key=f"cancel_{movie_id}"):
        force_refresh_seat_data()
        st.rerun()
    
    # Update session state
    st.session_state.selected_seats[movie_id] = selected_seats
    
    # Booking summary and actions
    if selected_seats:
        st.markdown("---")
        st.markdown("#### :material/assignment: Booking Summary")
        
        total_price = len(selected_seats) * float(movie['price'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Selected Seats:** {', '.join(selected_seats)}")
            st.write(f"**Number of Seats:** {len(selected_seats)}")
        with col2:
            st.write(f"**Total Price:** ${total_price:.2f}")
        
        # Booking buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Confirm Booking", type="primary", icon=":material/done_outline:", key=f"confirm_{movie_id}"):
                booking_id = handler.book_tickets_visual(
                    st.session_state.user['id'],
                    movie['id'],
                    selected_seats
                )
                
                if booking_id:
                    st.success(f"Booking successful! Booking ID: {booking_id}")
                    force_refresh_seat_data()
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Booking failed. Some seats may have been taken.")
        
        with col2:
            if st.button("Clear Selection", icon=":material/delete:", key=f"clear_{movie_id}"):
                st.session_state.selected_seats[movie_id] = []
                st.rerun()
    
    return True

def theatre_admin_interface():
    """Display theatre admin interface."""
    st.title("Theatre Admin Panel")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Add Movie/Showing", "Theatre Bookings"]
    )
    
    if page == "Add Movie/Showing":
        show_add_movie_page()
    elif page == "Theatre Bookings":
        show_theatre_bookings_page()
    
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

def show_movies_page():
    """Display movies page."""
    st.header("Available Movies and Showings")
    
    movies = handler.get_movies_showings()
    
    if not movies:
        st.info("No movies available at the moment.")
        return
    
    # Check if we're currently selecting seats for a movie
    if st.session_state.current_movie_selection:
        selected_movie = next(
            (m for m in movies if m['id'] == st.session_state.current_movie_selection), 
            None
        )
        if selected_movie:
            display_seat_selection(selected_movie)
            return
    
    # Display available movies
    for movie in movies:
        with st.expander(f"{movie['title']} - {movie['showtime']} | {movie['genre']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Genre:** {movie['genre']}")
                st.write(f"**Duration:** {movie['duration']} minutes")
                st.write(f"**Showtime:** {movie['showtime']}")
                st.write(f"**Available Seats:** {movie['available_seats']}")
                st.write(f"**Price:** ${float(movie['price']):.2f} per seat")
            
            with col2:
                if int(movie['available_seats']) > 0:
                    # Visual seat selection button
                    if st.button(
                        "Select Seats", 
                        key=f"visual_select_{movie['id']}",
                        type="primary",
                        icon=":material/comedy_mask:"
                    ):
                        st.session_state.current_movie_selection = movie['id']
                        st.rerun()
                    
                    # Traditional text input option (kept as fallback)
                    with st.expander(":material/text_snippet: Quick Text Entry"):
                        with st.form(f"booking_form_{movie['id']}"):
                            seats = st.text_input(
                                "Enter seat numbers (comma-separated, e.g., A1,A2)",
                                key=f"seats_{movie['id']}",
                                help="Use this for quick booking if you know the exact seat numbers"
                            )
                            if st.form_submit_button("Book Tickets"):
                                if seats:
                                    seat_list = [s.strip() for s in seats.split(',')]
                                    booking_id = handler.book_tickets(
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
                    st.write("This showing is fully booked.")

def show_bookings_page():
    """Display bookings page."""
    st.header("My Bookings")
    
    bookings = handler.get_user_bookings(st.session_state.user['id'])
    
    if not bookings:
        st.info("You have no bookings")
    else:
        for index, booking in enumerate(bookings):
            with st.expander(f"Booking #{index + 1} - ID: {booking['booking_id']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Booking ID:** {booking['booking_id']}")
                    st.write(f"**Movie ID:** {booking['showing_id']}")
                    st.write(f"**Seats:** {booking['seat_numbers']}")
                
                with col2:
                    st.write(f"**Total Price:** ${float(booking['total_price']):.2f}")
                    st.write(f"**Booking Date:** {booking['booking_date'][:19]}")
                
                # Unique button key using both index and booking ID
                button_key = f"cancel_booking_{index}_{booking['booking_id']}"
                
                if st.button("Cancel This Booking", key=button_key, type="secondary", icon=":material/delete:"):
                    success = handler.cancel_booking(
                        booking['booking_id'],
                        st.session_state.user['id']
                    )
                    
                    if success:
                        st.success("Booking cancelled successfully!")
                        force_refresh_seat_data()
                        st.rerun()
                    else:
                        st.error(f"Failed to cancel booking ID: {booking['booking_id']}")
                            
                st.markdown("---")

def show_add_movie_page():
    """Display add movie page."""
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
                if handler.add_movie_showing(
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

def show_theatre_bookings_page():
    """Display theatre bookings page."""
    st.header("Theatre Bookings")
    
    bookings = handler.get_theatre_bookings(st.session_state.user['theatre_id'])
    
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
    """Main application function."""
    # Set page configuration
    st.set_page_config(
        page_title="PVC Cinema Management",
        page_icon=":material/movie:",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .seat-available {
        background-color: #90EE90;
        border: 1px solid #006400;
        border-radius: 5px;
        padding: 5px;
        text-align: center;
        margin: 2px;
    }
    .seat-booked {
        background-color: #FF6B6B;
        border: 1px solid #8B0000;
        border-radius: 5px;
        padding: 5px;
        text-align: center;
        margin: 2px;
        color: white;
    }
    .seat-selected {
        background-color: #FFD700;
        border: 1px solid #FFA500;
        border-radius: 5px;
        padding: 5px;
        text-align: center;
        margin: 2px;
    }
    .stButton > button {
        width: 100%;
    }
    .movie-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)
def main():
    """Main application entry point."""
    # Initialize CSV files
    handler.ensure_csv_files_exist()
    
    # Configure page
    st.set_page_config(
        page_title="Perfectly Viewable Cinemas",
        page_icon="🎬",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Show appropriate interface based on login status
    if st.session_state.user is None:
        login_page()
    else:
        if st.session_state.user['type'] == 'user':
            user_interface()
        elif st.session_state.user['type'] == 'theatre':
            theatre_admin_interface()

if __name__ == "__main__":
    main()