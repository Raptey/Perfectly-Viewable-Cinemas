# Perfectly Viewable Cinemas

## Project Name

Perfectly Viewable Cinemas (PVC)

## Synopsis (Derived from Source Code Only)

Perfectly Viewable Cinemas is a modern cinema management and ticket booking system built with object-oriented design principles and CSV-based persistence, offering two interaction modes:

1. A command-line (CLI) interface for system administrators to manage platform-wide operations including:
   - Initialization/reset of core CSV datasets (movies/showings, users, admins, bookings)
   - Complete CRUD operations for theatre admin accounts (create, view, modify, delete)
   - Comprehensive user account management (view, modify, delete with cascading booking cleanup)
   - User ban/unban lifecycle management with email-based user lookup and status inspection

2. A class-based Streamlit GUI (`CinemaGUI`) providing rich visual interfaces for theatre admins and end-users:
   - User registration and authentication with secure password handling
   - Enhanced movie browsing with poster image display and expandable movie cards
   - Interactive visual seat selection grid with real-time availability indicators (🟢 available, 🔴 booked, 🟡 selected)
   - Streamlined booking workflow with seat conflict detection and atomic inventory updates
   - Personal booking management with cancellation and automatic seat restoration
   - Theatre admin dashboard for adding movies with poster URLs and viewing revenue analytics

### Core Features

- **Object-Oriented Architecture**: GUI refactored into `CinemaGUI` class with organized method structure and improved maintainability
- **Role-Based Access Control**: System admin (CLI-only), theatre admin, and regular user roles with appropriate interface restrictions
- **Enhanced Visual Experience**: Movie poster image integration, emoji-based seat indicators, and modern Material Design icons
- **CSV-Backed Persistence**: No external database dependencies with structured file-based storage
- **Advanced Security**: Salted HMAC-SHA256 password hashing with secure comparison and user ban enforcement
- **Interactive Seat Selection**: Dynamic grid generation with real-time state management and visual feedback
- **Booking Integrity**: Comprehensive conflict detection, atomic seat count updates, and cascading cleanup operations
- **Theatre Revenue Analytics**: Revenue tracking and booking aggregation for theatre-specific insights
- **Session State Management**: Persistent user sessions and seat selection state across page interactions

### User Types and Access Levels

The system supports three distinct user types, each with specific capabilities and interface access:

#### 1. System Administrator

- **Access**: Command-line interface (CLI) only
- **Capabilities**:
  - Initialize and reset all CSV data files
  - Full CRUD operations on theatre admin accounts
  - Complete user account management (view, modify, delete)
  - User ban/unban management with email-based lookup
  - System-wide oversight and data integrity management
- **Authentication**: Username/password with system-level privileges

#### 2. Theatre Administrator

- **Access**: Streamlit GUI with administrative dashboard
- **Capabilities**:
  - Add new movie showings with complete metadata (title, genre, duration, showtime, pricing, poster URLs)
  - View all bookings specific to their assigned theatre
  - Monitor theatre revenue and booking analytics
  - Manage theatre-specific movie inventory and scheduling
- **Authentication**: Username/password linked to specific theatre ID

#### 3. Regular User (Customer)

- **Access**: Streamlit GUI with customer-focused interface
- **Capabilities**:
  - Browse available movies across all theatres with rich visual display
  - Interactive seat selection using visual grid interface
  - Book tickets with real-time seat availability checking
  - View personal booking history with detailed information
  - Cancel bookings with automatic seat restoration
  - Account registration and profile management
- **Authentication**: Username/password with email verification

### Data Model (CSV Files)

- movies_showings.csv: id, title, genre, duration, theatre_id, showtime, available_seats, price, image_url
- users.csv: user_id, username, password, salt, email, status (active|banned)
- admins.csv: admin_id, username, password, salt, type (system|theatre), theatre_id
- bookings.csv: booking_id, user_id, showing_id, seats_booked, seat_numbers, total_price, booking_date (ISO timestamp)

### Security Considerations

- **Password Security**: All passwords stored as salted HMAC-SHA256 hashes with cryptographically secure random salt generation
- **Authentication Enforcement**: Ban status checking prevents banned users from accessing the system
- **Session Management**: Streamlit session state maintains user context without persistent tokens
- **Input Sanitization**: Form validation and type checking for user inputs across both CLI and GUI interfaces
- **Role Separation**: System administrators restricted to CLI interface, preventing GUI access to administrative functions

---

Generated automatically from code inspection (cli.py, gui.py, handler.py, crypto.py) without referencing README content.
