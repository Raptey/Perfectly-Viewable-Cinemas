# Perfectly-Viewable-Cinemas (PVC) — README

Version: 2.0.1
Last updated: 2025-09-17

## Overview

Perfectly-Viewable-Cinemas (PVC) is a lightweight, CSV-backed cinema management and ticket booking system built in Python. It provides **both CLI and Streamlit-based GUI interfaces**. This version introduces a **merged ********`movies_showings.csv`******** file** (instead of separate `movies.csv` and `showings.csv`) to simplify management and avoid conflicts. The system supports three roles with distinct permissions:

* **Users**: Can register, log in, edit profile info, browse movies and showings, select seats, make (mock) payments, book tickets, and manage bookings (cancel or view).
* **Theatre Admins**: Can add, edit, and remove movies and their showings, configure seat capacity and layouts, set ticket prices, and view bookings specific to their theatre.
* **System Admins**: Can manage users (edit/remove), ban specific email addresses from registering, initialize CSV files, and perform maintenance tasks. For security and simplicity, these operations are CLI-only.

The project is designed for learning, small-scale prototyping, and lightweight deployment without external databases.

---

## Features

### Core Operations (CRUD)

PVC is built around five key concepts:

* **Addition of data**: Movies, users, showings, bookings.
* **Removal of data**: Delete movies, cancel bookings, remove users.
* **Modification of data**: Update user profiles, edit movies, adjust showtimes.
* **System Admin Management**: Ban emails, manage users, reset data.
* **Initialization**: Create required CSV files with headers.

### Seat Selection System

When a theatre admin adds a new movie/showing, they must provide the number of seats available. The system automatically generates a **seat grid** corresponding to this capacity (e.g., 5x10 grid for 50 seats). Users booking tickets can:

* View the grid of seats (available vs booked).
* Select specific seats instead of only entering a seat count.
* See updated availability after booking.

Bookings store selected seat identifiers (e.g., `A1`, `A2`, `B3`). This prevents double-booking and provides transparency for both users and admins.

### Payment Simulation

* Each movie showing includes a **ticket price** set by the theatre admin when creating the showing.
* During booking, the system calculates the total price based on selected seats.
* Users proceed through a **mock payment flow** (no real transactions). The result is logged as a successful or failed simulated payment.

### CLI Features

* Login/register as user, theatre admin, or system admin.
* Users: browse movies, select seats from a grid, view prices, simulate payment, book tickets, manage bookings.
* Theatre admins: add/edit/remove movies and showings, configure seat layouts, set ticket prices, monitor bookings.
* System admins: edit/remove users, ban emails, initialize CSVs.

### GUI Features (Streamlit)

* A **single unified interface** with navigation components (instead of separate pages).
* Users: view movies, see ticket prices, choose seats via a grid, simulate payment, book tickets, view personal bookings, edit profile.
* Theatre admins: add/edit/remove movies, manage seat layouts, set ticket prices, view theatre bookings.
* System admin: CLI-only access (not available in GUI).

---

## File Structure

```
PVC/
├── cli.py              # Command-Line Interface
├── gui.py              # Streamlit GUI
├── handler.py          # Business logic & CSV helpers
├── movies_showings.csv # Unified movies & showings file
├── users.csv           # User accounts
├── admins.csv          # Admin accounts (system/theatre)
└── bookings.csv        # Ticket bookings
```

---

## Data Model

### movies\_showings.csv

Stores both movies and their scheduled showings, including seat capacity and ticket price.

```
id,title,genre,duration,theatre_id,showtime,available_seats,price
1,Avatar: The Way of Water,Sci-Fi,192,1,18:00,50,300
2,The Grand Budapest Hotel,Comedy,99,1,20:15,40,250
```

### users.csv

```
user_id,username,password,email
1,demo_user,password123,demo@email.com
```

### admins.csv

```
admin_id,username,password,type,theatre_id
1,system_admin,admin123,system,
2,theatre_admin1,theatre123,theatre,1
```

### bookings.csv

```
booking_id,user_id,showing_id,seats_booked,seat_numbers,total_price,booking_date
1,1,1,2,"A1,A2",600,2025-09-12T10:22:00
```

---

## Installation & Setup

### Prerequisites

* Python 3.8+
* pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Initialize CSV Files

On first run, let the system create CSVs with headers:

```bash
python handler.py
```

---

## Running the System

### CLI

```bash
python cli.py
```

* Text-based menus for user, theatre admin, and system admin.

### GUI

```bash
streamlit run gui.py
```

* Opens a web interface in your browser with a unified interface (role-based options visible through navigation and menus).

---

## Example Workflows

### User

1. Register an account.
2. Log in.
3. Browse available movies and showtimes with ticket prices.
4. Select seats from the grid.
5. Confirm booking and complete simulated payment.
6. View or cancel bookings.

### Theatre Admin

1. Log in.
2. Add a new movie with showtime, seat capacity, and ticket price.
3. Configure seat grid (rows x columns).
4. Edit or remove existing movies.
5. View theatre bookings and revenue summaries.

### System Admin (CLI only)

1. Log in.
2. Remove or edit users.
3. Ban an email.
4. Re-initialize CSVs if needed.

---

## Developer Notes

* All business logic goes through `handler.py`. Never manipulate CSVs directly.
* To extend the project:

  * Add functions in `handler.py`.
  * Update CLI/GUI to use new functions.
* Recommended improvements:

  * Switch to SQLite for concurrency.
  * SHA 256 passwords.
  * Add automated tests.
  * Enhance seat map rendering in GUI with clickable grids.
  * Expand simulated payment to include multiple payment methods.

---

## Troubleshooting

* **CSV headers mismatch**: Delete corrupted CSVs and re-run initialization.
* **Streamlit errors**: Ensure `streamlit` is installed.
* **Booking fails**: Check seat availability and seat selection in `movies_showings.csv`.

---

## License

This project is licensed under the MIT License. See LICENSE for details.
