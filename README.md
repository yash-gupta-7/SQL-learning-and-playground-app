SQL Interactive Environment

A complete interactive SQL learning and playground application built with Python, Gradio, and MySQL. This project provides a user-friendly interface to manage a database, explore advanced SQL concepts, and run custom queries in an interactive playground.

Features

The Gradio web interface includes the following tabs:

1. **DATA ENTRY**  
   Add records to the database interactively. You can add students, courses, and enrollments.
2. **CRUD TABS**  
   Perform basic Read, Update, and Delete operations on the student records and view joined data.
3. **SQL CONCEPT EXPLORER**  
   A learning section to explore and execute common SQL queries, including `INNER JOIN`, `LEFT JOIN`, `GROUP BY`, `SUBQUERY`, and `WINDOW FUNCTION`. It displays the query and the resulting data table side-by-side.
4. **SQL PLAYGROUND**  
   A sandbox environment to write and execute your own custom SQL queries directly against the database and see the output in real-time. Catch errors directly in the provided Log/Error box.
5. **SQL MASTERY GUIDE**  
   A basic markdown cheatsheet outlining essential SQL commands.

Prerequisites

Before running the app, ensure you have the following installed:
- Python 3.x
- MySQL Server

The following Python libraries are required:
- `gradio`
- `pandas`
- `mysql-connector-python`

You can typically install these via `pip`:
```bash
pip install gradio pandas mysql-connector-python
```

Database Configuration

The application expects a local MySQL database setup. You may need to review or update the connection credentials in `db.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qwertyuiop' # Update this according to your MySQL installation
}
```

The script will automatically create the required database (`sql_teaching`) and tables (`students`, `courses`, `enrollments`) on initialization.

Application Structure

- **`app.py`**: The frontend built using Gradio. It defines the layout, tabs, state management, and wires frontend inputs to the backend database queries. Also expects a `branding.json` for application title and slogan.
- **`db.py`**: The backend handling the MySQL connections and executing SQL operations. Also uses Pandas to structure the returned query data for display in Gradio DataFrames.
- **`branding.json`**: Make sure you have this JSON file in the same directory containing keys like `brand['organizationShortName']` and `brand['slogan']`.

How to Run

1. Ensure MySQL server is running locally.
2. Update the `DB_CONFIG` credentials in `db.py`.
3. Put `branding.json` in the working directory.
4. Run the application:

```bash
python app.py
```

The application will start a local Gradio server and provide a URL (usually `http://127.0.0.1:7860/`) to access the interface in your web browser.
