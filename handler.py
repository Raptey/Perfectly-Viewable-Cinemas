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
    # ...existing code from main_old.py...
    pass

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
