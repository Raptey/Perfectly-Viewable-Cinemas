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
        print("System Administrator Access Only")
        print_menu({
            "1": "Login as System Admin",
            "0": "Exit"
        })

        choice = get_input("Choose an option: ")

        if choice == "1":
            username = get_input("Admin Username: ")
            password = get_input("Admin Password: ")
            success, user_info = system.authenticate_user(username, password)
            if success and user_info and user_info.get('type') == 'system':
                current_user = user_info
                system_admin_menu()
            else:
                input("Invalid admin credentials or access denied. Press Enter to continue...")

        elif choice == "0":
            print("Goodbye!")
            break





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