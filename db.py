import mysql.connector
import pandas as pd

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qwertyuiop'
}

def get_connection():
    config = DB_CONFIG.copy()
    config['database'] = 'sql_teaching'
    return mysql.connector.connect(**config)

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS sql_teaching")
    conn.commit()

    cursor.close()
    conn.close()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT
           )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments(
            id INT AUTO_INCREMENT PRIMARY KEY,
            sid INT,
            cid INT,
            marks INT,
            FOREIGN KEY (sid) REFERENCES students(id) ON DELETE CASCADE,
            FOREIGN KEY (cid) REFERENCES courses(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def add_student(name, age):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()
    return "Student Added"

def add_course(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return "Course Added"

def enroll(sid, cid, marks):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO enrollments (sid, cid, marks) VALUES (%s, %s, %s)", (sid, cid, marks))
    conn.commit()
    cursor.close()
    conn.close()
    return "Enrollment Succesfull"

def update_student(id, name, age):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=%s, age=%s WHERE id=%s", (name, age, id))
    conn.commit()
    cursor.close()
    conn.close()
    return "Student Details Updated"

def delete_student(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "Student Details Deleted"

def get_join_data():
    query = """
    SELECT s.name as STUDENT , c.name as Course, e.marks
    FROM students s
    INNER JOIN enrollments e on  s.id = e.sid
    INNER JOIN courses c on  e.cid = c.id
    """

    return execute_sql(query)

def get_left_join_data():
    query = """
    SELECT s.name as student, e.marks
    FROM students s 
    LEFT JOIN enrollments e ON s.id = e.sid
    """

    return execute_sql(query)

def get_group_data():
    query = """
    SELECT age, COUNT(*) as Count 
    FROM students 
    GROUP BY age
    """
    return execute_sql(query)

def get_subquery_data():
    query = """
    SELECT name 
    FROM students 
    WHERE id in (SELECT sid FROM enrollments WHERE marks > 80)
    """
    return execute_sql(query)

def get_window_data():
    query = """
    SELECT sid, marks,
    RANK () OVER (ORDER BY marks DESC) as rankings 
    FROM enrollments
    """
    return execute_sql(query)

def execute_sql(query):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)
        return df, "Success"
    except Exception as e:
        return pd.DataFrame(),str(e)
    finally:
        conn.close()
