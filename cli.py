#!/usr/bin/env python3
"""
CLI for PVC - Perfectly Viewable Cinemas
Imports business logic from handler.py
"""
import sys
from handler import *

current_user = None
current_user_type = None

def cli_user_login():
    global current_user, current_user_type
    print("\n=== USER LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")
    user = user_login(username, password)
    if user:
        current_user = user
        current_user_type = 'user'
        print(f"Welcome, {username}!")
        return True
    print("Invalid credentials!")
    return False

def cli_admin_login():
    global current_user, current_user_type
    print("\n=== ADMIN LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")
    admin = admin_login(username, password)
    if admin:
        current_user = admin
        current_user_type = admin['type']
        print(f"Welcome, {username}! ({admin['type']} admin)")
        return True
    print("Invalid admin credentials!")
    return False

def cli_register_user():
    print("\n=== USER REGISTRATION ===")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    success, msg = register_user(username, password, email)
    print(msg)
    return success

def cli_view_movies():
    print("\n=== AVAILABLE MOVIES ===")
    movies = get_movies()
    showings = get_showings()
    theatres = get_theatres()
    if not showings:
        print("No showings available.")
        return
    movie_lookup = {m['movie_id']: m['title'] for m in movies}
    theatre_lookup = {t['theatre_id']: t['name'] for t in theatres}
    print(f"{'Showing ID':<10} {'Movie':<25} {'Theatre':<15} {'Showtime':<8} {'Seats':<5}")
    print("-" * 70)
    for showing in showings:
        movie_title = movie_lookup.get(showing['movie_id'], 'Unknown')
        theatre_name = theatre_lookup.get(showing['theatre_id'], 'Unknown')
        print(f"{showing['showing_id']:<10} {movie_title[:24]:<25} {theatre_name:<15} {showing['showtime']:<8} {showing['available_seats']:<5}")

def cli_book_ticket():
    if not current_user or current_user_type != 'user':
        print("Please login as a user first!")
        return
    print("\n=== BOOK TICKET ===")
    cli_view_movies()
    showing_id = input("\nEnter Showing ID to book: ")
    seats_wanted = input("Number of seats: ")
    try:
        seats_wanted = int(seats_wanted)
    except ValueError:
        print("Invalid number of seats!")
        return
    success, result = book_ticket(current_user['user_id'], showing_id, seats_wanted)
    if success:
        print(f"\nBooking successful! Booking ID: {result}")
    else:
        print(result)

def cli_view_user_bookings():
    if not current_user or current_user_type != 'user':
        print("Please login as a user first!")
        return
    print("\n=== YOUR BOOKINGS ===")
    bookings = get_user_bookings(current_user['user_id'])
    movies = get_movies()
    theatres = get_theatres()
    if not bookings:
        print("No bookings found.")
        return
    movie_lookup = {m['movie_id']: m['title'] for m in movies}
    theatre_lookup = {t['theatre_id']: t['name'] for t in theatres}
    print(f"{'Booking ID':<10} {'Movie':<25} {'Theatre':<15} {'Seats':<5} {'Date':<19}")
    print("-" * 80)
    for booking in bookings:
        movie_title = movie_lookup.get(booking['movie_id'], 'Unknown')
        theatre_name = theatre_lookup.get(booking['theatre_id'], 'Unknown')
        print(f"{booking['booking_id']:<10} {movie_title[:24]:<25} {theatre_name:<15} {booking['seats_booked']:<5} {booking['booking_date']:<19}")

def cli_add_movie():
    if not current_user or current_user_type != 'theatre':
        print("Access denied! Theatre admin login required.")
        return
    print("\n=== ADD MOVIE ===")
    title = input("Movie Title: ")
    genre = input("Genre: ")
    duration = input("Duration (minutes): ")
    showtime = input("Showtime (HH:MM): ")
    seats = input("Available Seats: ")
    success, msg = add_movie(title, genre, duration, showtime, seats, current_user['theatre_id'])
    print(msg)

def cli_add_showing():
    if not current_user or current_user_type != 'theatre':
        print("Access denied! Theatre admin login required.")
        return
    print("\n=== ADD SHOWING ===")
    movies = get_movies()
    movie_titles = [f"{m['title']} (ID: {m['movie_id']})" for m in movies]
    selected = input("Select Movie by ID: ")
    theatre_id = current_user['theatre_id']
    showtime = input("Showtime (HH:MM): ")
    seats = input("Available Seats: ")
    success, msg = add_showing(selected, theatre_id, showtime, seats)
    print(msg)

def cli_view_theatre_bookings():
    if not current_user or current_user_type != 'theatre':
        print("Access denied! Theatre admin login required.")
        return
    print(f"\n=== BOOKINGS FOR THEATRE {current_user['theatre_id']} ===")
    bookings = get_theatre_bookings(current_user['theatre_id'])
    movies = get_movies()
    users = get_users()
    if not bookings:
        print("No bookings found for this theatre.")
        return
    movie_lookup = {m['movie_id']: m['title'] for m in movies}
    user_lookup = {u['user_id']: u['username'] for u in users}
    print(f"{'Booking ID':<10} {'User':<15} {'Movie':<25} {'Seats':<5} {'Date':<19}")
    print("-" * 80)
    for booking in bookings:
        movie_title = movie_lookup.get(booking['movie_id'], 'Unknown')
        username = user_lookup.get(booking['user_id'], 'Unknown')
        print(f"{booking['booking_id']:<10} {username:<15} {movie_title[:24]:<25} {booking['seats_booked']:<5} {booking['booking_date']:<19}")

def cli_system_admin_stats():
    if not current_user or current_user_type != 'system':
        print("Access denied! System admin login required.")
        return
    print("\n=== SYSTEM STATISTICS ===")
    users = get_users()
    movies = get_movies()
    theatres = get_theatres()
    bookings = get_all_bookings()
    print(f"Total Users: {len(users)}")
    print(f"Total Movies: {len(movies)}")
    print(f"Total Theatres: {len(theatres)}")
    print(f"Total Bookings: {len(bookings)}")
    total_tickets = sum(int(b['seats_booked']) for b in bookings)
    total_revenue = total_tickets * 10
    print(f"Total Tickets Sold: {total_tickets}")
    print(f"Estimated Revenue: ${total_revenue}")

def cli_view_all_bookings():
    print("\n=== ALL BOOKINGS ===")
    bookings = get_all_bookings()
    movies = get_movies()
    users = get_users()
    theatres = get_theatres()
    if not bookings:
        print("No bookings found.")
        return
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
    global current_user, current_user_type
    print("Logged out successfully!")
    current_user = None
    current_user_type = None

def main():
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
                if cli_user_login():
                    user_menu()
            elif choice == '2':
                cli_register_user()
            elif choice == '3':
                if cli_admin_login():
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
            if current_user_type == 'user':
                user_menu()
            elif current_user_type == 'theatre':
                theatre_admin_menu()
            elif current_user_type == 'system':
                system_admin_menu()

def user_menu():
    while True:
        print("\n=== USER MENU ===")
        print("1. View Available Movies")
        print("2. Book Ticket")
        print("3. View My Bookings")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            cli_view_movies()
        elif choice == '2':
            cli_book_ticket()
        elif choice == '3':
            cli_view_user_bookings()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice!")

def theatre_admin_menu():
    while True:
        print("\n=== THEATRE ADMIN MENU ===")
        print("1. View Available Movies")
        print("2. Add Movie")
        print("3. View Theatre Bookings")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            cli_view_movies()
        elif choice == '2':
            cli_add_movie()
        elif choice == '3':
            cli_view_theatre_bookings()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice!")

def system_admin_menu():
    while True:
        print("\n=== SYSTEM ADMIN MENU ===")
        print("1. View System Statistics")
        print("2. View All Movies")
        print("3. View All Bookings")
        print("4. Logout")
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            cli_system_admin_stats()
        elif choice == '2':
            cli_view_movies()
        elif choice == '3':
            cli_view_all_bookings()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
