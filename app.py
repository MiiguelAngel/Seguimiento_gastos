import streamlit as st
from streamlit_option_menu import option_menu
from pages import Checklist, Dashboard, Tabla_de_trx
import form_nueva_tarea
from datetime import datetime


# Configuración de la página
# st.set_page_config(page_title="Seguimiento gastos", page_icon=':money_with_wings:', layout='wide')



# Insertar JavaScript para obtener las dimensiones de la ventana
st.markdown("""
    <script>
    (function() {
        function sendWindowSize() {
            const size = {
                width: window.innerWidth,
                height: window.innerHeight
            };
            window.parent.postMessage(size, "*");
        }
        window.onresize = sendWindowSize;
        sendWindowSize();
    })();
    </script>
    """, unsafe_allow_html=True)

# Función para manejar mensajes de ventana
def handle_window_size():
    if "width" in st.session_state and "height" in st.session_state:
        st.write(f"Window width: {st.session_state.width}px")
        st.write(f"Window height: {st.session_state.height}px")

# Función JavaScript para manejar mensajes
st.markdown("""
    <script>
    window.addEventListener("message", (event) => {
        const size = event.data;
        window.parent.postMessage(size, "*");
        if (size.width && size.height) {
            window.streamlitWebSocket.send(JSON.stringify({
                "width": size.width,
                "height": size.height,
            }));
        }
    });
    </script>
    """, unsafe_allow_html=True)





# CSS personalizado para ocultar el sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para autenticar al usuario
def authenticate():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("Introduce la contraseña")
        password = st.text_input("Contraseña", type="password")
        if st.button("Acceder"):
            if password == st.secrets["password"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Contraseña incorrecta")
        return False
    return True

# Menú de opciones horizontal
selected = option_menu(
    menu_title=None,
    options=["Home", "Checklist", "Dashboard", "Tabla de transacciones"],
    icons=["house", "check2-square", "bar-chart-line", "file-earmark-text"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
                "padding": "5px", 
                "background-color": "#ffffff", 
                "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.1)", 
                "border-radius": "10px", 
                "border": "0.5px solid #ddd",
                "width": "100%"
            },
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "18px", 
                     "text-align": "center", 
                     "margin": "0px", 
                     "--hover-color": "#D9B310",
                     "color": "black"
                     },
        "nav-link-selected": {"background-color": "#EC576B", 
                              "color": "white", 
                              "transition": "background-color 0.3s, color 0.3s"
                              
                              },
    }
)

# Función para imprimir en consola el valor de session_state.page
def print_page_state():
    print("Current page:", st.session_state.page)

# Control de navegación basado en estado de sesión
if 'page' not in st.session_state:
    st.session_state.page = "Home"
    print_page_state()  # Imprimir el estado inicial

# Control de navegación basado en estado de sesión
if 'wait_new_tarea' not in st.session_state:
    st.session_state.wait_new_tarea = "Home"
    print_page_state()  # Imprimir el estado inicial

#Control de cambios para el checklist
if 'edit_task' not in st.session_state:
    st.session_state.edit_task = None

if selected == "Home":
    handle_window_size()
    st.session_state.page = "Home"
    st.session_state.wait_new_tarea = "Home"
    print_page_state()
    st.title("Bienvenido a la aplicación")
    st.write("Aquí puedes llevar el seguimiento de tus gastos.")
elif st.session_state.page == "form_nueva_tarea":
    print_page_state()
    form_nueva_tarea.mostrar()
elif selected == "Checklist" and st.session_state.wait_new_tarea == "Home":
    st.session_state.page = "Checklist"
    st.session_state.wait_new_tarea = "Home"
    print_page_state()
    if authenticate():
        Checklist.mostrar()
elif selected == "Dashboard":
    st.session_state.wait_new_tarea = "Home"
    st.session_state.page = "Dashboard"
    print_page_state()
    Dashboard.mostrar()
elif selected == "Tabla de transacciones":
    st.session_state.wait_new_tarea = "Home"
    st.session_state.page = "Tabla_de_trx"
    print_page_state()
    Tabla_de_trx.mostrar()
