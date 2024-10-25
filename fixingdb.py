import sqlite3

# Path to the SQLite database
db_path = "training_data.db"

def create_parents_data_table():
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create the 'parents_data' table with all necessary columns, including 'microciclos'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parents_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_padre TEXT NOT NULL,
                nombre_jugador TEXT NOT NULL,
                notas TEXT,
                microciclos TEXT
            );
        """)
        print("Table 'parents_data' created successfully or already exists.")

        # Commit the changes and close the connection
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Call the function to create the table
create_parents_data_table()
