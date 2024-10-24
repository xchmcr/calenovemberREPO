import streamlit as st
import sqlite3
import os

# Define the path to the SQLite database file
db_path = os.path.join(os.path.dirname(__file__), 'training_data.db')

# Function to connect to the local SQLite database
def connect_to_sqlite():
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        st.error(f"Error connecting to the SQLite database: {e}")
        return None

# Function to create the table if it doesn't exist
def create_table():
    conn = connect_to_sqlite()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS fridayparents (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre_padre TEXT,
                            nombre_jugador TEXT,
                            notas TEXT,
                            microciclos TEXT
                        )''')
        conn.commit()
        conn.close()

# Save data to SQLite database
def save_to_sqlite(nombre_padre, nombre_jugador, notas, microciclos):
    conn = connect_to_sqlite()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO fridayparents (nombre_padre, nombre_jugador, notas, microciclos) VALUES (?, ?, ?, ?)",
                       (nombre_padre, nombre_jugador, notas, str(microciclos)))
        conn.commit()
        conn.close()
        st.success("¡Información guardada exitosamente!")

# Function to display data from SQLite in an admin view
def visualize_microciclos(data):
    for parent in data:
        st.subheader(f"Parent: {parent[1]}, Player: {parent[2]}")
        
        # Display the microciclos (retrieved as a string)
        microciclos = eval(parent[4])  # Convert string back to dictionary
        
        for cycle, dates in microciclos.items():
            selected_dates = [date for date, chosen in dates.items() if chosen]
            if selected_dates:
                st.markdown(f"**{cycle.capitalize()}:** {', '.join(selected_dates)}")
            else:
                st.markdown(f"**{cycle.capitalize()}:** No dates selected.")
        
        # Display notes field
        st.markdown(f"**Notas del Padre:** {parent[3]}")
        st.write("---")

# Function to display all data from SQLite in an admin view
def display_all_data():
    conn = connect_to_sqlite()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fridayparents")
        data = cursor.fetchall()
        conn.close()
        if data:
            visualize_microciclos(data)
        else:
            st.info("No records found in the database.")

# Admin access section
def admin_access():
    st.subheader("Admin Access")
    password = st.text_input("Enter password", type="password")
    
    if st.button("Login"):
        if password == "chave4043":
            st.success("Access granted!")
            display_all_data()
        else:
            st.error("Incorrect password. Access denied.")

# Main form for parent to input microcycle selections
def informacion_padre_y_calendario():
    st.subheader("Ingrese Información del Padre y del Jugador")
    nombre_padre = st.text_input("Nombre del Padre")
    nombre_jugador = st.text_input("Nombre del Jugador")
    
    st.subheader("¿Qué es un Microciclo?")
    st.markdown("""
        **Un microciclo** es un período de entrenamiento a corto plazo dentro de un programa de entrenamiento general. 
        Generalmente, dura de 1 a 2 semanas y se enfoca en objetivos físicos o tácticos específicos. Para los jugadores de fútbol, 
        esto podría involucrar sesiones de resistencia, fuerza, agilidad o recuperación.
    """)

    st.info("Los días subrayados con color son los días en los que se va a entrenar, cada color corresponde a un microciclo diferente. por favor seleccionar los días en los que se encuentre disponible.")

    # Show calendar image
    st.image("https://raw.githubusercontent.com/xchmcr/calenovemberREPO/main/calendar.png", 
             caption="Calendario de Entrenamiento de Noviembre 2024", use_column_width=True)

    # Microcycle selections
    st.subheader("Seleccione Fechas de Entrenamiento Disponibles")
    
    # Create a dictionary to store microcycle data
    microciclos = {}

    st.markdown("<h4 style='color: lightblue;'>Microciclo #1</h4>", unsafe_allow_html=True)
    microciclos['microciclo_1'] = {
        "29 de octubre (martes)": st.checkbox("29 de octubre (martes)", key="microciclo_1"),
        "30 de octubre (miércoles)": st.checkbox("30 de octubre (miércoles)", key="microciclo_1_2"),
        "1 de noviembre (viernes)": st.checkbox("1 de noviembre (viernes)", key="microciclo_1_3"),
        "2 de noviembre (sábado)": st.checkbox("2 de noviembre (sábado)", key="microciclo_1_4"),
    }

    st.markdown("<h4 style='color: lightcoral;'>Microciclo #2</h4>", unsafe_allow_html=True)
    microciclos['microciclo_2'] = {
        "4 de noviembre (lunes)": st.checkbox("4 de noviembre (lunes)", key="microciclo_2_1"),
        "5 de noviembre (martes)": st.checkbox("5 de noviembre (martes)", key="microciclo_2_2"),
        "7 de noviembre (jueves)": st.checkbox("7 de noviembre (jueves)", key="microciclo_2_3"),
        "8 de noviembre (viernes)": st.checkbox("8 de noviembre (viernes)", key="microciclo_2_4"),
        "9 de noviembre (sábado)": st.checkbox("9 de noviembre (sábado)", key="microciclo_2_5"),
    }

    # Continue with other cycles...
    
    # Notes field
    st.subheader("Notas o Mensajes para el Entrenador")
    notas = st.text_area("Escriba sus notas o mensajes aquí:")

    # Submit button
    if st.button("Enviar"):
        if nombre_padre and nombre_jugador:
            save_to_sqlite(nombre_padre, nombre_jugador, notas, microciclos)
        else:
            st.error("Por favor, ingrese el nombre del padre y del jugador.")

# Main function
def main():
    st.title("Sistema de Gestión de entrenamientos Octubre-Noviembre")
    
    # Create the table on startup if it doesn't exist
    create_table()

    # Choose between data input or admin access
    menu = ["Formulario Padre", "Acceso Admin"]
    choice = st.sidebar.selectbox("Seleccione una opción", menu)
    
    if choice == "Formulario Padre":
        informacion_padre_y_calendario()
    elif choice == "Acceso Admin":
        admin_access()

if __name__ == "__main__":
    main()
