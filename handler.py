#!/usr/bin/env python3
"""
Funvtion handler file
"""
import csv
import os
from datetime import datetime
import sys

# Global variables for file paths
USERS_FILE = 'users.csv'
MOVIES_FILE = 'movies.csv'
THEATRES_FILE = 'theatres.csv'
BOOKINGS_FILE = 'bookings.csv'
ADMINS_FILE = 'admins.csv'

# Current logged-in user
current_user = None
current_user_type = None

def initialize_csv_files():
    """Initialize CSV files with headers if they don't exist"""
    
    # Users CSV
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'username', 'password', 'email'])
            # Add a demo user
            writer.writerow(['1', 'demo_user', 'password123', 'demo@email.com'])
    
    # Movies CSV
    if not os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['movie_id', 'title', 'genre', 'duration', 'theatre_id', 'showtime', 'available_seats'])
            # Add demo movies
            writer.writerow(['1', 'Avatar: The Way of Water', 'Sci-Fi', '192', '1', '18:00', '50'])
            writer.writerow(['2', 'Top Gun: Maverick', 'Action', '131', '1', '21:00', '45'])
            writer.writerow(['3', 'The Batman', 'Action', '176', '2', '19:30', '60'])
    
    # Theatres CSV
    if not os.path.exists(THEATRES_FILE):
        with open(THEATRES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['theatre_id', 'name', 'location', 'total_seats'])
            writer.writerow(['1', 'PVR Cinemas', 'Mall Road', '100'])
            writer.writerow(['2', 'INOX Theatre', 'City Center', '120'])
    
    # Bookings CSV
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['booking_id', 'user_id', 'movie_id', 'theatre_id', 'seats_booked', 'booking_date'])
    
    # Admins CSV
    if not os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['admin_id', 'username', 'password', 'type', 'theatre_id'])
            # Add demo admins
            writer.writerow(['1', 'system_admin', 'admin123', 'system', ''])
            writer.writerow(['2', 'theatre_admin1', 'theatre123', 'theatre', '1'])
    # print('Init complete.')

def read_csv_file(filename):
    """Read CSV file and return list of dictionaries"""
    data = []
    if os.path.exists(filename):
        with open(filename, 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
    return data

def write_csv_file(filename, data, fieldnames):
    """Write data to CSV file"""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# User login handler
def user_login(username, password):

    global current_user, current_user_type 
    users = read_csv_file(USERS_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            current_user = user # IS IN FORM [user_id,username,password,email]
            current_user_type = 'user'
            # print(f"Welcome, {username}!")
            return True
    
    # print("Invalid credentials!")
    return False

# Admin login handler
def admin_login(username, password):

    global current_user, current_user_type
    
    admins = read_csv_file(ADMINS_FILE)
    for admin in admins:
        if admin['username'] == username and admin['password'] == password:
            current_user = admin
            current_user_type = admin['type']
            #print(f"Welcome, {username}! ({admin['type']} admin)")
            return True
    
    #print("Invalid admin credentials!")
    return False

# Registration Handler
def register_user(username, password, email):
    
    users = read_csv_file(USERS_FILE)
    
    # Check if username already exists
    for user in users:
        if user['username'] == username:
            # print("Username already exists!")
            return False
    
    # Generate new user ID
    new_id = str(len(users) + 1)
    
    # Add new user
    users.append({
        'user_id': new_id,
        'username': username,
        'password': password,
        'email': email
    })
    
    write_csv_file(USERS_FILE, users, ['user_id', 'username', 'password', 'email'])
    # print("Registration successful!")
    return True

# movie list display handler
def view_movies():

    movies = read_csv_file(MOVIES_FILE)
    theatres = read_csv_file(THEATRES_FILE)
    
    if not movies:
        # print("No movies available.")
        return False
    
    """
    # Create theatre lookup
    theatre_lookup = {t['theatre_id']: t['name'] for t in theatres}
    
    print(f"{'ID':<3} {'Title':<25} {'Genre':<12} {'Duration':<8} {'Theatre':<15} {'Showtime':<8} {'Seats':<5}")
    print("-" * 85)
    
    for movie in movies:
        theatre_name = theatre_lookup.get(movie['theatre_id'], 'Unknown')
        print(f"{movie['movie_id']:<3} {movie['title'][:24]:<25} {movie['genre']:<12} {movie['duration']+'m':<8} {theatre_name:<15} {movie['showtime']:<8} {movie['available_seats']:<5}")
    """

# booking handler
def book_ticket(movie_id, seats_wanted):

    # Check user type before starting booking process
    if not current_user or current_user_type != 'user':
        # print("Please login as a user first!")
        return
    
    # view_movies()
    
    try:
        seats_wanted = int(seats_wanted)
    except ValueError:
        return False
    
    movies = read_csv_file(MOVIES_FILE)
    selected_movie = None
    
    for movie in movies:
        if movie['movie_id'] == movie_id:
            selected_movie = movie
            break
    
    if not selected_movie:
        # print("Movie not found!")
        return False
    
    available_seats = int(selected_movie['available_seats'])
    
    #if seats_wanted > available_seats:
        # print(f"Only {available_seats} seats available!")
    #    return
    
    # Update available seats
    selected_movie['available_seats'] = str(available_seats - seats_wanted)
    write_csv_file(MOVIES_FILE, movies, ['movie_id', 'title', 'genre', 'duration', 'theatre_id', 'showtime', 'available_seats'])
    
    # Add booking record
    bookings = read_csv_file(BOOKINGS_FILE)
    new_booking_id = str(len(bookings) + 1)
    
    bookings.append({
        'booking_id': new_booking_id,
        'user_id': current_user['user_id'],
        'movie_id': movie_id,
        'theatre_id': selected_movie['theatre_id'],
        'seats_booked': str(seats_wanted),
        'booking_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    write_csv_file(BOOKINGS_FILE, bookings, ['booking_id', 'user_id', 'movie_id', 'theatre_id', 'seats_booked', 'booking_date'])
    
    print(f"\nBooking successful! Booking ID: {new_booking_id}")
    print(f"Movie: {selected_movie['title']}")
    print(f"Seats: {seats_wanted}")
    print(f"Showtime: {selected_movie['showtime']}")

