import streamlit as st
import sqlite3
from sqlite3 import Error

# Function to create a connection to SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('training_data.db')
    except Error as e:
        st.error(f"Error connecting to database: {e}")
    return conn

# Save form data to SQLite
def save_to_sqlite(nombre_padre, nombre_jugador, notas, microciclos):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """INSERT INTO parents_data (nombre_padre, nombre_jugador, notas, microciclos) 
                       VALUES (?, ?, ?, ?)"""
            cursor.execute(query, (nombre_padre, nombre_jugador, notas, str(microciclos)))
            conn.commit()
            conn.close()
        except Error as e:
            st.error(f"Error saving data: {e}")

def get_all_parents():
    """Fetch all parent names from the database"""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT nombre_padre FROM parents_data")
            parents = cursor.fetchall()
            conn.close()
            return [parent[0] for parent in parents]
        except Error as e:
            st.error(f"Error fetching parent names: {e}")
            return []

def delete_record_by_name(nombre_padre):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # First verify if the record exists
            cursor.execute("SELECT COUNT(*) FROM parents_data WHERE nombre_padre = ?", (nombre_padre,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                cursor.execute("DELETE FROM parents_data WHERE nombre_padre = ?", (nombre_padre,))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                return False
        except Error as e:
            st.error(f"Error deleting data: {e}")
            return False

# Function to display data from SQLite in admin view
def visualize_microciclos(data):
    for parent in data:
        st.subheader(f"Parent: {parent[1]}, Player: {parent[2]}")
        
        # Loop through each microciclo and show selected dates
        microciclos = eval(parent[4])  # Convert string back to dict
        for cycle, dates in microciclos.items():
            selected_dates = [date for date, chosen in dates.items() if chosen]
            if selected_dates:
                st.markdown(f"{cycle.capitalize()}: {', '.join(selected_dates)}")
            else:
                st.markdown(f"{cycle.capitalize()}: No dates selected.")
        
        # Now display the notes field at the end
        st.markdown(f"Notas del Padre: {parent[3]}")
        
        st.write("---")

# Display all data from SQLite
def display_all_data():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM parents_data")
            data = cursor.fetchall()
            conn.close()
            if data:
                visualize_microciclos(data)
            else:
                st.info("No records found in the database.")
        except Error as e:
            st.error(f"Error fetching data: {e}")

# Admin access section
def admin_access():
    st.subheader("Admin Access")
    password = st.text_input("Enter password", type="password")
    
    if password == "chave4043":
        st.success("Access granted!")
        
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Current Records")
            display_all_data()
        
        with col2:
            st.subheader("Delete Records")
            # Get list of all parents
            parents = get_all_parents()
            
            if parents:
                # Create a selection box for parents
                selected_parent = st.selectbox(
                    "Select parent to delete:",
                    options=parents,
                    key="parent_select"
                )
                
                # Add a confirmation checkbox
                confirm_delete = st.checkbox("Confirm deletion", key="confirm_delete")
                
                # Delete button
                if st.button("Delete Selected Record"):
                    if confirm_delete:
                        if delete_record_by_name(selected_parent):
                            st.success(f"Successfully deleted record for {selected_parent}")
                            # Instead of experimental_rerun, just refresh the components
                            st.empty()
                            st.rerun()
                        else:
                            st.error("Failed to delete record")
                    else:
                        st.warning("Please confirm deletion by checking the box above")
            else:
                st.info("No records available to delete")
    else:
        if password:  # Only show error if password was attempted
            st.error("Incorrect password. Access denied.")

# Main form for parent to input microcycle selections
def informacion_padre_y_calendario():
    st.subheader("Ingrese Información del Padre y del Jugador")
    nombre_padre = st.text_input("Nombre del Padre")
    nombre_jugador = st.text_input("Nombre del Jugador")
    
    st.subheader("¿Qué es un Microciclo?")
    st.markdown("""
        Un microciclo es un período de entrenamiento a corto plazo dentro de un programa de entrenamiento general. 
        Generalmente, dura de 1 a 2 semanas y se enfoca en objetivos físicos o tácticos específicos.
    """)

    st.info("""Los días subrayados con color son los días en los que se va a entrenar, cada color corresponde a un microciclo diferente. Por favor seleccionar los días en los que se encuentre disponible.""")

    # Add custom HTML/CSS for the zoomable image
    st.markdown("""
        <style>
            .zoom-container {
                position: relative;
                text-align: center;
            }
            .zoom-button {
                background-color: #1E88E5;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 10px 0;
                font-size: 16px;
            }
            .zoom-button:hover {
                background-color: #1976D2;
            }
            .zoom-image {
                max-width: 100%;
                transition: transform 0.3s ease;
                cursor: zoom-in;
            }
            .zoom-image.zoomed {
                transform: scale(1.5);
                cursor: zoom-out;
            }
            @media (max-width: 768px) {
                .zoom-image.zoomed {
                    transform: scale(2);
                }
            }
        </style>
        <div class="zoom-container">
            <img src="https://raw.githubusercontent.com/xchmcr/calenovemberREPO/main/calendar.png" 
                 class="zoom-image" 
                 id="calendar-image"
                 onclick="this.classList.toggle('zoomed')"
                 alt="Calendario de Entrenamiento"
            />
            <br>
            <button class="zoom-button" onclick="document.getElementById('calendar-image').classList.toggle('zoomed')">
                👆 Click para hacer zoom
            </button>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing

    st.subheader("Por favor seleccione las fechas de entrenamiento en las que se encuentra disponible")

    microciclos = {}

    # Microciclo #1
    st.markdown("<h4 style='color: lightblue;'>Microciclo #1</h4>", unsafe_allow_html=True)
    microciclos['microciclo_1'] = {
        "28 de octubre (lunes)": st.checkbox("28 de octubre (lunes)", key="microciclo_1_1"),
        "31 de octubre (jueves)": st.checkbox("31 de octubre (jueves)", key="microciclo_1_2"),
        "1 de noviembre (viernes)": st.checkbox("1 de noviembre (viernes)", key="microciclo_1_3"),
        "2 de noviembre (sábado)": st.checkbox("2 de noviembre (sábado)", key="microciclo_1_4"),
    }

    # Microciclo #2
    st.markdown("<h4 style='color: lightcoral;'>Microciclo #2</h4>", unsafe_allow_html=True)
    microciclos['microciclo_2'] = {
        "7 de noviembre (jueves)": st.checkbox("7 de noviembre (jueves)", key="microciclo_2_1"),
        "8 de noviembre (viernes)": st.checkbox("8 de noviembre (viernes)", key="microciclo_2_2"),
        "9 de noviembre (sábado)": st.checkbox("9 de noviembre (sábado)", key="microciclo_2_3"),
    }

    # Microciclo #3
    st.markdown("<h4 style='color: orange;'>Microciclo #3</h4>", unsafe_allow_html=True)
    microciclos['microciclo_3'] = {
        "14 de noviembre (jueves)": st.checkbox("14 de noviembre (jueves)", key="microciclo_3_1"),
        "15 de noviembre (viernes)": st.checkbox("15 de noviembre (viernes)", key="microciclo_3_2"),
        "16 de noviembre (sábado)": st.checkbox("16 de noviembre (sábado)", key="microciclo_3_3"),
    }

    # Microciclo #4
    st.markdown("<h4 style='color: purple;'>Microciclo #4</h4>", unsafe_allow_html=True)
    microciclos['microciclo_4'] = {
        "21 de noviembre (jueves)": st.checkbox("21 de noviembre (jueves)", key="microciclo_4_1"),
        "22 de noviembre (viernes)": st.checkbox("22 de noviembre (viernes)", key="microciclo_4_2"),
        "23 de noviembre (sábado)": st.checkbox("23 de noviembre (sábado)", key="microciclo_4_3"),
    }

    # Microciclo #5
    st.markdown("<h4 style='color: green;'>Microciclo #5</h4>", unsafe_allow_html=True)
    microciclos['microciclo_5'] = {
        "28 de noviembre (jueves)": st.checkbox("28 de noviembre (jueves)", key="microciclo_5_1"),
        "29 de noviembre (viernes)": st.checkbox("29 de noviembre (viernes)", key="microciclo_5_2"),
        "30 de noviembre (sábado)": st.checkbox("30 de noviembre (sábado)", key="microciclo_5_3"),
    }

    st.subheader("Notas o Mensajes para el Entrenador")
    notas = st.text_area("Escriba sus notas o mensajes aquí:")

    if st.button("Enviar"):
        if nombre_padre and nombre_jugador:
            save_to_sqlite(nombre_padre, nombre_jugador, notas, microciclos)
            st.success("¡Información enviada con éxito!")
        else:
            st.error("Por favor, ingrese el nombre del padre y del jugador.")

# Main function
def main():
    st.title("Sistema de Gestión de Entrenamientos Octubre-Noviembre 2024")
    
    menu = ["Formulario de Entrenamiento", "Acceso Admin"]
    choice = st.sidebar.selectbox("Seleccione una opción", menu)
    
    if choice == "Formulario de Entrenamiento":
        informacion_padre_y_calendario()
    elif choice == "Acceso Admin":
        admin_access()

if __name__ == "__main__":
    main()