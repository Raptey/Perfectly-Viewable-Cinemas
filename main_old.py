#!/usr/bin/env python3
"""
PVC - Perfectly Viewable Cinemas
A simple movie booking system using procedural programming
Command Line Interface Demo
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
    print('Init complete.')

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

def user_login():
    """Handle user login"""
    global current_user, current_user_type
    
    print("\n=== USER LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")
    
    users = read_csv_file(USERS_FILE)
    for user in users:
        if user['username'] == username and user['password'] == password:
            current_user = user
            current_user_type = 'user'
            print(f"Welcome, {username}!")
            return True
    
    print("Invalid credentials!")
    return False

def admin_login():
    """Handle admin login"""
    global current_user, current_user_type
    
    print("\n=== ADMIN LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")
    
    admins = read_csv_file(ADMINS_FILE)
    for admin in admins:
        if admin['username'] == username and admin['password'] == password:
            current_user = admin
            current_user_type = admin['type']
            print(f"Welcome, {username}! ({admin['type']} admin)")
            return True
    
    print("Invalid admin credentials!")
    return False

def register_user():
    """Register a new user"""
    print("\n=== USER REGISTRATION ===")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    
    users = read_csv_file(USERS_FILE)
    
    # Check if username already exists
    for user in users:
        if user['username'] == username:
            print("Username already exists!")
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
    print("Registration successful!")
    return True

def view_movies():
    """View available movies"""
    print("\n=== AVAILABLE MOVIES ===")
    movies = read_csv_file(MOVIES_FILE)
    theatres = read_csv_file(THEATRES_FILE)
    
    if not movies:
        print("No movies available.")
        return
    
    # Create theatre lookup
    theatre_lookup = {t['theatre_id']: t['name'] for t in theatres}
    
    print(f"{'ID':<3} {'Title':<25} {'Genre':<12} {'Duration':<8} {'Theatre':<15} {'Showtime':<8} {'Seats':<5}")
    print("-" * 85)
    
    for movie in movies:
        theatre_name = theatre_lookup.get(movie['theatre_id'], 'Unknown')
        print(f"{movie['movie_id']:<3} {movie['title'][:24]:<25} {movie['genre']:<12} {movie['duration']+'m':<8} {theatre_name:<15} {movie['showtime']:<8} {movie['available_seats']:<5}")

def book_ticket():
    """Book a movie ticket"""
    if not current_user or current_user_type != 'user':
        print("Please login as a user first!")
        return
    
    print("\n=== BOOK TICKET ===")
    view_movies()
    
    movie_id = input("\nEnter Movie ID to book: ")
    seats_wanted = input("Number of seats: ")
    
    try:
        seats_wanted = int(seats_wanted)
    except ValueError:
        print("Invalid number of seats!")
        return
    
    movies = read_csv_file(MOVIES_FILE)
    selected_movie = None
    
    for movie in movies:
        if movie['movie_id'] == movie_id:
            selected_movie = movie
            break
    
    if not selected_movie:
        print("Movie not found!")
        return
    
    available_seats = int(selected_movie['available_seats'])
    
    if seats_wanted > available_seats:
        print(f"Only {available_seats} seats available!")
        return
    
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

def view_user_bookings():
    """View current user's booking history"""
    if not current_user or current_user_type != 'user':
        print("Please login as a user first!")
        return
    
    print("\n=== YOUR BOOKINGS ===")
    bookings = read_csv_file(BOOKINGS_FILE)
    movies = read_csv_file(MOVIES_FILE)
    theatres = read_csv_file(THEATRES_FILE)
    
    user_bookings = [b for b in bookings if b['user_id'] == current_user['user_id']]
    
    if not user_bookings:
        print("No bookings found.")
        return
    
    # Create lookups
    movie_lookup = {m['movie_id']: m['title'] for m in movies}
    theatre_lookup = {t['theatre_id']: t['name'] for t in theatres}
    
    print(f"{'Booking ID':<10} {'Movie':<25} {'Theatre':<15} {'Seats':<5} {'Date':<19}")
    print("-" * 80)
    
    for booking in user_bookings:
        movie_title = movie_lookup.get(booking['movie_id'], 'Unknown')
        theatre_name = theatre_lookup.get(booking['theatre_id'], 'Unknown')
        print(f"{booking['booking_id']:<10} {movie_title[:24]:<25} {theatre_name:<15} {booking['seats_booked']:<5} {booking['booking_date']:<19}")

def add_movie():
    """Theatre admin function to add a movie"""
    if not current_user or current_user_type != 'theatre':
        print("Access denied! Theatre admin login required.")
        return
    
    print("\n=== ADD MOVIE ===")
    title = input("Movie Title: ")
    genre = input("Genre: ")
    duration = input("Duration (minutes): ")
    showtime = input("Showtime (HH:MM): ")
    seats = input("Available Seats: ")
    
    movies = read_csv_file(MOVIES_FILE)
    new_movie_id = str(len(movies) + 1)
    
    movies.append({
        'movie_id': new_movie_id,
        'title': title,
        'genre': genre,
        'duration': duration,
        'theatre_id': current_user['theatre_id'],
        'showtime': showtime,
        'available_seats': seats
    })
    
    write_csv_file(MOVIES_FILE, movies, ['movie_id', 'title', 'genre', 'duration', 'theatre_id', 'showtime', 'available_seats'])
    print(f"Movie '{title}' added successfully!")

def view_theatre_bookings():
    """Theatre admin function to view all bookings for their theatre"""
    if not current_user or current_user_type != 'theatre':
        print("Access denied! Theatre admin login required.")
        return
    
    print(f"\n=== BOOKINGS FOR THEATRE {current_user['theatre_id']} ===")
    bookings = read_csv_file(BOOKINGS_FILE)
    movies = read_csv_file(MOVIES_FILE)
    users = read_csv_file(USERS_FILE)
    
    theatre_bookings = [b for b in bookings if b['theatre_id'] == current_user['theatre_id']]
    
    if not theatre_bookings:
        print("No bookings found for this theatre.")
        return
    
    # Create lookups
    movie_lookup = {m['movie_id']: m['title'] for m in movies}
    user_lookup = {u['user_id']: u['username'] for u in users}
    
    print(f"{'Booking ID':<10} {'User':<15} {'Movie':<25} {'Seats':<5} {'Date':<19}")
    print("-" * 80)
    
    for booking in theatre_bookings:
        movie_title = movie_lookup.get(booking['movie_id'], 'Unknown')
        username = user_lookup.get(booking['user_id'], 'Unknown')
        print(f"{booking['booking_id']:<10} {username:<15} {movie_title[:24]:<25} {booking['seats_booked']:<5} {booking['booking_date']:<19}")

def system_admin_stats():
    """System admin function to view system statistics"""
    if not current_user or current_user_type != 'system':
        print("Access denied! System admin login required.")
        return
    
    print("\n=== SYSTEM STATISTICS ===")
    
    users = read_csv_file(USERS_FILE)
    movies = read_csv_file(MOVIES_FILE)
    theatres = read_csv_file(THEATRES_FILE)
    bookings = read_csv_file(BOOKINGS_FILE)
    
    print(f"Total Users: {len(users)}")
    print(f"Total Movies: {len(movies)}")
    print(f"Total Theatres: {len(theatres)}")
    print(f"Total Bookings: {len(bookings)}")
    
    # Calculate total revenue (assuming $10 per ticket)
    total_tickets = sum(int(b['seats_booked']) for b in bookings)
    total_revenue = total_tickets * 10
    print(f"Total Tickets Sold: {total_tickets}")
    print(f"Estimated Revenue: ${total_revenue}")

def user_menu():
    """Display user menu and handle user actions"""
    while True:
        print("\n=== USER MENU ===")
        print("1. View Available Movies")
        print("2. Book Ticket")
        print("3. View My Bookings")
        print("4. Logout")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            view_movies()
        elif choice == '2':
            book_ticket()
        elif choice == '3':
            view_user_bookings()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice!")

def theatre_admin_menu():
    """Display theatre admin menu and handle actions"""
    while True:
        print("\n=== THEATRE ADMIN MENU ===")
        print("1. View Available Movies")
        print("2. Add Movie")
        print("3. View Theatre Bookings")
        print("4. Logout")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            view_movies()
        elif choice == '2':
            add_movie()
        elif choice == '3':
            view_theatre_bookings()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice!")

def system_admin_menu():
    """Display system admin menu and handle actions"""
    while True:
        print("\n=== SYSTEM ADMIN MENU ===")
        print("1. View System Statistics")
        print("2. View All Movies")
        print("3. View All Bookings")
        print("4. Logout")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '1':
            system_admin_stats()
        elif choice == '2':
            view_movies()
        elif choice == '3':
            view_all_bookings()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice!")

def view_all_bookings():
    """System admin function to view all bookings"""
    print("\n=== ALL BOOKINGS ===")
    bookings = read_csv_file(BOOKINGS_FILE)
    movies = read_csv_file(MOVIES_FILE)
    users = read_csv_file(USERS_FILE)
    theatres = read_csv_file(THEATRES_FILE)
    
    if not bookings:
        print("No bookings found.")
        return
    
    # Create lookups
    movie_lookup = {m['movie_id']: m['title'] for m in movies}
    user_lookup = {u['user_id']: u['username'] for u in users}
    theatre_lookup = {t['theatre_id']: t['name'] for t in theatres}
    
    print(f"{'ID':<4} {'User':<12} {'Movie':<20} {'Theatre':<12} {'Seats':<5} {'Date':<19}")
    print("-" * 75)
    
    for booking in bookings:
        movie_title = movie_lookup.get(booking['movie_id'], 'Unknown')
        username = user_lookup.get(booking['user_id'], 'Unknown')
        theatre_name = theatre_lookup.get(booking['theatre_id'], 'Unknown')
        print(f"{booking['booking_id']:<4} {username:<12} {movie_title[:19]:<20} {theatre_name[:11]:<12} {booking['seats_booked']:<5} {booking['booking_date']:<19}")

def logout():
    """Logout current user"""
    global current_user, current_user_type
    print("Logged out successfully!")
    current_user = None
    current_user_type = None

def main():
    """Main function to run the PVC system"""
    print("=" * 50)
    print("    Welcome to PVC - Perfectly Viewable Cinemas")
    print("=" * 50)
    
    while True:
        if not current_user:
            print("\n=== MAIN MENU ===")
            print("1. User Login")
            print("2. User Registration")
            print("3. Admin Login")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                if user_login():
                    user_menu()
            elif choice == '2':
                register_user()
            elif choice == '3':
                if admin_login():
                    if current_user_type == 'theatre':
                        theatre_admin_menu()
                    elif current_user_type == 'system':
                        system_admin_menu()
            elif choice == '4':
                print("Thank you for using PVC!")
                sys.exit()
            elif choice == 'init2025':
                initialize_csv_files()
                print('Initializing Csv files..........')
            else:
                print("Invalid choice!")
        else:
            #already logged in
            if current_user_type == 'user':
                user_menu()
            elif current_user_type == 'theatre':
                theatre_admin_menu()
            elif current_user_type == 'system':
                system_admin_menu()



if __name__ == "__main__":
    main()
