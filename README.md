# Events Organizer App
 This is a simple Events Organizer application built using the Flask web framework. 
 It allows users to register, log in, and manage their personal events and tasks independently.

## Features

 - User Authentication: Register and log in securely.
 - Task Management: Add, update, and delete personal tasks.
 - User-Specific Events: Each user manages their own events separately.
 - Flash Messages: Provides feedback to users on actions performed.
 - Responsive Design: Accessible on different devices.


## Installation
 
 ### Pre-requisites
  - Ensure you have python installed (version 3.6 or later)

 ### Steps

  1. Clone the repository:
      ```sh
      git clone `https://github.com/harizonelopez/Events-Organizer.git`
      cd Event-Organizer
      ```

  2. Create a virtual environment and activate it:
      ```sh
      python -m venv venv
      source venv/Scripts/activate  # On Mac use `source venv\bin\activate`
      ```

  3. Initialize the database:
      ```sh
      flask db init
      flask db migrate -m "Initial migration"
      flask db upgrade
      ```

## Usage

1. Run the Flask application:
    ```sh
    `python main.py` 

    OR

    `flask run` 

    OR

    `flask --app main.py run`
    ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## API Endpoints

### User  Authentication

- `POST/register`: Register a new user
- `POST/login`: Log in a user

### Task Management

- `POST/add_task`: Add a new task
- `PUT/update_task_name/<int:task_id>`: Update a task name
- `POST/update_status/<int:task_id>`: Update a task status
- `DELETE/delete_task/<int:task_id>`: Delete a task

## License

This project is licensed under the MIT License.
