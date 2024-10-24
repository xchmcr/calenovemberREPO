import streamlit as st
from connections import connect_to_mongo

def main():
    st.title("Sistema de Gestión de entrenamientos Noviembre")

    # Estado de sesión para almacenar datos del formulario y estado de administrador
    if "nombre_padre" not in st.session_state:
        st.session_state.nombre_padre = None
    if "nombre_jugador" not in st.session_state:
        st.session_state.nombre_jugador = None
    if "es_admin" not in st.session_state:
        st.session_state.es_admin = False  # Estado de administrador para ver envíos

    # Opciones del menú para la recopilación de datos de padres
    menu = ["Información del Padre y Calendario", "Inicio de Sesión de Administrador"]

    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Información del Padre y Calendario":
        informacion_padre_y_calendario()

    elif choice == "Inicio de Sesión de Administrador":
        inicio_sesion_admin()

    # Si el usuario ha iniciado sesión como administrador, permite ver envíos
    if st.session_state.es_admin:
        st.sidebar.subheader("Opciones de Administrador")
        if st.sidebar.button("Ver Envíos"):
            ver_envios()


def informacion_padre_y_calendario():
    # Paso 1: Recoger nombres del padre y del jugador
    st.subheader("Ingrese Información del Padre y del Jugador")
    nombre_padre = st.text_input("Nombre del Padre")
    nombre_jugador = st.text_input("Nombre del Jugador")

    # Paso 2: Información sobre el Microciclo
    st.subheader("¿Qué es un Microciclo?")
    st.markdown("""
        **Un microciclo** es un período de entrenamiento a corto plazo dentro de un programa de entrenamiento general. 
        Generalmente, dura de 1 a 2 semanas y se enfoca en objetivos físicos o tácticos específicos. Para los jugadores de fútbol, 
        esto podría involucrar sesiones de resistencia, fuerza, agilidad o recuperación. Cada microciclo es fundamental para optimizar el rendimiento del jugador.
    """)

    # Paso 3: Mostrar la imagen del calendario personalizado
    st.image("https://raw.githubusercontent.com/xchmcr/calenovemberREPO/main/calendar.png", caption="Calendario de Entrenamiento de Noviembre 2024", use_column_width=True)

    # Paso 4: Definir los microciclos con casillas de verificación
    st.subheader("Seleccione Fechas de Entrenamiento Disponibles")

    st.markdown("### Microciclo #1 (Azul Claro)")
    microciclo_1 = {
        "29 de octubre (martes)": st.checkbox("29 de octubre (martes)"),
        "31 de octubre (Jueves)": st.checkbox("31 de octubre (Jueves)"),
        "1 de Noviembre (Viernes)": st.checkbox("1 de Noviembre (Viernes)"),
        "2 de Noviembre (Viernes)": st.checkbox("2 de Noviembre (Viernes)")
    }

    st.markdown("### Microciclo #2 (Rojo)")
    microciclo_2 = {
        "4 de noviembre (lunes)": st.checkbox("4 de noviembre (lunes)"),
        "5 de noviembre (martes)": st.checkbox("5 de noviembre (martes)"),
        "7 de noviembre (jueves)": st.checkbox("7 de noviembre (jueves)"),
        "8 de noviembre (viernes)": st.checkbox("8 de noviembre (viernes)"),
        "9 de noviembre (sábado)": st.checkbox("9 de noviembre (sábado)")
    }

    st.markdown("### Microciclo #3 (Naranja)")
    microciclo_3 = {
        "11 de noviembre (lunes)": st.checkbox("11 de noviembre (lunes)"),
        "12 de noviembre (martes)": st.checkbox("12 de noviembre (martes)"),
        "14 de noviembre (jueves)": st.checkbox("14 de noviembre (jueves)"),
        "15 de noviembre (viernes)": st.checkbox("15 de noviembre (viernes)"),
        "16 de noviembre (sábado)": st.checkbox("16 de noviembre (sábado)")
    }

    st.markdown("### Microciclo #4 (Morado)")
    microciclo_4 = {
        "18 de noviembre (lunes)": st.checkbox("18 de noviembre (lunes)"),
        "19 de noviembre (martes)": st.checkbox("19 de noviembre (martes)"),
        "21 de noviembre (jueves)": st.checkbox("21 de noviembre (jueves)"),
        "22 de noviembre (viernes)": st.checkbox("22 de noviembre (viernes)"),
        "23 de noviembre (sábado)": st.checkbox("23 de noviembre (sábado)")
    }

    st.markdown("### Microciclo #5 (Verde)")
    microciclo_5 = {
        "25 de noviembre (lunes)": st.checkbox("25 de noviembre (lunes)"),
        "26 de noviembre (martes)": st.checkbox("26 de noviembre (martes)"),
        "28 de noviembre (jueves)": st.checkbox("28 de noviembre (jueves)"),
        "29 de noviembre (viernes)": st.checkbox("29 de noviembre (viernes)"),
        "30 de noviembre (sábado)": st.checkbox("30 de noviembre (sábado)")
    }

    # Paso 5: Campo de notas o mensajes
    st.subheader("Notas o Mensajes para el Entrenador")
    notas = st.text_area("Escriba sus notas o mensajes aquí:")

    # Botón de envío
    if st.button("Enviar"):
        st.session_state.nombre_padre = nombre_padre
        st.session_state.nombre_jugador = nombre_jugador
        st.session_state.notas = notas
        
        # Aquí puedes agregar el código para guardar la información en la base de datos
        st.success("¡Información enviada con éxito!")

def inicio_sesion_admin():
    st.subheader("Inicio de Sesión de Administrador")
    password = st.text_input("Contraseña", type="password")
    
    if st.button("Iniciar Sesión"):
        # Aquí debes verificar la contraseña y permitir el acceso
        if password == "Chave4043":  # Cambia esto a la verificación real
            st.session_state.es_admin = True
            st.success("Inicio de sesión exitoso.")
        else:
            st.error("Contraseña incorrecta.")

def ver_envios():
    st.subheader("Envíos Recibidos")
    # Aquí debes agregar el código para mostrar los envíos guardados en la base de datos
    st.write("Aquí puedes ver los datos enviados por los padres.")

if __name__ == "__main__":
    main()
