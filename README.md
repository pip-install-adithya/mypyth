```markdown
# School Timetable Management System

This project is a School Timetable Management System that helps in generating and managing weekly school timetables. It uses a MySQL database to store subject data and a Tkinter GUI for user interaction.

## Features

- Create and manage main and elective subjects
- Generate a weekly timetable
- Edit specific periods in the timetable
- Confirm and display the finalized timetable
- Uses a GUI for easy interaction

## Requirements

- Python 3.x
- MySQL Connector for Python
- Tkinter (usually included with Python)
- A running MySQL server

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/school-timetable.git
   cd school-timetable
   ```

2. Install required packages:

   You may need to install the MySQL Connector if it's not already installed:

   ```bash
   pip install mysql-connector-python
   ```

3. Set up the MySQL database:

   - Update the MySQL credentials in the code (username, password).
   - Run the initial setup code to create the database and tables.

## Usage

1. Run the application:

   ```bash
   python your_script_name.py
   ```

2. Use the GUI to:
   - Generate a new timetable
   - Edit periods as needed
   - Confirm and view the finalized timetable

## Database Structure

The application uses two main tables:

- `main_subjects`
  - `id`: Auto-incremented primary key
  - `subject_name`: Name of the main subject
  - `weekly_frequency`: Number of classes per week

- `elective_subjects`
  - `id`: Auto-incremented primary key
  - `subject_name`: Name of the elective subject
  - `weekly_frequency`: Number of classes per week

## Contributing

Feel free to submit pull requests or report issues. Your contributions are welcome!

Feel free to customize any sections as needed!
