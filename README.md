# Museum Database Management System

This project is a Museum Database Management System implemented in Python using MySQL. It allows users to perform various operations related to managing a museum's art collection, exhibitions, artists, and more.

## Features

- **Login System**: Users can log in with different roles (admin, data entry, guest) to perform specific actions.
- **Database Initialization**: Initialize the database using a provided SQL script.
- **Admin Console**: Admins can manage users, initialize the database, execute SQL queries, and block/unblock users.
- **Data Entry**: Users with data entry roles can insert, update, and delete tuples from various tables.
- **Guest View**: Guests can browse through the museum's collection and view information without modifying the database.

## Requirements

- Python 3.x
- MySQL

## Installation

1. Clone the repository.
2. Install the necessary Python packages: `pip install python-sql`.
3. Initialize database with the steps provided below
4. Execute the `MainApp.py` file to start the Museum Database Management System.

### Database Initialization

1. In creation.py enter the username and password for your root account in MySQL to give permission to initialize database when you start the project (option 3). This option will not work otherwise.
2. If for some reason that is not working for you you would need to initialize the database yourself by running the provided museum_db_initialization.sql script BEFORE running the application "MainApp.py" and then use one of the provided login info below

## Usage

### `creation.py`

This file contains the function to initialize the database using a provided SQL script. Enter the username and password for your MySQL root account to grant permission for database initialization.

### `MainApp.py`

#### Main Functionality

The `MainApp.py` file contains the main functionality of the Museum Database Management System.

1. **Login System**: Allows users to log in with different roles and perform specific actions.
2. **Admin Console**: Admins can manage users, execute SQL queries, and more.
3. **Data Entry**: Perform operations like inserting, updating, and deleting tuples.
4. **Guest View**: Allows guests to browse through the museum's collection.

## Database Login Information

If you've initialized the database using the provided SQL script, you can use the following login information for different roles:

### Login Info

- **db_admin**
  - Username: administrator
  - Password: password

- **data_access**
  - Username: data_entry
  - Password: password

- **read_access**
  - Username: guest
  - Password: [Leave Blank]

Please ensure you use the appropriate login credentials based on your role in the application.

