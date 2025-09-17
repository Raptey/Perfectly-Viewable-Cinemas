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
        """Initialize CSV files with headers if they don't exist."""
        headers = {
            'movies_showings': ['id', 'title', 'genre', 'duration', 'theatre_id', 'showtime', 'available_seats', 'price'],
            'users': ['user_id', 'username', 'password', 'salt', 'email'],
            'admins': ['admin_id', 'username', 'password', 'salt', 'type', 'theatre_id'],
            'bookings': ['booking_id', 'user_id', 'showing_id', 'seats_booked', 'seat_numbers', 'total_price', 'booking_date']
        }
        
        for file_key, filename in self.csv_files.items():
            if not os.path.exists(filename):
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers[file_key])

    def _read_csv(self, file_key: str) -> List[Dict]:
        """Read a CSV file and return list of dictionaries."""
        data = []
        with open(self.csv_files[file_key], 'r', newline='') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return data

    def _write_csv(self, file_key: str, data: List[Dict]):
        """Write list of dictionaries to CSV file."""
        if not data:
            return
        
        with open(self.csv_files[file_key], 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

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
            'email': email
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
        
        # Find the booking
        booking = None
        for b in bookings:
            if b['booking_id'] == booking_id and b['user_id'] == user_id:
                booking = b
                break
        
        if not booking:
            return False
        
        # Update movie seats
        for movie in movies:
            if movie['id'] == booking['showing_id']:
                movie['available_seats'] = str(int(movie['available_seats']) + 
                                             int(booking['seats_booked']))
                break
        
        # Remove booking
        bookings = [b for b in bookings if b['booking_id'] != booking_id]
        
        # Save changes
        self._write_csv('bookings', bookings)
        self._write_csv('movies_showings', movies)
        return True

    def get_theatre_bookings(self, theatre_id: str) -> List[Dict]:
        """Get all bookings for a specific theatre."""
        bookings = self._read_csv('bookings')
        movies = self._read_csv('movies_showings')
        
        theatre_movies = {m['id']: m for m in movies if m['theatre_id'] == theatre_id}
        return [b for b in bookings if b['showing_id'] in theatre_movies]

# Initialize system if run directly
if __name__ == '__main__':
    system = CinemaSystem()