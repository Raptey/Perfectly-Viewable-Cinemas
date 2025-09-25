import os
from typing import Dict, Optional
from handler import CinemaSystem

system = CinemaSystem()
current_user: Optional[Dict] = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu(options: Dict[str, str]):
    print("\n" + "="*50)
    for key, value in options.items():
        print(f"{key}. {value}")
    print("="*50)

def get_input(prompt: str, validate=None) -> str:
    while True:
        value = input(prompt).strip()
        if validate is None or validate(value):
            return value
        print("Invalid input, please try again.")

def login_menu():
    global current_user
    while True:
        clear_screen()
        print("Welcome to PVC - Cinema Management System")
        print_menu({
            "1": "Login",
            "2": "Register",
            "0": "Exit"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            username = get_input("Username: ")
            password = get_input("Password: ")
            success, user_info = system.authenticate_user(username, password)
            if success and user_info:
                current_user = user_info
                if user_info.get('type') == 'user':
                    user_menu()
                elif user_info.get('type') == 'theatre':
                    theatre_admin_menu()
                else:
                    system_admin_menu()
            else:
                input("Invalid credentials. Press Enter to continue...")

        elif choice == "2":
            username = get_input("Username: ")
            password = get_input("Password: ")
            email = get_input("Email: ")
            if system.register_user(username, password, email):
                print("Registration successful!")
            else:
                print("Registration failed. Username or email already exists.")
            input("Press Enter to continue...")

        elif choice == "0":
            print("Goodbye!")
            break

def user_menu():
    global current_user
    while True:
        clear_screen()
        print(f"Welcome, User!")
        print_menu({
            "1": "Browse Movies",
            "2": "View My Bookings",
            "3": "Cancel Booking",
            "0": "Logout"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            browse_and_book_movies()
        elif choice == "2":
            view_bookings()
        elif choice == "3":
            cancel_user_booking()
        elif choice == "0":
            current_user = None
            break

def browse_and_book_movies():
    global current_user
    while True:
        clear_screen()
        movies = system.get_movies_showings()
        print("\nAvailable Movies and Showings:")
        print("-" * 80)
        print(f"{'ID':<4} {'Title':<30} {'Genre':<15} {'Time':<10} {'Seats':<8} {'Price':<8}")
        print("-" * 80)
        
        for movie in movies:
            print(f"{movie['id']:<4} {movie['title']:<30} {movie['genre']:<15} "
                f"{movie['showtime']:<10} {movie['available_seats']:<8} "
                f"${float(movie['price']):<7.2f}")
        
        print("\nEnter movie ID to book, or 0 to go back")
        choice = get_input("Choice: ")
        
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
                seats = get_input("Seats: ").split(',')
                if current_user and 'id' in current_user:
                    booking_id = system.book_tickets(
                        current_user['id'], 
                        selected_movie['id'],
                        seats
                    )
                    if booking_id:
                        print(f"\nBooking successful! Your booking ID is: {booking_id}")
                    else:
                        print("\nBooking failed. Seats might be taken or invalid.")
                else:
                    print("\nNo user logged in.")
            else:
                print("\nSorry, no seats available for this showing.")
            input("\nPress Enter to continue...")
        else:
            print("\nInvalid movie ID.")
            input("Press Enter to continue...")

def view_bookings():
    global current_user
    clear_screen()
    if not current_user or 'id' not in current_user:
        print("No user logged in.")
        input("\nPress Enter to continue...")
        return
    bookings = system.get_user_bookings(current_user['id'])
    
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

def cancel_user_booking():
    global current_user
    clear_screen()
    view_bookings()
    
    booking_id = get_input("\nEnter booking ID to cancel (or 0 to go back): ")
    if booking_id == "0":
        return
        
    if not current_user or 'id' not in current_user:
        print("No user logged in.")
        input("\nPress Enter to continue...")
        return
    if system.cancel_booking(booking_id, current_user['id']):
        print("Booking cancelled successfully!")
    else:
        print("Failed to cancel booking. Please check the booking ID.")
    input("\nPress Enter to continue...")

def theatre_admin_menu():
    global current_user
    while True:
        clear_screen()
        print(f"Welcome, Theatre Admin!")
        print_menu({
            "1": "Add Movie/Showing",
            "2": "View Theatre Bookings",
            "0": "Logout"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            add_movie_showing()
        elif choice == "2":
            view_theatre_bookings()
        elif choice == "0":
            current_user = None
            break

def add_movie_showing():
    global current_user
    clear_screen()
    print("Add New Movie/Showing")
    print("-" * 50)
    
    title = get_input("Movie Title: ")
    genre = get_input("Genre: ")
    duration = get_input("Duration (minutes): ", lambda x: x.isdigit())
    showtime = get_input("Showtime (HH:MM): ")
    seats = get_input("Number of Seats: ", lambda x: x.isdigit())
    price = get_input("Ticket Price: ", lambda x: x.replace('.','',1).isdigit())
    
    if not current_user or 'theatre_id' not in current_user:
        print("No theatre admin logged in.")
        input("\nPress Enter to continue...")
        return
    if system.add_movie_showing(
        title, genre, int(duration),
        current_user['theatre_id'], showtime,
        int(seats), float(price)
    ):
        print("Movie/Showing added successfully!")
    else:
        print("Failed to add movie/showing.")
    input("\nPress Enter to continue...")

def view_theatre_bookings():
    global current_user
    clear_screen()
    if not current_user or 'theatre_id' not in current_user:
        print("No theatre admin logged in.")
        input("\nPress Enter to continue...")
        return
    bookings = system.get_theatre_bookings(current_user['theatre_id'])
    
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

def system_admin_menu():
    global current_user
    while True:
        clear_screen()
        print(f"Welcome, System Admin!")
        print_menu({
            "1": "Initialize/Reset CSVs",
            "2": "Manage Theatre Admins",
            "3": "Manage User Accounts",
            "4": "Ban/Unban Users",
            "0": "Logout"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            system._ensure_csv_files_exist()
            print("CSV files have been initialized/reset.")
            input("Press Enter to continue...")
        elif choice == "2":
            manage_theatre_admins()
        elif choice == "3":
            manage_user_accounts()
        elif choice == "4":
            manage_user_bans()
        elif choice == "0":
            current_user = None
            break

def manage_theatre_admins():
    while True:
        clear_screen()
        print("Theatre Admin Management")
        print_menu({
            "1": "View All Theatre Admins",
            "2": "Create Theatre Admin",
            "3": "Modify Theatre Admin",
            "4": "Delete Theatre Admin",
            "0": "Back to Main Menu"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            view_theatre_admins()
        elif choice == "2":
            create_theatre_admin()
        elif choice == "3":
            modify_theatre_admin()
        elif choice == "4":
            delete_theatre_admin()
        elif choice == "0":
            break

def view_theatre_admins():
    clear_screen()
    admins = system.get_all_theatre_admins()
    
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

def create_theatre_admin():
    clear_screen()
    print("Create New Theatre Admin")
    print("-" * 50)
    
    username = get_input("Username: ")
    password = get_input("Password: ")
    theatre_id = get_input("Theatre ID: ")
    
    if system.create_theatre_admin(username, password, theatre_id):
        print("Theatre admin created successfully!")
    else:
        print("Failed to create theatre admin. Username may already exist.")
    input("\nPress Enter to continue...")

def modify_theatre_admin():
    clear_screen()
    view_theatre_admins()
    
    admin_id = get_input("\nEnter Admin ID to modify (or 0 to go back): ")
    if admin_id == "0":
        return
    
    print("\nLeave fields empty to keep current values:")
    username = get_input("New Username (or press Enter to skip): ")
    password = get_input("New Password (or press Enter to skip): ")
    theatre_id = get_input("New Theatre ID (or press Enter to skip): ")
    
    kwargs = {}
    if username:
        kwargs['username'] = username
    if password:
        kwargs['password'] = password
    if theatre_id:
        kwargs['theatre_id'] = theatre_id
    if system.modify_theatre_admin(admin_id, **kwargs):
        print("Theatre admin modified successfully!")
    else:
        print("Failed to modify theatre admin. Admin ID not found or username already exists.")
    input("\nPress Enter to continue...")

def delete_theatre_admin():
    clear_screen()
    view_theatre_admins()
    
    admin_id = get_input("\nEnter Admin ID to delete (or 0 to go back): ")
    if admin_id == "0":
        return
    
    confirm = get_input("Are you sure you want to delete this admin? (y/N): ")
    if confirm.lower() == 'y':
        if system.delete_theatre_admin(admin_id):
            print("Theatre admin deleted successfully!")
        else:
            print("Failed to delete theatre admin. Admin ID not found.")
    else:
        print("Deletion cancelled.")
    input("\nPress Enter to continue...")

def manage_user_accounts():
    while True:
        clear_screen()
        print("User Account Management")
        print_menu({
            "1": "View All Users",
            "2": "Modify User Account",
            "3": "Delete User Account",
            "0": "Back to Main Menu"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            view_all_users()
        elif choice == "2":
            modify_user_account()
        elif choice == "3":
            delete_user_account()
        elif choice == "0":
            break

def view_all_users():
    clear_screen()
    users = system.get_all_users()
    
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

def modify_user_account():
    clear_screen()
    view_all_users()
    
    user_id = get_input("\nEnter User ID to modify (or 0 to go back): ")
    if user_id == "0":
        return
    
    print("\nLeave fields empty to keep current values:")
    username = get_input("New Username (or press Enter to skip): ")
    password = get_input("New Password (or press Enter to skip): ")
    email = get_input("New Email (or press Enter to skip): ")
    
    kwargs = {}
    if username:
        kwargs['username'] = username
    if password:
        kwargs['password'] = password
    if email:
        kwargs['email'] = email
    if system.modify_user(user_id, **kwargs):
        print("User account modified successfully!")
    else:
        print("Failed to modify user account. User ID not found or username/email already exists.")
    input("\nPress Enter to continue...")

def delete_user_account():
    clear_screen()
    view_all_users()
    
    user_id = get_input("\nEnter User ID to delete (or 0 to go back): ")
    if user_id == "0":
        return
    
    confirm = get_input("Are you sure you want to delete this user and all their bookings? (y/N): ")
    if confirm.lower() == 'y':
        if system.delete_user(user_id):
            print("User account and all bookings deleted successfully!")
        else:
            print("Failed to delete user account. User ID not found.")
    else:
        print("Deletion cancelled.")
    input("\nPress Enter to continue...")

def manage_user_bans():
    while True:
        clear_screen()
        print("User Ban Management")
        print_menu({
            "1": "View Banned Users",
            "2": "Ban User by Email",
            "3": "Unban User by Email",
            "4": "Check User Status by Email",
            "0": "Back to Main Menu"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            view_banned_users()
        elif choice == "2":
            ban_user_by_email()
        elif choice == "3":
            unban_user_by_email()
        elif choice == "4":
            check_user_status_by_email()
        elif choice == "0":
            break

def view_banned_users():
    clear_screen()
    banned_users = system.get_banned_users()
    
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

def ban_user_by_email():
    clear_screen()
    print("Ban User by Email")
    print("-" * 50)
    
    email = get_input("Enter user email to ban: ")
    
    user = system.find_user_by_email(email)
    if not user:
        print("No user found with that email address.")
    elif user.get('status', 'active') == 'banned':
        print("User is already banned.")
    else:
        if system.ban_user_by_email(email):
            print(f"User with email '{email}' has been banned successfully!")
        else:
            print("Failed to ban user.")
    
    input("\nPress Enter to continue...")

def unban_user_by_email():
    clear_screen()
    print("Unban User by Email")
    print("-" * 50)
    
    email = get_input("Enter user email to unban: ")
    
    user = system.find_user_by_email(email)
    if not user:
        print("No user found with that email address.")
    elif user.get('status', 'active') == 'active':
        print("User is not currently banned.")
    else:
        if system.unban_user_by_email(email):
            print(f"User with email '{email}' has been unbanned successfully!")
        else:
            print("Failed to unban user.")
    
    input("\nPress Enter to continue...")

def check_user_status_by_email():
    clear_screen()
    print("Check User Status by Email")
    print("-" * 50)
    
    email = get_input("Enter user email to check: ")
    
    user = system.find_user_by_email(email)
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
    login_menu()