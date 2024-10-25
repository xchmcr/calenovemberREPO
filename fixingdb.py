import sqlite3
from sqlite3 import Error

# Path to the SQLite database
db_path = "training_data.db"

def recreate_parents_data_table():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Drop the old table if it exists
        cursor.execute("DROP TABLE IF EXISTS parents_data")

        # Create the new 'parents_data' table with the correct columns
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parents_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_padre TEXT NOT NULL,
                nombre_jugador TEXT NOT NULL,
                notas TEXT,
                microciclos TEXT
            );
        """)
        print("Table 'parents_data' has been recreated successfully.")

        # Commit the changes and close the connection
        conn.commit()

    except Error as e:
        print(f"Error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Call the function to recreate the table
recreate_parents_data_table()
