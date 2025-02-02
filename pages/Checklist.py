import time
import streamlit as st
import streamlit as st
import json
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime



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
        tasks_data = json.load(f)
    
    # Ordenar las tareas
    for month, tasks in tasks_data.items():
        tasks_data[month] = sorted(tasks, key=lambda x: (x['completado'], x['monto']))
    
    return tasks_data

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

# Función para obtener el mes en español
def get_month_name(date):
    try:
        MONTHS = {
        "January": "Enero",
        "February": "Febrero",
        "March": "Marzo",
        "April": "Abril",
        "May": "Mayo",
        "June": "Junio",
        "July": "Julio",
        "August": "Agosto",
        "September": "Septiembre",
        "October": "Octubre",
        "November": "Noviembre",
        "December": "Diciembre"
        }
        return MONTHS[date]
    except:
        return date





def mostrar():

    

    load_css('assets/style.css')

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


    # Botón estilizado "Añadir nueva tarea"
    if st.button('Añadir nueva tarea', key='add_task', help='Añadir una nueva tarea'):
        st.session_state.page = "form_nueva_tarea"
        print("Current page:", st.session_state.page)  # Imprimir el cambio de página
        st.rerun()

    # Obtener el mes actual
    current_date = get_month_name(datetime.now())
    eng_month = current_date.strftime("%B")
    eng_year = current_date.strftime("%Y")
    current_month = get_month_name(eng_month) + " " + eng_year

    # Seleccionar el mes, por defecto el mes actual si está en los datos
    meses = list(tasks_data.keys())
    if current_month in meses:
        
        selected_month = st.selectbox('Selecciona un mes', meses, index=meses.index(current_month))
    else:
        selected_month = st.selectbox('Selecciona un mes', meses)

    # Mostrar las tareas del mes seleccionado con un diseño amigable
    tasks = tasks_data[selected_month]

    
    
    # Contenedor para el checklist
    # with st.container(border=True, key='checklist_container'):

    # Título del checklist
    #-------------------------------------------------------------------------
    # CSS para forzar que los elementos estén en una sola fila
    st.markdown(
        """
        <style>
            .table-header {
                display: flex;
                flex-direction: row;
                justify-content: space-between;
                width: 100%;
                white-space: nowrap;
                overflow-x: auto;
                border-bottom: 2px solid #ddd;
                padding-bottom: 5px;
            }
            .table-header div {
                flex: 1;
                text-align: center;
                min-width: 80px; /* Ajusta según sea necesario */
                font-size: 15x;
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Estructura de la cabecera de la tabla
    st.markdown(
        """
        <div class="table-header">
            <div>Check</div>
            <div>Descripción</div>
            <div>Monto</div>
            <div>Fecha</div>
            <div>Edit</div>
            <div>Delete</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    #-------------------------------------------------------------------------

    # Mostrar las tareas con el diseño modificado
    for i, task in enumerate(tasks):
        desc_class = "completed" if task["completado"] else ""
        # CSS para asegurar que cada fila de tareas se manteng en una sola línea

        st.markdown(
            """
            <style>
                .task-container-new {
                    display: flex;
                    flex-direction: row;
                    justify-content: space-between;
                    align-items: center;
                    width: 100%;
                    padding: 5px 0;
                }
                .task-container-new div {
                    flex: 1;
                    text-align: center;
                    min-width: 80px;
                    word-wrap: break-word;
                    white-space: normal;
                    font-size: 16px; /* Tamaño base de la fuente */
                }
                .task-desc {
                    max-width: 200px; /* Ajusta el ancho máximo de la descripción */
                }

                /* Media Queries para tamaños de fuente responsivos */
                @media (max-width: 1024px) {
                    .task-container-new div {
                        font-size: 15px;
                    }
                }
                @media (max-width: 768px) {
                    .task-container-new div {
                        font-size: 15px;
                    }
                }
                @media (max-width: 480px) {
                    .task-container-new div {
                        font-size: 15px;
                    }
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        
        col1, col2, col3, col4 = st.columns([0.5, 3, 0.5, 0.5])
        with col1:
            checkbox_value = st.toggle(f' ', key=f'check_{selected}_{selected_month}_{i}', value=task["completado"])
            if checkbox_value != task["completado"]:
                task["completado"] = checkbox_value
                save_task_update(tasks_data, selected_month, i, task, selected)  # Guardar cambios inmediatos solo para la tarea específica

        
        with col2:
            desc_class = "completed" if task["completado"] else ""
        
        # st.markdown(f"<p class='task-desc {desc_class}'>{task['descripcion']}</p>", unsafe_allow_html=True)
        
            st.markdown(
                f"""
                <div class="task-container-new">
                    <div class="task-desc {desc_class}">{task["descripcion"]}</div>
                    <div class="task-desc {desc_class}">${task["monto"]}</div>
                    <div class="task-desc {desc_class}">{task["fecha"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        
        # with col3:
        #     desc_class = "completed" if task["completado"] else ""
        #     st.markdown(f"<p class='task-amount {desc_class}'>${task['monto']}</p>", unsafe_allow_html=True)
        
        # with col4:
        #     desc_class = "completed" if task["completado"] else ""
        #     st.markdown(f"<p class='task-desc {desc_class}'>{task['fecha']}</p>", unsafe_allow_html=True)
        
        with col3:
            if st.button('✏️', key=f'edit_{selected}_{selected_month}_{i}', help="Editar tarea"):
                st.session_state.page = "form_nueva_tarea"
                st.session_state.wait_new_tarea = "Awaiting new task data"
                print("Current page:", st.session_state.page)  # Imprimir el cambio de página
                
                st.session_state.edit_task = {
                    "index": i,
                    "selected": selected,
                    "selected_month": selected_month,
                    "task": task
                }
                st.rerun()

        with col4:
            if st.button('❌', key=f'delete_{selected}_{selected_month}_{i}', help="Eliminar tarea"):
                del tasks[i]
                save_tasks(tasks_data, selected)
        st.markdown('<div class="task-container">', unsafe_allow_html=True)