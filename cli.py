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
                "2": "Manage Theatre Admins",
                "3": "Manage User Accounts",
                "4": "Ban/Unban Users",
                "0": "Logout"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.system._ensure_csv_files_exist()
                print("CSV files have been initialized/reset.")
                input("Press Enter to continue...")
            elif choice == "2":
                self.manage_theatre_admins()
            elif choice == "3":
                self.manage_user_accounts()
            elif choice == "4":
                self.manage_user_bans()
            elif choice == "0":
                self.current_user = None
                break

    def manage_theatre_admins(self):
        while True:
            self.clear_screen()
            print("Theatre Admin Management")
            self.print_menu({
                "1": "View All Theatre Admins",
                "2": "Create Theatre Admin",
                "3": "Modify Theatre Admin",
                "4": "Delete Theatre Admin",
                "0": "Back to Main Menu"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.view_theatre_admins()
            elif choice == "2":
                self.create_theatre_admin()
            elif choice == "3":
                self.modify_theatre_admin()
            elif choice == "4":
                self.delete_theatre_admin()
            elif choice == "0":
                break

    def view_theatre_admins(self):
        self.clear_screen()
        admins = self.system.get_all_theatre_admins()
        
        if not admins:
            print("No theatre admins found.")
        else:
            print("\nTheatre Admins:")
            print("-" * 80)
            print(f"{'Admin ID':<10} {'Username':<20} {'Theatre ID':<15}")
            print("-" * 80)
            
            for admin in admins:
                print(f"{admin['admin_id']:<10} {admin['username']:<20} {admin['theatre_id']:<15}")
        
        input("\nPress Enter to continue...")

    def create_theatre_admin(self):
        self.clear_screen()
        print("Create New Theatre Admin")
        print("-" * 50)
        
        username = self.get_input("Username: ")
        password = self.get_input("Password: ")
        theatre_id = self.get_input("Theatre ID: ")
        
        if self.system.create_theatre_admin(username, password, theatre_id):
            print("Theatre admin created successfully!")
        else:
            print("Failed to create theatre admin. Username may already exist.")
        input("\nPress Enter to continue...")

    def modify_theatre_admin(self):
        self.clear_screen()
        self.view_theatre_admins()
        
        admin_id = self.get_input("\nEnter Admin ID to modify (or 0 to go back): ")
        if admin_id == "0":
            return
        
        print("\nLeave fields empty to keep current values:")
        username = self.get_input("New Username (or press Enter to skip): ")
        password = self.get_input("New Password (or press Enter to skip): ")
        theatre_id = self.get_input("New Theatre ID (or press Enter to skip): ")
        
        # Convert empty strings to None
        username = username if username else None
        password = password if password else None
        theatre_id = theatre_id if theatre_id else None
        
        if self.system.modify_theatre_admin(admin_id, username, password, theatre_id):
            print("Theatre admin modified successfully!")
        else:
            print("Failed to modify theatre admin. Admin ID not found or username already exists.")
        input("\nPress Enter to continue...")

    def delete_theatre_admin(self):
        self.clear_screen()
        self.view_theatre_admins()
        
        admin_id = self.get_input("\nEnter Admin ID to delete (or 0 to go back): ")
        if admin_id == "0":
            return
        
        confirm = self.get_input("Are you sure you want to delete this admin? (y/N): ")
        if confirm.lower() == 'y':
            if self.system.delete_theatre_admin(admin_id):
                print("Theatre admin deleted successfully!")
            else:
                print("Failed to delete theatre admin. Admin ID not found.")
        else:
            print("Deletion cancelled.")
        input("\nPress Enter to continue...")

    def manage_user_accounts(self):
        while True:
            self.clear_screen()
            print("User Account Management")
            self.print_menu({
                "1": "View All Users",
                "2": "Modify User Account",
                "3": "Delete User Account",
                "0": "Back to Main Menu"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.view_all_users()
            elif choice == "2":
                self.modify_user_account()
            elif choice == "3":
                self.delete_user_account()
            elif choice == "0":
                break

    def view_all_users(self):
        self.clear_screen()
        users = self.system.get_all_users()
        
        if not users:
            print("No users found.")
        else:
            print("\nAll Users:")
            print("-" * 90)
            print(f"{'User ID':<10} {'Username':<20} {'Email':<30} {'Status':<10}")
            print("-" * 90)
            
            for user in users:
                status = user.get('status', 'active')
                print(f"{user['user_id']:<10} {user['username']:<20} {user['email']:<30} {status:<10}")
        
        input("\nPress Enter to continue...")

    def modify_user_account(self):
        self.clear_screen()
        self.view_all_users()
        
        user_id = self.get_input("\nEnter User ID to modify (or 0 to go back): ")
        if user_id == "0":
            return
        
        print("\nLeave fields empty to keep current values:")
        username = self.get_input("New Username (or press Enter to skip): ")
        password = self.get_input("New Password (or press Enter to skip): ")
        email = self.get_input("New Email (or press Enter to skip): ")
        
        # Convert empty strings to None
        username = username if username else None
        password = password if password else None
        email = email if email else None
        
        if self.system.modify_user(user_id, username, password, email):
            print("User account modified successfully!")
        else:
            print("Failed to modify user account. User ID not found or username/email already exists.")
        input("\nPress Enter to continue...")

    def delete_user_account(self):
        self.clear_screen()
        self.view_all_users()
        
        user_id = self.get_input("\nEnter User ID to delete (or 0 to go back): ")
        if user_id == "0":
            return
        
        confirm = self.get_input("Are you sure you want to delete this user and all their bookings? (y/N): ")
        if confirm.lower() == 'y':
            if self.system.delete_user(user_id):
                print("User account and all bookings deleted successfully!")
            else:
                print("Failed to delete user account. User ID not found.")
        else:
            print("Deletion cancelled.")
        input("\nPress Enter to continue...")

    def manage_user_bans(self):
        while True:
            self.clear_screen()
            print("User Ban Management")
            self.print_menu({
                "1": "View Banned Users",
                "2": "Ban User by Email",
                "3": "Unban User by Email",
                "4": "Check User Status by Email",
                "0": "Back to Main Menu"
            })

            choice = self.get_input("Choose an option: ")

            if choice == "1":
                self.view_banned_users()
            elif choice == "2":
                self.ban_user_by_email()
            elif choice == "3":
                self.unban_user_by_email()
            elif choice == "4":
                self.check_user_status_by_email()
            elif choice == "0":
                break

    def view_banned_users(self):
        self.clear_screen()
        banned_users = self.system.get_banned_users()
        
        if not banned_users:
            print("No banned users found.")
        else:
            print("\nBanned Users:")
            print("-" * 80)
            print(f"{'User ID':<10} {'Username':<20} {'Email':<30} {'Status':<10}")
            print("-" * 80)
            
            for user in banned_users:
                print(f"{user['user_id']:<10} {user['username']:<20} {user['email']:<30} {user['status']:<10}")
        
        input("\nPress Enter to continue...")

    def ban_user_by_email(self):
        self.clear_screen()
        print("Ban User by Email")
        print("-" * 50)
        
        email = self.get_input("Enter user email to ban: ")
        
        # First check if user exists
        user = self.system.find_user_by_email(email)
        if not user:
            print("No user found with that email address.")
        elif user.get('status', 'active') == 'banned':
            print("User is already banned.")
        else:
            if self.system.ban_user_by_email(email):
                print(f"User with email '{email}' has been banned successfully!")
            else:
                print("Failed to ban user.")
        
        input("\nPress Enter to continue...")

    def unban_user_by_email(self):
        self.clear_screen()
        print("Unban User by Email")
        print("-" * 50)
        
        email = self.get_input("Enter user email to unban: ")
        
        # First check if user exists
        user = self.system.find_user_by_email(email)
        if not user:
            print("No user found with that email address.")
        elif user.get('status', 'active') == 'active':
            print("User is not currently banned.")
        else:
            if self.system.unban_user_by_email(email):
                print(f"User with email '{email}' has been unbanned successfully!")
            else:
                print("Failed to unban user.")
        
        input("\nPress Enter to continue...")

    def check_user_status_by_email(self):
        self.clear_screen()
        print("Check User Status by Email")
        print("-" * 50)
        
        email = self.get_input("Enter user email to check: ")
        
        user = self.system.find_user_by_email(email)
        if not user:
            print("No user found with that email address.")
        else:
            status = user.get('status', 'active')
            print(f"\nUser Details:")
            print(f"User ID: {user['user_id']}")
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
            print(f"Status: {status}")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    cli = CinemaCLI()
    cli.login_menu()