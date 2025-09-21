import csv
import os
import datetime
from typing import List, Dict, Optional, Tuple
from crypto import hash_password, verify_password

class CinemaSystem:
    def __init__(self):
        self.csv_files = {
            'movies_showings': 'movies_showings.csv',
            'users': 'users.csv',
            'admins': 'admins.csv',
            'bookings': 'bookings.csv'
        }
        self._ensure_csv_files_exist()

    def _ensure_csv_files_exist(self):
        """Initialize CSV files with headers and example data if they don't exist."""
        headers = {
            'movies_showings': ['id', 'title', 'genre', 'duration', 'theatre_id', 'showtime', 'available_seats', 'price'],
            'users': ['user_id', 'username', 'password', 'salt', 'email', 'status'],
            'admins': ['admin_id', 'username', 'password', 'salt', 'type', 'theatre_id'],
            'bookings': ['booking_id', 'user_id', 'showing_id', 'seats_booked', 'seat_numbers', 'total_price', 'booking_date']
        }
        
        # Example data to populate when creating new files
        example_data = {
            'movies_showings': [
                ['1', 'The Matrix', 'Sci-Fi', '136', '1', '19:30', '50', '12.50'],
                ['2', 'Inception', 'Sci-Fi', '148', '1', '21:00', '45', '14.00'],
                ['3', 'The Dark Knight', 'Action', '152', '2', '20:15', '60', '13.50'],
                ['4', 'Interstellar', 'Sci-Fi', '169', '2', '18:45', '40', '15.00']
            ],
            'users': [
                # Regular user - username: demo, password: demo
                ['1', 'demo', 'bf46ada9f6237602b2e2818ecfd914bd18e822c7dcdaf4a835a80c870d4f5fe3', '22fe334fef8b2995d7cc1b5cf8f97880', 'demo@demo.com', 'active'],
                # Second regular user - username: john, password: user123
                ['2', 'john', '2cb8605e5e9330db6db5c9a810030403dad3d2ebc89a9ca57a1755f7874cefaa', '59947a5f5445a0ed45545bfd58d3bdae', 'john@cinema.com', 'active'],
                # Third regular user - username: alice, password: alice123
                ['3', 'alice', '44762a3a55f7ddfae12d806c9232a00229590ad2bb0072cfa8e4d30c03766ac1', 'a42d72101325ba5456e47d9aa3bc402f', 'alice@email.com', 'active']
            ],
            'admins': [
                # System admin - username: sysadmin, password: admin
                ['1', 'sysadmin', '9debf7cc5454c09f1ca385b50528164a0efd311b829afb0fd8052d294dbd1244', 'f132111b0b374f9cf1c6fc83d072e21a', 'system', ''],
                # Theatre admin for theatre 1 - username: theatre1, password: theatre1
                ['2', 'theatre1', 'feb2c5d2f340e320439353fc3561eceb747378e452d48ed41cad20807bc15396', 'd4ba216a203205f7e3f959c759eb9959', 'theatre', '1'],
                # Theatre admin for theatre 2 - username: theatre2, password: theatre2
                ['3', 'theatre2', 'a7014bc186c29cf0c2b5fd00250310fb2ad30f919600390b58fdcdbb471dc585', '372e733eab5eb9716a31478d545de037', 'theatre', '2']
            ],
            'bookings': []
        }
        
        for file_key, filename in self.csv_files.items():
            if not os.path.exists(filename):
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers[file_key])
                    # Add example data if available for this file type
                    if file_key in example_data:
                        writer.writerows(example_data[file_key])

    def _read_csv(self, file_key: str) -> List[Dict]:
        """Read a CSV file and return list of dictionaries."""
        data = []
        with open(self.csv_files[file_key], 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data

    def _write_csv(self, file_key: str, data: List[Dict]):
        """Write list of dictionaries to CSV file."""
        headers = {
            'movies_showings': ['id', 'title', 'genre', 'duration', 'theatre_id', 'showtime', 'available_seats', 'price'],
            'users': ['user_id', 'username', 'password', 'salt', 'email', 'status'],
            'admins': ['admin_id', 'username', 'password', 'salt', 'type', 'theatre_id'],
            'bookings': ['booking_id', 'user_id', 'showing_id', 'seats_booked', 'seat_numbers', 'total_price', 'booking_date']
        }
        
        with open(self.csv_files[file_key], 'w', newline='') as f:
            writer = csv.writer(f)
            # Always write headers
            writer.writerow(headers[file_key])
            
            # Write data rows if any exist
            if data:
                dict_writer = csv.DictWriter(f, fieldnames=headers[file_key])
                dict_writer.writerows(data)

    def register_user(self, username: str, password: str, email: str) -> bool:
        """Register a new user."""
        users = self._read_csv('users')
        
        # Check if username or email already exists
        if any(u['username'] == username or u['email'] == email for u in users):
            return False
        
        # Hash password
        hashed_pass, salt = hash_password(password)
        
        # Generate new user ID
        user_id = str(max([int(u['user_id']) for u in users], default=0) + 1)
        
        new_user = {
            'user_id': user_id,
            'username': username,
            'password': hashed_pass,
            'salt': salt,
            'email': email,
            'status': 'active'
        }
        
        users.append(new_user)
        self._write_csv('users', users)
        return True

    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict]]:
        """Authenticate a user or admin."""
        # Check users first
        users = self._read_csv('users')
        for user in users:
            if user['username'] == username:
                # Check if user is banned
                if user.get('status', 'active') == 'banned':
                    return False, None
                if verify_password(password, user['password'], user['salt']):
                    return True, {'type': 'user', 'id': user['user_id']}
        
        # Check admins
        admins = self._read_csv('admins')
        for admin in admins:
            if admin['username'] == username:
                if verify_password(password, admin['password'], admin['salt']):
                    return True, {'type': admin['type'], 'id': admin['admin_id'], 
                                'theatre_id': admin['theatre_id']}
        
        return False, None

    def get_movies_showings(self, theatre_id: Optional[str] = None) -> List[Dict]:
        """Get all movies and showings, optionally filtered by theatre."""
        movies = self._read_csv('movies_showings')
        if theatre_id:
            return [m for m in movies if m['theatre_id'] == theatre_id]
        return movies

    def add_movie_showing(self, title: str, genre: str, duration: int, 
                         theatre_id: str, showtime: str, seats: int, price: float) -> bool:
        """Add a new movie showing."""
        movies = self._read_csv('movies_showings')
        
        # Generate new ID
        movie_id = str(max([int(m['id']) for m in movies], default=0) + 1)
        
        new_movie = {
            'id': movie_id,
            'title': title,
            'genre': genre,
            'duration': str(duration),
            'theatre_id': theatre_id,
            'showtime': showtime,
            'available_seats': str(seats),
            'price': str(price)
        }
        
        movies.append(new_movie)
        self._write_csv('movies_showings', movies)
        return True

    def book_tickets(self, user_id: str, showing_id: str, 
                    seat_numbers: List[str]) -> Optional[str]:
        """Book tickets for a showing."""
        movies = self._read_csv('movies_showings')
        bookings = self._read_csv('bookings')
        
        # Find the showing
        showing = None
        for m in movies:
            if m['id'] == showing_id:
                showing = m
                break
        
        if not showing:
            return None
        
        # Check if seats are available
        available_seats = int(showing['available_seats'])
        if available_seats < len(seat_numbers):
            return None
        
        # Check if seats are already booked
        existing_bookings = [b for b in bookings if b['showing_id'] == showing_id]
        booked_seats = []
        for booking in existing_bookings:
            booked_seats.extend(booking['seat_numbers'].split(','))
        
        if any(seat in booked_seats for seat in seat_numbers):
            return None
        
        # Create booking
        booking_id = str(max([int(b['booking_id']) for b in bookings], default=0) + 1)
        total_price = len(seat_numbers) * float(showing['price'])
        
        new_booking = {
            'booking_id': booking_id,
            'user_id': user_id,
            'showing_id': showing_id,
            'seats_booked': str(len(seat_numbers)),
            'seat_numbers': ','.join(seat_numbers),
            'total_price': str(total_price),
            'booking_date': datetime.datetime.now().isoformat()
        }
        
        # Update available seats
        showing['available_seats'] = str(available_seats - len(seat_numbers))
        
        # Save changes
        bookings.append(new_booking)
        self._write_csv('bookings', bookings)
        self._write_csv('movies_showings', movies)
        
        return booking_id

    def get_user_bookings(self, user_id: str) -> List[Dict]:
        """Get all bookings for a user."""
        bookings = self._read_csv('bookings')
        return [b for b in bookings if b['user_id'] == user_id]

    def cancel_booking(self, booking_id: str, user_id: str) -> bool:
        """Cancel a booking and return seats to availability."""
        bookings = self._read_csv('bookings')
        movies = self._read_csv('movies_showings')
        
        # Convert inputs to strings to ensure consistency
        booking_id = str(booking_id)
        user_id = str(user_id)
        
        # Find the booking
        booking = None
        for b in bookings:
            # Convert booking data to strings for comparison
            b_booking_id = str(b['booking_id'])
            b_user_id = str(b['user_id'])
            
            if b_booking_id == booking_id and b_user_id == user_id:
                booking = b
                break
        
        if not booking:
            # Debug: Print all bookings for troubleshooting
            print(f"DEBUG: Could not find booking {booking_id} for user {user_id}")
            print("Available bookings:")
            for b in bookings:
                print(f"  Booking {b['booking_id']} for user {b['user_id']}")
            return False
        
        # Update movie seats
        for movie in movies:
            if movie['id'] == booking['showing_id']:
                current_available = int(movie['available_seats'])
                seats_to_restore = int(booking['seats_booked'])
                movie['available_seats'] = str(current_available + seats_to_restore)
                print(f"DEBUG: Restored {seats_to_restore} seats to movie {movie['id']}")
                break
        
        # Remove booking - filter out the specific booking
        original_count = len(bookings)
        bookings = [b for b in bookings if str(b['booking_id']) != booking_id]
        removed_count = original_count - len(bookings)
        
        print(f"DEBUG: Removed {removed_count} booking(s) with ID {booking_id}")
        print(f"DEBUG: Bookings remaining: {len(bookings)}")
        
        # Save changes
        self._write_csv('bookings', bookings)
        self._write_csv('movies_showings', movies)
        
        # Verify the file was updated
        updated_bookings = self._read_csv('bookings')
        print(f"DEBUG: After save, CSV contains {len(updated_bookings)} bookings")
        
        return True

    def get_theatre_bookings(self, theatre_id: str) -> List[Dict]:
        """Get all bookings for a specific theatre."""
        bookings = self._read_csv('bookings')
        movies = self._read_csv('movies_showings')
        
        theatre_movies = {m['id']: m for m in movies if m['theatre_id'] == theatre_id}
        return [b for b in bookings if b['showing_id'] in theatre_movies]

    # Theatre Admin Management Methods
    def create_theatre_admin(self, username: str, password: str, theatre_id: str) -> bool:
        """Create a new theatre admin account."""
        admins = self._read_csv('admins')
        
        # Check if username already exists
        if any(a['username'] == username for a in admins):
            return False
        
        # Hash password
        hashed_pass, salt = hash_password(password)
        
        # Generate new admin ID
        admin_id = str(max([int(a['admin_id']) for a in admins if a['admin_id']], default=0) + 1)
        
        new_admin = {
            'admin_id': admin_id,
            'username': username,
            'password': hashed_pass,
            'salt': salt,
            'type': 'theatre',
            'theatre_id': theatre_id
        }
        
        admins.append(new_admin)
        self._write_csv('admins', admins)
        return True

    def get_all_theatre_admins(self) -> List[Dict]:
        """Get all theatre admin accounts."""
        admins = self._read_csv('admins')
        return [a for a in admins if a['type'] == 'theatre']

    def modify_theatre_admin(self, admin_id: str, username: str = None, 
                           password: str = None, theatre_id: str = None) -> bool:
        """Modify a theatre admin account."""
        admins = self._read_csv('admins')
        
        # Find the admin
        admin_found = False
        for admin in admins:
            if admin['admin_id'] == admin_id and admin['type'] == 'theatre':
                admin_found = True
                if username:
                    # Check if new username already exists
                    if any(a['username'] == username and a['admin_id'] != admin_id for a in admins):
                        return False
                    admin['username'] = username
                if password:
                    hashed_pass, salt = hash_password(password)
                    admin['password'] = hashed_pass
                    admin['salt'] = salt
                if theatre_id:
                    admin['theatre_id'] = theatre_id
                break
        
        if not admin_found:
            return False
        
        self._write_csv('admins', admins)
        return True

    def delete_theatre_admin(self, admin_id: str) -> bool:
        """Delete a theatre admin account."""
        admins = self._read_csv('admins')
        original_count = len(admins)
        
        # Remove the admin
        admins = [a for a in admins if not (a['admin_id'] == admin_id and a['type'] == 'theatre')]
        
        if len(admins) == original_count:
            return False
        
        self._write_csv('admins', admins)
        return True

    # User Account Management Methods
    def get_all_users(self) -> List[Dict]:
        """Get all user accounts."""
        return self._read_csv('users')

    def modify_user(self, user_id: str, username: str = None, 
                   password: str = None, email: str = None) -> bool:
        """Modify a user account."""
        users = self._read_csv('users')
        
        # Find the user
        user_found = False
        for user in users:
            if user['user_id'] == user_id:
                user_found = True
                if username:
                    # Check if new username already exists
                    if any(u['username'] == username and u['user_id'] != user_id for u in users):
                        return False
                    user['username'] = username
                if password:
                    hashed_pass, salt = hash_password(password)
                    user['password'] = hashed_pass
                    user['salt'] = salt
                if email:
                    # Check if new email already exists
                    if any(u['email'] == email and u['user_id'] != user_id for u in users):
                        return False
                    user['email'] = email
                break
        
        if not user_found:
            return False
        
        self._write_csv('users', users)
        return True

    def delete_user(self, user_id: str) -> bool:
        """Delete a user account and their bookings."""
        users = self._read_csv('users')
        bookings = self._read_csv('bookings')
        movies = self._read_csv('movies_showings')
        
        # Check if user exists
        user_exists = any(u['user_id'] == user_id for u in users)
        if not user_exists:
            return False
        
        # Cancel all user's bookings and restore seats
        user_bookings = [b for b in bookings if b['user_id'] == user_id]
        for booking in user_bookings:
            # Restore seats to movie
            for movie in movies:
                if movie['id'] == booking['showing_id']:
                    movie['available_seats'] = str(int(movie['available_seats']) + 
                                                 int(booking['seats_booked']))
                    break
        
        # Remove user and their bookings
        users = [u for u in users if u['user_id'] != user_id]
        bookings = [b for b in bookings if b['user_id'] != user_id]
        
        # Save changes
        self._write_csv('users', users)
        self._write_csv('bookings', bookings)
        self._write_csv('movies_showings', movies)
        return True

    # User Ban Management Methods
    def ban_user_by_email(self, email: str) -> bool:
        """Ban a user by their email address."""
        users = self._read_csv('users')
        
        user_found = False
        for user in users:
            if user['email'] == email:
                user_found = True
                user['status'] = 'banned'
                break
        
        if not user_found:
            return False
        
        self._write_csv('users', users)
        return True

    def unban_user_by_email(self, email: str) -> bool:
        """Unban a user by their email address."""
        users = self._read_csv('users')
        
        user_found = False
        for user in users:
            if user['email'] == email:
                user_found = True
                user['status'] = 'active'
                break
        
        if not user_found:
            return False
        
        self._write_csv('users', users)
        return True

    def get_banned_users(self) -> List[Dict]:
        """Get all banned users."""
        users = self._read_csv('users')
        return [u for u in users if u.get('status', 'active') == 'banned']

    def find_user_by_email(self, email: str) -> Optional[Dict]:
        """Find a user by their email address."""
        users = self._read_csv('users')
        for user in users:
            if user['email'] == email:
                return user
        return None

    # Seat Layout and Visual Selection Methods
    def get_seat_layout(self, showing_id: str) -> Dict:
        """Get seat layout information for a showing."""
        movies = self._read_csv('movies_showings')
        bookings = self._read_csv('bookings')
        
        # Find the showing
        showing = None
        for m in movies:
            if m['id'] == showing_id:
                showing = m
                break
        
        if not showing:
            return {}
        
        # Calculate seat layout (assuming 10 seats per row)
        total_seats = int(showing['available_seats']) + sum(
            int(b['seats_booked']) for b in bookings 
            if b['showing_id'] == showing_id
        )
        
        rows = (total_seats + 9) // 10  # Round up to get number of rows
        seats_per_row = min(10, total_seats)
        
        # Get booked seats
        booked_seats = []
        for booking in bookings:
            if booking['showing_id'] == showing_id:
                booked_seats.extend(booking['seat_numbers'].split(','))
        
        # Generate seat layout
        seat_layout = {
            'rows': rows,
            'seats_per_row': seats_per_row,
            'total_seats': total_seats,
            'booked_seats': booked_seats,
            'available_count': int(showing['available_seats'])
        }
        
        return seat_layout

    def generate_seat_grid(self, total_seats: int, seats_per_row: int = 10) -> List[List[str]]:
        """Generate a grid of seat identifiers."""
        rows = (total_seats + seats_per_row - 1) // seats_per_row
        seat_grid = []
        
        seat_counter = 0
        for row in range(rows):
            row_letter = chr(65 + row)  # A, B, C, etc.
            row_seats = []
            for seat in range(seats_per_row):
                if seat_counter < total_seats:
                    seat_id = f"{row_letter}{seat + 1}"
                    row_seats.append(seat_id)
                    seat_counter += 1
                else:
                    # Add empty placeholder to maintain grid structure
                    row_seats.append("")
            
            # Only add the row if it has at least one real seat
            if any(seat for seat in row_seats):
                seat_grid.append(row_seats)
        
        return seat_grid

    def book_tickets_visual(self, user_id: str, showing_id: str, 
                           selected_seats: List[str]) -> Optional[str]:
        """Book tickets using visual seat selection."""
        movies = self._read_csv('movies_showings')
        bookings = self._read_csv('bookings')
        
        # Find the showing
        showing = None
        for m in movies:
            if m['id'] == showing_id:
                showing = m
                break
        
        if not showing:
            return None
        
        # Check if selected seats are available
        existing_bookings = [b for b in bookings if b['showing_id'] == showing_id]
        booked_seats = []
        for booking in existing_bookings:
            booked_seats.extend(booking['seat_numbers'].split(','))
        
        # Check if any selected seats are already booked
        if any(seat in booked_seats for seat in selected_seats):
            return None
        
        # Check if enough seats are available
        available_seats = int(showing['available_seats'])
        if available_seats < len(selected_seats):
            return None
        
        # Create booking
        booking_id = str(max([int(b['booking_id']) for b in bookings], default=0) + 1)
        total_price = len(selected_seats) * float(showing['price'])
        
        new_booking = {
            'booking_id': booking_id,
            'user_id': user_id,
            'showing_id': showing_id,
            'seats_booked': str(len(selected_seats)),
            'seat_numbers': ','.join(selected_seats),
            'total_price': str(total_price),
            'booking_date': datetime.datetime.now().isoformat()
        }
        
        # Update available seats
        showing['available_seats'] = str(available_seats - len(selected_seats))
        
        # Save changes
        bookings.append(new_booking)
        self._write_csv('bookings', bookings)
        self._write_csv('movies_showings', movies)
        
        return booking_id

# Initialize system if run directly
if __name__ == '__main__':
    system = CinemaSystem()