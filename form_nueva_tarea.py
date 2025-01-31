import streamlit as st
from pages import Checklist
from datetime import datetime
from streamlit_option_menu import option_menu
import locale



def mostrar():
    # Establecer el locale en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    # Seleccionar usuario
    users = ["Amoorcitaaa", "Amooorcitooo"]
    selected = option_menu(
        menu_title=None,
        options=users,
        icons=["fa fa-dinosaur", "fa fa-dragon"],
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
                "width": "70%"
            },
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "18px", 
                     "text-align": "center", 
                     "margin": "0px", 
                     "--hover-color": "#D9B310",
                     "color": "black"
                     },
        "nav-link-selected": {"background-color": "#4EC5C1", 
                              "color": "white", 
                              "transition": "background-color 0.3s, color 0.3s"
                              
                              },
    }
    )

    st.title("Añadir Nueva Tarea")
    st.session_state.wait_new_tarea == "Awaiting new task data"
    print("Current state task:", st.session_state.wait_new_tarea)  # Imprimir el cambio de página
    # Formulario para añadir nueva tarea
    with st.form(key='new_task_form_unique'):
        descripcion = st.text_input('Descripción')
        monto = st.number_input('Monto', min_value=0)
        fecha = st.date_input('Fecha', value=datetime.today())
        submit_button = st.form_submit_button(label='Guardar tarea')
        if submit_button:
            st.session_state.new_task_data = {
                "descripcion": descripcion,
                "monto": monto,
                "fecha": fecha.strftime('%Y-%m-%d'),
                "completado": False
            }
            st.success('Tarea añadida con éxito')
        
        # Actualizar el archivo JSON con la nueva tarea
            tasks_data = Checklist.load_tasks(selected)  # Ajusta esto según la lógica de usuario
            mes = datetime.strptime(st.session_state.new_task_data['fecha'], '%Y-%m-%d').strftime('%B %Y').capitalize()
            if mes in tasks_data:
                tasks_data[mes].append(st.session_state.new_task_data)
            else:
                tasks_data[mes] = [st.session_state.new_task_data]
            Checklist.save_tasks(tasks_data, selected)
            st.session_state.new_task_data = None

    # Botón para volver al checklist
    if st.button('Volver al Checklist'):
        st.session_state.page = "Checklist"
        print("Current page:", st.session_state.page)  # Imprimir el cambio de página
