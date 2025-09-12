# Perfectly-Viewable-Cinemas — Project Report

Version: 1.0.0
Last updated: 2025-09-12

Table of contents
-----------------
- Executive Summary
- Goals and Scope
- System Overview and Architecture
- Data Model (CSV formats and examples)
- Core Components and Key Functions
- CLI: Walkthrough + Example Sessions (detailed)
- GUI (Streamlit): Screens, interactions, example output
- Testing and Validation
- Developer Notes: How to extend, add features, and run locally
- Troubleshooting & Common Errors
- Roadmap and Future Work
- Appendix: Sample files, API surface, and quick reference


Executive summary
-----------------
Perfectly-Viewable-Cinemas (PVC) is a lightweight movie booking system implemented in Python. It provides both a Command-Line Interface (CLI) and a Streamlit-based Graphical User Interface (GUI). The project stores data in CSV files (no external database required) and is suitable as a learning project or prototype for small cinemas.

This document serves as a detailed project report and developer guide. It documents the data model, expected CSV structures, examples of usage, internal function contracts, and diagnostics for common runtime errors. If you maintain or extend PVC, this README should be the single source of truth for expected file formats and runtime behavior.


Goals and scope
---------------
- Provide a simple ticket booking flow (view movies -> select showing -> book seats).
- Allow theatre admins to add movies and showings, and to view bookings for their theatre.
- Provide a GUI using Streamlit for easy demonstration and a text-based CLI for quick testing.
- Keep persistence simple and portable using CSV files in the repository root.


System overview and architecture
--------------------------------
PVC is organized into the following layers:

- Presentation
  - `cli.py` — Single-file interactive CLI application.
  - `gui.py` — Streamlit application for a tab-based UI.

- Business logic / Service layer
  - `handler.py` — Core read/write logic, validation, and orchestration. All CSV operations should go through this module.

- Data
  - CSV files stored in the repository root. These are the source of truth: `movies.csv`, `showings.csv`, `theatres.csv`, `users.csv`, `admins.csv`, `bookings.csv`.

This architecture keeps the UI thin (presentation) and concentrates domain logic in `handler.py`. When adding new UIs, reuse the `handler.py` functions.


Data model (CSV formats and examples)
-----------------------------------
All CSV files are comma-separated, include a header row, and use simple string fields. IDs are strings to preserve portability (you can use numeric-looking strings like "1").

## 1) movies.csv

Columns: movie_id,title,genre,duration

### Example:

movie_id,title,genre,duration

1,Avatar: The Way of Water,Sci-Fi,192

2,The Grand Budapest Hotel,Comedy,99


## 2) showings.csv

Columns: showing_id,movie_id,theatre_id,showtime,available_seats

### Example:

showing_id,movie_id,theatre_id,showtime,available_seats
1,1,1,18:00,50
2,2,1,20:15,40

> Notes: `movie_id` must reference an existing `movie_id` from `movies.csv`. `theatre_id` must exist in `theatres.csv`.


## 3) theatres.csv

Columns: theatre_id,name,location,total_seats

### Example:

theatre_id,name,location,total_seats
1,PVR Cinemas,Mall Road,100
2,Central Screens,City Center,80


## 4) users.csv

Columns: user_id,username,password,email

### Example:

user_id,username,password,email
1,demo_user,password123,demo@email.com


## 5) admins.csv

Columns: admin_id,username,password,type,theatre_id

### Example:

admin_id,username,password,type,theatre_id
1,system_admin,admin123,system,
2,theatre_admin1,theatre123,theatre,1

Notes: `type` is either `system` or `theatre`. `theatre_id` is optional (empty) for system admins.


## 6) bookings.csv

Columns: booking_id,user_id,showing_id,seats_booked,booking_date

### Example:

booking_id,user_id,showing_id,seats_booked,booking_date
1,1,1,2,2025-09-12T10:22:00


# Core components and key functions

All data access is centralized in `handler.py`. The following functions are the primary surface expected by `cli.py` and `gui.py`.

- initialize_csv_files(): Ensures CSV files exist with headers and sample rows. Run on startup.
- get_movies() -> list[dict]: Returns all movies. Each movie dict has keys: movie_id, title, genre, duration.
- add_movie(title, genre, duration) -> (bool, str): Creates a new movie row and returns (success, message).
- get_showings() -> list[dict]: Returns all showings as dictionaries.
- add_showing(movie_id, theatre_id, showtime, available_seats) -> (bool, str): Adds a new showing; validates that movie and theatre exist.
- book_ticket(user_id, showing_id, seats) -> (bool, str|booking_id): Attempts to book seats for a showing; returns booking id on success.
- get_user_bookings(user_id) -> list[dict]
- get_theatre_bookings(theatre_id) -> list[dict]
- get_theatres(), get_users(), get_admins() — simple readers.

If you change column names in CSV files, update `handler.py` immediately to match them.


CLI: Walkthrough + Example Sessions (detailed)
---------------------------------------------
Start the CLI (from the repository root):

```powershell
python cli.py
```

Sample session: theatre admin adds a movie and a showing

### Example input and resulting prompts (user input in bold):
```py
==================================================
    Welcome to PVC - Perfectly Viewable Cinemas
==================================================

=== MAIN MENU ===
1. User Login
2. User Registration
3. Admin Login
4. Exit
Enter your choice (1-4): 3

=== ADMIN LOGIN ===
Username: theatre_admin1
Password: theatre123
Welcome, theatre_admin1! (theatre admin)

=== THEATRE ADMIN MENU ===
1. View Available Movies
2. Add Movie
3. View Theatre Bookings
4. Logout
Enter your choice (1-4): 2

=== ADD MOVIE ===
Movie Title: Lokah
Genre: Sci fi
Duration (minutes): 150
Showtime (HH:MM): 18:00
Available Seats: 50
Movie 'Lokah' added successfully (id: 3).
Showing added successfully (id: 3) for theatre 1.

Notes about what happens behind the scenes:
- `add_movie()` creates a new `movie_id` (incremental). It writes to `movies.csv`.
- `add_showing()` creates a `showing_id`, validates `movie_id` and `theatre_id`, and writes to `showings.csv`.


CLI: Booking example

- User logs in
- User selects showing 3 (Lokah at 18:00)
- User requests 2 seats
- System checks available_seats, decrements it, writes booking row to `bookings.csv`, and returns booking id.

Example output on successful booking:

Booking successful! Booking ID: 4
```

GUI (Streamlit): Screens, interactions, example output
---------------------------------------------------
Run the GUI with:

```powershell
streamlit run gui.py
```

Main GUI tabs and how they map to functionality:
- Login — Accepts username/password and sets `st.session_state['user']`.
- Register — Registers a new user.
- Movies — Shows a table of showings with movie and theatre names substituted.
- Book Ticket — Allows a logged-in user to pick a showing and number of seats.
- My Bookings — Shows bookings for logged-in user.
- Admin: Movies — For theatre admins; allows adding a showing for an existing movie.
- Admin: Bookings — Shows bookings for the theatre admin's theatre.

Example Streamlit table (Available Movies tab):

showing_id | movie_id | theatre_id | showtime | available_seats | Movie                         | Theatre
-----------------------------------------------------------------------------------------------
1          | 1        | 1          | 18:00    | 50              | Avatar: The Way of Water      | PVR Cinemas
3          | 3        | 1          | 18:00    | 50              | Lokah                         | PVR Cinemas


Testing and validation
----------------------
Unit testing approach:
- Focus on `handler.py` functions. Small, isolated tests can validate CSV reads and writes.
- Example test cases:
  - Add a movie -> new row appended with unique id.
  - Add a showing with invalid `movie_id` -> returns error and does not write.
  - Book more seats than available -> returns error and does not write.

Manual smoke tests:
- Run CLI and perform the end-to-end flows (admin add movie -> add showing -> user books)
- Run Streamlit GUI and exercise tabs.


Developer notes and how to run locally
-------------------------------------
Prerequisites
- Python 3.8+
- (Optional) Virtual environment

Install dependencies (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

Start CLI:

```powershell
python cli.py
```

Start GUI:

```powershell
streamlit run gui.py
```

Programming contracts (quick reference)
- add_movie(title, genre, duration) -> (bool, message)
- add_showing(movie_id, theatre_id, showtime, available_seats) -> (bool, message)
- book_ticket(user_id, showing_id, seats) -> (bool, booking_id|string)

Always treat these functions as atomic: they must validate inputs, update CSV rows, and return a clear success/failure tuple.


Troubleshooting & common errors
-------------------------------
1) TypeError: add_movie() takes 3 positional arguments but 6 were given
- Cause: UI (CLI) was passing showtime and seats to `add_movie`. Fix: split responsibility — call `add_movie()` to create a movie and then `add_showing()` to add a showing.

2) Streamlit import errors
- Fix: `pip install streamlit` in your active environment.

3) Pandas import errors
- Fix: `pip install pandas`.

4) CSV header mismatches
- If you update `handler.py` to expect different column names, delete the CSV files and let `initialize_csv_files()` recreate them with the correct headers (or edit the headers manually).


Roadmap and future work
-----------------------
- Migrate from CSV to a lightweight database (SQLite) to avoid race conditions and make concurrent access safer.
- Add authentication with hashed passwords (bcrypt) instead of storing plaintext.
- Add unit tests (pytest) and a CI workflow.
- Add seat maps per theatre with seat labels and selections.


Appendix: sample CSV contents (full snapshot)
-------------------------------------------
### movies.csv

movie_id,title,genre,duration
1,Avatar: The Way of Water,Sci-Fi,192
2,The Grand Budapest Hotel,Comedy,99
3,Lokah,Sci-Fi,150

### showings.csv

showing_id,movie_id,theatre_id,showtime,available_seats
1,1,1,18:00,50
2,2,1,20:15,40
3,3,1,18:00,50

### bookings.csv

booking_id,user_id,showing_id,seats_booked,booking_date
1,1,1,2,2025-09-12T10:22:00
2,1,2,4,2025-09-12T10:25:00


Contact and license
-------------------
This project is licensed under the MIT License (see LICENSE file). For questions or contributions, open an issue or a PR on the project repository.
