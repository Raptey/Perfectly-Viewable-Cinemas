# Perfectly-Viewable-Cinemas

## Overview
Perfectly-Viewable-Cinemas (PVC) is a movie booking system that supports both a Command-Line Interface (CLI) and a Streamlit-based Graphical User Interface (GUI). The system allows users to book tickets, view available movies, and manage bookings. Admins can manage movies, showings, and view statistics.

---

## Features
### User Features:
- **View Available Movies**: Browse movies and their showings.
- **Book Tickets**: Reserve seats for a specific showing.
- **View Bookings**: Check your booking history.

### Admin Features:
- **Add Movies**: Add new movies to the catalog.
- **Add Showings**: Schedule showings for movies in specific theatres.
- **View Theatre Bookings**: View bookings for a specific theatre.
- **System Statistics**: View overall system statistics (System Admin only).

---

## Project Structure
```
Perfectly-Viewable-Cinemas/
├── admins.csv          # Admin data
├── bookings.csv        # Booking records
├── cli.py              # Command-Line Interface
├── gui.py              # Streamlit-based GUI
├── handler.py          # Core business logic
├── movies.csv          # Movie catalog
├── showings.csv        # Movie showings
├── theatres.csv        # Theatre data
├── users.csv           # User data
└── README.md           # Project documentation
```

---

## Setup Instructions
### Prerequisites
- Python 3.8+
- `pip` (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Raptey/Perfectly-Viewable-Cinemas.git
   cd Perfectly-Viewable-Cinemas
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
### Command-Line Interface (CLI)
1. Run the CLI:
   ```bash
   python cli.py
   ```
2. Follow the on-screen menu to log in, view movies, book tickets, etc.

### Streamlit GUI
1. Run the Streamlit app:
   ```bash
   streamlit run gui.py
   ```
2. Open the provided URL in your browser to access the GUI.

---

## Data Model
### Movies (`movies.csv`):
| Column      | Description              |
|-------------|--------------------------|
| `movie_id`  | Unique ID for the movie  |
| `title`     | Movie title              |
| `genre`     | Movie genre              |
| `duration`  | Duration in minutes      |

### Showings (`showings.csv`):
| Column         | Description                     |
|----------------|---------------------------------|
| `showing_id`   | Unique ID for the showing       |
| `movie_id`     | References `movie_id` in movies |
| `theatre_id`   | Theatre where the movie is shown|
| `showtime`     | Showtime (HH:MM)               |
| `available_seats` | Number of available seats    |

---

## Developer Notes
### Adding a New Feature
1. Add the core logic to `handler.py`.
2. Update `cli.py` for CLI support.
3. Update `gui.py` for GUI support.

### Testing
- Ensure all CSV files are initialized using the `initialize_csv_files` function in `handler.py`.
- Use the CLI or GUI to verify functionality.

---

## Troubleshooting
### Common Issues
1. **Missing Dependencies**:
   - Ensure all dependencies are installed:
     ```bash
     pip install -r requirements.txt
     ```
2. **Streamlit Import Error**:
   - Install Streamlit:
     ```bash
     pip install streamlit
     ```
3. **Pandas Import Error**:
   - Install Pandas:
     ```bash
     pip install pandas
     ```

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contact
For questions or contributions, please contact the repository owners at [Raptey](https://github.com/Raptey).