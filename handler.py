"""
Handler module for PVC - Perfectly Viewable Cinemas
Contains all business logic and CSV operations.
"""
import csv
import os
from datetime import datetime


USERS_FILE = 'users.csv'
MOVIES_FILE = 'movies.csv'  # Movie catalog
SHOWINGS_FILE = 'showings.csv'  # Showings (movie in theatre)
THEATRES_FILE = 'theatres.csv'
BOOKINGS_FILE = 'bookings.csv'
ADMINS_FILE = 'admins.csv'

# --- CSV Operations ---
def initialize_csv_files():
    """Initialize CSV files with headers if they don't exist"""
    # Users CSV
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'username', 'password', 'email'])
            writer.writerow(['1', 'demo_user', 'password123', 'demo@email.com'])

    # Movies CSV
    if not os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['movie_id', 'title', 'genre', 'duration'])
            writer.writerow(['1', 'Avatar: The Way of Water', 'Sci-Fi', '192'])

    # Showings CSV
    if not os.path.exists(SHOWINGS_FILE):
        with open(SHOWINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['showing_id', 'movie_id', 'theatre_id', 'showtime', 'available_seats'])
            writer.writerow(['1', '1', '1', '18:00', '50'])

    # Theatres CSV
    if not os.path.exists(THEATRES_FILE):
        with open(THEATRES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['theatre_id', 'name', 'location', 'total_seats'])
            writer.writerow(['1', 'PVR Cinemas', 'Mall Road', '100'])

    # Bookings CSV
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['booking_id', 'user_id', 'showing_id', 'seats_booked', 'booking_date'])

    # Admins CSV
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['admin_id', 'username', 'password', 'type', 'theatre_id'])
            writer.writerow(['1', 'system_admin', 'admin123', 'system', ''])
            writer.writerow(['2', 'theatre_admin1', 'theatre123', 'theatre', '1'])
    print('Init complete.')

def read_csv_file(filename):
    data = []
    if os.path.exists(filename):
        with open(filename, 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def write_csv_file(filename, data, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# --- Authentication ---
def user_login(username, password):
    users = read_csv_file(USERS_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def admin_login(username, password):
    admins = read_csv_file(ADMINS_FILE)
    for admin in admins:
        if admin['username'] == username and admin['password'] == password:
            return admin
    return None

def register_user(username, password, email):
    users = read_csv_file(USERS_FILE)
    for user in users:
        if user['username'] == username:
            return False, "Username already exists!"
    new_id = str(len(users) + 1)
    users.append({'user_id': new_id, 'username': username, 'password': password, 'email': email})
    write_csv_file(USERS_FILE, users, ['user_id', 'username', 'password', 'email'])
    return True, "Registration successful!"

# --- Movie Operations ---

def get_movies():
    """Return movie catalog."""
    return read_csv_file(MOVIES_FILE)

def get_showings():
    """Return all showings."""
    return read_csv_file(SHOWINGS_FILE)

def get_theatres():
    return read_csv_file(THEATRES_FILE)

def add_movie(title, genre, duration):
    """Add a new movie to the catalog."""
    movies = read_csv_file(MOVIES_FILE)
    new_movie_id = str(len(movies) + 1)
    movies.append({'movie_id': new_movie_id, 'title': title, 'genre': genre, 'duration': duration})
    write_csv_file(MOVIES_FILE, movies, ['movie_id', 'title', 'genre', 'duration'])
    return True, f"Movie '{title}' added successfully!"

def del_movie(movie_id):
    """Delete a movie from the catalog."""
    movies = read_csv_file(MOVIES_FILE)
    for i in movies:
        if i['movie_id'] == movie_id:
            movies.remove(i)
            break
    write_csv_file(MOVIES_FILE, movies, ['movie_id', 'title', 'genre', 'duration'])
    showings = read_csv_file(SHOWINGS_FILE)
    showings = [s for s in showings if s['movie_id'] != movie_id]
    write_csv_file(SHOWINGS_FILE, showings, ['showing_id', 'movie_id', 'theatre_id', 'showtime', 'available_seats'])
    return True, f"Movie ID {movie_id} deleted successfully!"



def add_showing(movie_id, theatre_id, showtime, seats):
    """Add a new showing for a movie in a theatre."""
    showings = read_csv_file(SHOWINGS_FILE)
    new_showing_id = str(len(showings) + 1)
    showings.append({'showing_id': new_showing_id, 'movie_id': movie_id, 'theatre_id': theatre_id, 'showtime': showtime, 'available_seats': seats})
    write_csv_file(SHOWINGS_FILE, showings, ['showing_id', 'movie_id', 'theatre_id', 'showtime', 'available_seats'])
    return True, f"Showing added successfully!"

# --- Booking Operations ---

def book_ticket(user_id, showing_id, seats_wanted):
    showings = read_csv_file(SHOWINGS_FILE)
    selected_showing = None
    for showing in showings:
        if showing['showing_id'] == showing_id:
            selected_showing = showing
            break
    if not selected_showing:
        return False, "Showing not found!"
    available_seats = int(selected_showing['available_seats'])
    if seats_wanted > available_seats:
        return False, f"Only {available_seats} seats available!"
    selected_showing['available_seats'] = str(available_seats - seats_wanted)
    write_csv_file(SHOWINGS_FILE, showings, ['showing_id', 'movie_id', 'theatre_id', 'showtime', 'available_seats'])
    bookings = read_csv_file(BOOKINGS_FILE)
    new_booking_id = str(len(bookings) + 1)
    bookings.append({'booking_id': new_booking_id, 'user_id': user_id, 'showing_id': showing_id, 'seats_booked': str(seats_wanted), 'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    write_csv_file(BOOKINGS_FILE, bookings, ['booking_id', 'user_id', 'showing_id', 'seats_booked', 'booking_date'])
    return True, new_booking_id


def get_user_bookings(user_id):
    bookings = read_csv_file(BOOKINGS_FILE)
    return [b for b in bookings if b['user_id'] == user_id]

def get_theatre_bookings(theatre_id):
    showings = read_csv_file(SHOWINGS_FILE)
    theatre_showing_ids = [s['showing_id'] for s in showings if s['theatre_id'] == theatre_id]
    bookings = read_csv_file(BOOKINGS_FILE)
    return [b for b in bookings if b['showing_id'] in theatre_showing_ids]

def get_all_bookings():
    return read_csv_file(BOOKINGS_FILE)

def get_users():
    return read_csv_file(USERS_FILE)

def get_admins():
    return read_csv_file(ADMINS_FILE)
