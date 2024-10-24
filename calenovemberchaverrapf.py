import streamlit as st
import sqlite3
import pandas as pd

# Function to create/connect to the SQLite database
def init_db():
    conn = sqlite3.connect('training_data.db')  # SQLite database stored in the same directory
    cursor = conn.cursor()
    # Create a table to store parents' submissions if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parents_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_padre TEXT,
        nombre_jugador TEXT,
        notas TEXT,
        microciclo_1 TEXT,
        microciclo_2 TEXT,
        microciclo_3 TEXT,
        microciclo_4 TEXT,
        microciclo_5 TEXT
    )
    ''')
    conn.commit()
    return conn

# Function to save data to SQLite database
def save_to_db(nombre_padre, nombre_jugador, notas, microciclos):
    conn = init_db()
    cursor = conn.cursor()
    # Convert microciclos (dictionaries) to strings for storage
    microciclo_1 = str(microciclos['microciclo_1'])
    microciclo_2 = str(microciclos['microciclo_2'])
    microciclo_3 = str(microciclos['microciclo_3'])
    microciclo_4 = str(microciclos['microciclo_4'])
    microciclo_5 = str(microciclos['microciclo_5'])
    
    # Insert the data into the table
    cursor.execute('''
    INSERT INTO parents_data (nombre_padre, nombre_jugador, notas, microciclo_1, microciclo_2, microciclo_3, microciclo_4, microciclo_5)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
    (nombre_padre, nombre_jugador, notas, microciclo_1, microciclo_2, microciclo_3, microciclo_4, microciclo_5))
    conn.commit()
    conn.close()

# Function to fetch data from SQLite for visualization
def fetch_data():
    conn = sqlite3.connect('training_data.db')
    df = pd.read_sql_query("SELECT * FROM parents_data", conn)
    conn.close()
    return df

# Function to display microcycles data from SQLite in the admin view
def visualize_microciclos(data):
    for _, row in data.iterrows():
        st.subheader(f"Parent: {row['nombre_padre']}, Player: {row['nombre_jugador']}")
        for i in range(1, 6):
            microciclo = eval(row[f'microciclo_{i}'])  # Convert string back to dictionary
            selected_dates = [date for date, chosen in microciclo.items() if chosen]
            if selected_dates:
                st.markdown(f"**Microciclo #{i}:** {', '.join(selected_dates)}")
            else:
                st.markdown(f"**Microciclo #{i}:** No dates selected.")
        st.markdown(f"**Notas del Padre:** {row['notas']}")
        st.write("---")

# Admin access section to view all data
def admin_access():
    st.subheader("Admin Access")
    password = st.text_input("Enter password", type="password")
    
    if st.button("Login"):
        if password == "chave4043":
            st.success("Access granted!")
            data = fetch_data()
            if not data.empty:
                visualize_microciclos(data)
            else:
                st.info("No records found in the database.")
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
        Generalmente, dura de 1 a 2 semanas y se enfoca en objetivos físicos o tácticos específicos.
    """)
    st.info("Por favor seleccione los días disponibles para cada microciclo.")

    # Microcycle selections
    st.subheader("Seleccione Fechas de Entrenamiento Disponibles")
    microciclos = {}

    # Microciclo 1
    st.markdown("<h4 style='color: lightblue;'>Microciclo #1</h4>", unsafe_allow_html=True)
    microciclos['microciclo_1'] = {
        "29 de octubre (martes)": st.checkbox("29 de octubre (martes)", key="microciclo_1_1"),
        "30 de octubre (miércoles)": st.checkbox("30 de octubre (miércoles)", key="microciclo_1_2"),
        "1 de noviembre (viernes)": st.checkbox("1 de noviembre (viernes)", key="microciclo_1_3"),
        "2 de noviembre (sábado)": st.checkbox("2 de noviembre (sábado)", key="microciclo_1_4"),
    }

    # Microciclo 2
    st.markdown("<h4 style='color: lightcoral;'>Microciclo #2</h4>", unsafe_allow_html=True)
    microciclos['microciclo_2'] = {
        "4 de noviembre (lunes)": st.checkbox("4 de noviembre (lunes)", key="microciclo_2_1"),
        "5 de noviembre (martes)": st.checkbox("5 de noviembre (martes)", key="microciclo_2_2"),
        "7 de noviembre (jueves)": st.checkbox("7 de noviembre (jueves)", key="microciclo_2_3"),
        "8 de noviembre (viernes)": st.checkbox("8 de noviembre (viernes)", key="microciclo_2_4"),
    }

    # Additional microcycles (3, 4, 5) follow the same structure...

    # Notes field
    st.subheader("Notas o Mensajes para el Entrenador")
    notas = st.text_area("Escriba sus notas o mensajes aquí:")

    # Submit button
    if st.button("Enviar"):
        if nombre_padre and nombre_jugador:
            save_to_db(nombre_padre, nombre_jugador, notas, microciclos)
            st.success("¡Información enviada con éxito!")
        else:
            st.error("Por favor, ingrese el nombre del padre y del jugador.")

# Main function
def main():
    st.title("Sistema de Gestión de entrenamientos Octubre-Noviembre")
    
    # Choose between data input or admin access
    menu = ["Formulario Padre", "Acceso Admin"]
    choice = st.sidebar.selectbox("Seleccione una opción", menu)
    
    if choice == "Formulario Padre":
        informacion_padre_y_calendario()
    elif choice == "Acceso Admin":
        admin_access()

if __name__ == "__main__":
    main()
