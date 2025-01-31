import time
import streamlit as st
import streamlit as st
import json
import pandas as pd
from streamlit_option_menu import option_menu
import locale


# Establecer el locale en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    """, unsafe_allow_html=True)


def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Función para cargar las tareas desde un archivo JSON
def load_tasks(usuario):
    filename = f'tasks_{usuario.lower()}.json'
    with open(filename, 'r') as f:
        return json.load(f)

# Función para guardar las tareas en un archivo JSON
def save_tasks(tasks, usuario):

    filename = f'tasks_{usuario.lower()}.json'
    with open(filename, 'w') as f:
        json.dump(tasks, f, indent=4)

def save_task_update(tasks_data, selected_month, task_index, updated_task, selected):
    # Actualizar solo la tarea específica en el JSON
    tasks_data[selected_month][task_index] = updated_task
    save_tasks(tasks_data, selected)


# Inicializar estado de sesión
def initialize_session_state():
    if 'update' not in st.session_state:
        st.session_state.update = False
    if 'new_task' not in st.session_state:
        st.session_state.new_task = False



def mostrar():

    load_css('assets\style.css')

    initialize_session_state()

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

    # Cargar las tareas para el usuario seleccionado
    tasks_data = load_tasks(selected)

    # Seleccionar el mes
    meses = list(tasks_data.keys())
    selected_month = st.selectbox('Selecciona un mes', meses)

    # Mostrar las tareas del mes seleccionado con un diseño amigable
    tasks = tasks_data[selected_month]

    
    

    # Contenedor para el checklist
    with st.container(border=True, key='checklist_container'):

        # Mostrar las tareas con el diseño modificado
        for i, task in enumerate(tasks):
            desc_class = "completed" if task["completado"] else ""
            
            col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2,1])
            with col1:
                checkbox_value = st.toggle(f' ', key=f'check_{selected}_{selected_month}_{i}', value=task["completado"])
                if checkbox_value != task["completado"]:
                    task["completado"] = checkbox_value
                    save_task_update(tasks_data, selected_month, i, task, selected)  # Guardar cambios inmediatos solo para la tarea específica

            with col2:
                desc_class = "completed" if task["completado"] else ""
                st.markdown(f"<p class='task-desc {desc_class}'>{task['descripcion']}</p>", unsafe_allow_html=True)
            
            with col3:
                desc_class = "completed" if task["completado"] else ""
                st.markdown(f"<p class='task-amount {desc_class}'>${task['monto']}</p>", unsafe_allow_html=True)
            
            with col4:
                desc_class = "completed" if task["completado"] else ""
                st.markdown(f"<p class='task-desc {desc_class}'>{task['fecha']}</p>", unsafe_allow_html=True)
            
            with col5:
                if st.button('❌', key=f'delete_{selected}_{selected_month}_{i}', help="Eliminar tarea"):
                    del tasks[i]
                    save_tasks(tasks_data, selected)
            st.markdown('<div class="task-container">', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        
        # Botón estilizado "Añadir nueva tarea"
        if st.button('Añadir nueva tarea', key='add_task', help='Añadir una nueva tarea'):
            st.session_state.page = "form_nueva_tarea"
            print("Current page:", st.session_state.page)  # Imprimir el cambio de página
            st.rerun()