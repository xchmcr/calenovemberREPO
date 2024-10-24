import streamlit as st
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def connect_to_mongo():
    uri = "mongodb+srv://xchmcr:Waffletea27@clustertest01.dc3gd.mongodb.net/fridaydatabase?retryWrites=true&w=majority&ssl=true&tlsAllowInvalidCertificates=true"
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=30000)
        db = client["fridaydatabase"]
        return db
    except ConnectionFailure as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None


#save to mongo
def save_to_mongo(nombre_padre, nombre_jugador, notas, microciclos):
    db = connect_to_mongo()
    
    if db is not None:  # Corrected check
        data = {
            "nombre_padre": nombre_padre,
            "nombre_jugador": nombre_jugador,
            "notas": notas,
            "microciclos": microciclos,
        }
        db.fridayparents.insert_one(data)


# Function to display data from MongoDB in an admin view
def visualize_microciclos(data):
    for parent in data:
        st.subheader(f"Parent: {parent['nombre_padre']}, Player: {parent['nombre_jugador']}")
        
        # Loop through each microciclo and show selected dates
        for cycle, dates in parent["microciclos"].items():
            selected_dates = [date for date, chosen in dates.items() if chosen]
            if selected_dates:
                st.markdown(f"**{cycle.capitalize()}:** {', '.join(selected_dates)}")
            else:
                st.markdown(f"**{cycle.capitalize()}:** No dates selected.")
        
        # Now display the notes field at the end
        st.markdown(f"**Notas del Padre:** {parent.get('notas', 'No notes provided')}")
        
        st.write("---")


        # Function to display data from MongoDB in an admin view
def display_all_data():
    db = connect_to_mongo()
    if db is not None:  # Corrected check
        records = db.fridayparents.find()
        data = list(records)
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

    st.info("""Los días subrayados con color son los días en los que se va a entrenar, cada color corresponde a un microciclo diferente. por favor seleccionar los días en los que se encuentre disponible.""")

    # Show calendar image
    st.image("https://raw.githubusercontent.com/xchmcr/calenovemberREPO/main/calendar.png", 
             caption="Calendario de Entrenamiento de Noviembre 2024", use_column_width=True)

    # Microcycle selections
    st.subheader("Seleccione Fechas de Entrenamiento Disponibles")
    
    # Create a dictionary to store microcycle data with colored headers
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

    st.markdown("<h4 style='color: orange;'>Microciclo #3</h4>", unsafe_allow_html=True)
    microciclos['microciclo_3'] = {
        "11 de noviembre (lunes)": st.checkbox("11 de noviembre (lunes)", key="microciclo_3_1"),
        "12 de noviembre (martes)": st.checkbox("12 de noviembre (martes)", key="microciclo_3_2"),
        "14 de noviembre (jueves)": st.checkbox("14 de noviembre (jueves)", key="microciclo_3_3"),
        "15 de noviembre (viernes)": st.checkbox("15 de noviembre (viernes)", key="microciclo_3_4"),
        "16 de noviembre (sábado)": st.checkbox("16 de noviembre (sábado)", key="microciclo_3_5"),
    }

    st.markdown("<h4 style='color: purple;'>Microciclo #4</h4>", unsafe_allow_html=True)
    microciclos['microciclo_4'] = {
        "18 de noviembre (lunes)": st.checkbox("18 de noviembre (lunes)", key="microciclo_4_1"),
        "19 de noviembre (martes)": st.checkbox("19 de noviembre (martes)", key="microciclo_4_2"),
        "21 de noviembre (jueves)": st.checkbox("21 de noviembre (jueves)", key="microciclo_4_3"),
        "22 de noviembre (viernes)": st.checkbox("22 de noviembre (viernes)", key="microciclo_4_4"),
        "23 de noviembre (sábado)": st.checkbox("23 de noviembre (sábado)", key="microciclo_4_5"),
    }

    st.markdown("<h4 style='color: green;'>Microciclo #5</h4>", unsafe_allow_html=True)
    microciclos['microciclo_5'] = {
        "25 de noviembre (lunes)": st.checkbox("25 de noviembre (lunes)", key="microciclo_5_1"),
        "26 de noviembre (martes)": st.checkbox("26 de noviembre (martes)", key="microciclo_5_2"),
        "28 de noviembre (jueves)": st.checkbox("28 de noviembre (jueves)", key="microciclo_5_3"),
        "29 de noviembre (viernes)": st.checkbox("29 de noviembre (viernes)", key="microciclo_5_4"),
        "30 de noviembre (sábado)": st.checkbox("30 de noviembre (sábado)", key="microciclo_5_5"),
    }

    # Notes field
    st.subheader("Notas o Mensajes para el Entrenador")
    notas = st.text_area("Escriba sus notas o mensajes aquí:")

    # Submit button
    if st.button("Enviar"):
        if nombre_padre and nombre_jugador:
            save_to_mongo(nombre_padre, nombre_jugador, notas, microciclos)
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
