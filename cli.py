import os
from typing import Dict, Optional
from handler import CinemaSystem

class CinemaCLI:
    def __init__(self):
        self.system = CinemaSystem()
        self.current_user: Optional[Dict] = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self, options: Dict[str, str]):
        print("\n" + "="*50)
        for key, value in options.items():
            print(f"{key}. {value}")
        print("="*50)

    def get_input(self, prompt: str, validate=None) -> str:
        while True:
            value = input(prompt).strip()
            if validate is None or validate(value):
                return value
            print("Invalid input, please try again.")

    def login_menu(self):
        while True:
            self.clear_screen()
            print("Welcome to PVC - Cinema Management System")
            self.print_menu({
                "1": "Login",
                "2": "Register",
                "0": "Exit"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                username = self.get_input("Username: ")
                password = self.get_input("Password: ")
                success, user_info = self.system.authenticate_user(username, password)
                if success:
                    self.current_user = user_info
                    if user_info['type'] == 'user':
                        self.user_menu()
                    elif user_info['type'] == 'theatre':
                        self.theatre_admin_menu()
                    else:  # system admin
                        self.system_admin_menu()
                else:
                    input("Invalid credentials. Press Enter to continue...")

            elif choice == "2":
                username = self.get_input("Username: ")
                password = self.get_input("Password: ")
                email = self.get_input("Email: ")
                if self.system.register_user(username, password, email):
                    print("Registration successful!")
                else:
                    print("Registration failed. Username or email already exists.")
                input("Press Enter to continue...")

            elif choice == "0":
                print("Goodbye!")
                break

    def user_menu(self):
        while True:
            self.clear_screen()
            print(f"Welcome, User!")
            self.print_menu({
                "1": "Browse Movies",
                "2": "View My Bookings",
                "3": "Cancel Booking",
                "0": "Logout"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.browse_and_book_movies()
            elif choice == "2":
                self.view_bookings()
            elif choice == "3":
                self.cancel_user_booking()
            elif choice == "0":
                self.current_user = None
                break

    def browse_and_book_movies(self):
        while True:
            self.clear_screen()
            movies = self.system.get_movies_showings()
            print("\nAvailable Movies and Showings:")
            print("-" * 80)
            print(f"{'ID':<4} {'Title':<30} {'Genre':<15} {'Time':<10} {'Seats':<8} {'Price':<8}")
            print("-" * 80)
            
            for movie in movies:
                print(f"{movie['id']:<4} {movie['title']:<30} {movie['genre']:<15} "
                      f"{movie['showtime']:<10} {movie['available_seats']:<8} "
                      f"${float(movie['price']):<7.2f}")
            
            print("\nEnter movie ID to book, or 0 to go back")
            choice = self.get_input("Choice: ")
            
            if choice == "0":
                break
                
            # Find selected movie
            selected_movie = next((m for m in movies if m['id'] == choice), None)
            if selected_movie:
                seats_available = int(selected_movie['available_seats'])
                if seats_available > 0:
                    print(f"\nBooking for: {selected_movie['title']}")
                    print(f"Available seats: {seats_available}")
                    print("Enter seat numbers separated by commas (e.g., A1,A2,B1)")
                    seats = self.get_input("Seats: ").split(',')
                    
                    booking_id = self.system.book_tickets(
                        self.current_user['id'], 
                        selected_movie['id'],
                        seats
                    )
                    
                    if booking_id:
                        print(f"\nBooking successful! Your booking ID is: {booking_id}")
                    else:
                        print("\nBooking failed. Seats might be taken or invalid.")
                else:
                    print("\nSorry, no seats available for this showing.")
                input("\nPress Enter to continue...")
            else:
                print("\nInvalid movie ID.")
                input("Press Enter to continue...")

    def view_bookings(self):
        self.clear_screen()
        bookings = self.system.get_user_bookings(self.current_user['id'])
        
        if not bookings:
            print("You have no bookings.")
        else:
            print("\nYour Bookings:")
            print("-" * 80)
            print(f"{'Booking ID':<12} {'Movie ID':<10} {'Seats':<20} {'Price':<10} {'Date':<25}")
            print("-" * 80)
            
            for booking in bookings:
                print(f"{booking['booking_id']:<12} {booking['showing_id']:<10} "
                      f"{booking['seat_numbers']:<20} ${float(booking['total_price']):<9.2f} "
                      f"{booking['booking_date'][:19]}")
        
        input("\nPress Enter to continue...")

    def cancel_user_booking(self):
        self.clear_screen()
        self.view_bookings()
        
        booking_id = self.get_input("\nEnter booking ID to cancel (or 0 to go back): ")
        if booking_id == "0":
            return
            
        if self.system.cancel_booking(booking_id, self.current_user['id']):
            print("Booking cancelled successfully!")
        else:
            print("Failed to cancel booking. Please check the booking ID.")
        input("\nPress Enter to continue...")

    def theatre_admin_menu(self):
        while True:
            self.clear_screen()
            print(f"Welcome, Theatre Admin!")
            self.print_menu({
                "1": "Add Movie/Showing",
                "2": "View Theatre Bookings",
                "0": "Logout"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.add_movie_showing()
            elif choice == "2":
                self.view_theatre_bookings()
            elif choice == "0":
                self.current_user = None
                break

    def add_movie_showing(self):
        self.clear_screen()
        print("Add New Movie/Showing")
        print("-" * 50)
        
        title = self.get_input("Movie Title: ")
        genre = self.get_input("Genre: ")
        duration = self.get_input("Duration (minutes): ", lambda x: x.isdigit())
        showtime = self.get_input("Showtime (HH:MM): ")
        seats = self.get_input("Number of Seats: ", lambda x: x.isdigit())
        price = self.get_input("Ticket Price: ", lambda x: x.replace('.','',1).isdigit())
        
        if self.system.add_movie_showing(
            title, genre, int(duration),
            self.current_user['theatre_id'], showtime,
            int(seats), float(price)
        ):
            print("Movie/Showing added successfully!")
        else:
            print("Failed to add movie/showing.")
        input("\nPress Enter to continue...")

    def view_theatre_bookings(self):
        self.clear_screen()
        bookings = self.system.get_theatre_bookings(self.current_user['theatre_id'])
        
        if not bookings:
            print("No bookings for your theatre.")
        else:
            print("\nTheatre Bookings:")
            print("-" * 80)
            print(f"{'Booking ID':<12} {'User ID':<10} {'Movie ID':<10} "
                  f"{'Seats':<20} {'Price':<10} {'Date':<25}")
            print("-" * 80)
            
            for booking in bookings:
                print(f"{booking['booking_id']:<12} {booking['user_id']:<10} "
                      f"{booking['showing_id']:<10} {booking['seat_numbers']:<20} "
                      f"${float(booking['total_price']):<9.2f} "
                      f"{booking['booking_date'][:19]}")
        
        input("\nPress Enter to continue...")

    def system_admin_menu(self):
        while True:
            self.clear_screen()
            print(f"Welcome, System Admin!")
            self.print_menu({
                "1": "Initialize/Reset CSVs",
                "0": "Logout"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.system._ensure_csv_files_exist()
                print("CSV files have been initialized/reset.")
                input("Press Enter to continue...")
            elif choice == "0":
                self.current_user = None
                break

if __name__ == '__main__':
    cli = CinemaCLI()
    cli.login_menu()