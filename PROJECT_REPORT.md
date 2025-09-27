# Perfectly Viewable Cinemas

## Project Name

Perfectly Viewable Cinemas (PVC)

## Synopsis

Perfectly Viewable Cinemas is a modern cinema management and ticket booking system built with object-oriented design principles and CSV-based persistence. It offers two interaction modes:

1. A command-line (CLI) interface for system administrators to manage platform-wide operations.
2. A class-based Streamlit GUI (`CinemaGUI`) providing visual interfaces for theatre admins and end-users.

### Core Features

* **Object-Oriented Architecture**: Organized methods in `CinemaGUI` class for maintainability
* **Role-Based Access Control**: Separate privileges for system admin, theatre admin, and user roles
* **Enhanced Visual Experience**: Movie posters, emoji seat indicators, and modern icons
* **CSV Persistence**: File-based storage without external databases
* **Advanced Security**: Salted HMAC-SHA256 password hashing with enforcement of bans
* **Interactive Seat Selection**: Dynamic grid with real-time availability
* **Booking Integrity**: Conflict detection, atomic updates, and cascading cleanup
* **Theatre Analytics**: Revenue tracking and booking aggregation
* **Session State Management**: Persistent sessions and seat state across interactions

### User Types and Access Levels

#### 1. System Administrator

* **Access**: CLI only
* **Capabilities**:

  * Initialize/reset CSV data
  * Manage theatre admin accounts
  * Manage user accounts
  * Ban/unban users
  * Ensure data integrity
* **Authentication**: Username/password with elevated privileges

#### 2. Theatre Administrator

* **Access**: Streamlit GUI (admin dashboard)
* **Capabilities**:

  * Add new movie showings with metadata
  * View bookings for their theatre
  * Monitor revenue and analytics
  * Manage theatre inventory and schedules
* **Authentication**: Username/password tied to theatre ID

#### 3. Regular User (Customer)

* **Access**: Streamlit GUI (customer interface)
* **Capabilities**:

  * Browse movies across theatres
  * Select seats with real-time availability
  * Book tickets with conflict checks
  * View and cancel bookings
  * Register and manage account
* **Authentication**: Username/password with email verification

### Data Model (CSV Files)

```
CSV Data Model
├── movies_showings.csv
│   ├── id
│   ├── title
│   ├── genre
│   ├── duration
│   ├── theatre_id
│   ├── showtime
│   ├── available_seats
│   ├── price
│   └── image_url
│
├── users.csv
│   ├── user_id
│   ├── username
│   ├── password
│   ├── salt
│   ├── email
│   └── status (active|banned)
│
├── admins.csv
│   ├── admin_id
│   ├── username
│   ├── password
│   ├── salt
│   ├── type (system|theatre)
│   └── theatre_id
│
└── bookings.csv
    ├── booking_id
    ├── user_id
    ├── showing_id
    ├── seats_booked
    ├── seat_numbers
    ├── total_price
    └── booking_date (ISO timestamp)
```

### Security Considerations

* **Password Security**: Salted HMAC-SHA256 hashes with secure random salts
* **Authentication Enforcement**: Banned users blocked from access
* **Session Management**: Streamlit session state preserves user context
* **Input Validation**: Validation and type-checking across CLI and GUI
* **Role Separation**: System admins restricted to CLI; GUI reserved for theatre admins and users
