import streamlit as st
from pages import Checklist
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu
import uuid

# CSS personalizado para el checkbox
st.markdown("""
    <style>
    .stCheckbox label {
        font-size: 30px !important;
        font-weight: bold !important;
        font-family: cursive !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)


# Función para reiniciar los campos del formulario
def reiniciar_formulario():
    st.session_state.descripcion = ''
    st.session_state.monto = 0
    st.session_state.fecha = datetime.today()

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

    st.title("Añadir/Editar Tarea")

    task_to_edit = st.session_state.edit_task

    #es_recurrente = st.toggle('¿Es una tarea recurrente?', key='es_recurrente')
    es_recurrente = st.checkbox('¿Es una tarea recurrente?', key='es_recurrente')
    st.session_state.wait_new_tarea == "Awaiting new task data"
    print("Current state task:", st.session_state.wait_new_tarea)  # Imprimir el cambio de página
    # Formulario para añadir nueva tarea
    with st.form(key='new_task_form_unique'):
        descripcion = st.text_input('Descripción', value=task_to_edit["task"]["descripcion"] if task_to_edit else "")
        monto = st.number_input('Monto', min_value=0, value=task_to_edit["task"]["monto"] if task_to_edit else 0)
        fecha = st.date_input('Fecha', value=datetime.strptime(task_to_edit["task"]["fecha"], '%Y-%m-%d') if task_to_edit else datetime.today())
        submit_button = st.form_submit_button(label='Guardar tarea')
        if submit_button:
            nueva_tarea = {
                "descripcion": descripcion,
                "monto": monto,
                "fecha": fecha.strftime('%Y-%m-%d'),
                "completado": False,
                "id": str(uuid.uuid4())
            }
            #--------------------------para editar un registro
            if task_to_edit:

                # Si la tarea es recurrente, modificar todas las tareas recurrentes con la misma descripción
                if es_recurrente:
                    tasks_data = Checklist.load_tasks(task_to_edit["selected"])
                    for mes, tareas in tasks_data.items():
                        for i, tarea in enumerate(tareas):
                            if tarea["descripcion"] == task_to_edit["task"]["descripcion"]:
                                tasks_data[mes][i] = nueva_tarea
                    Checklist.save_tasks(tasks_data, task_to_edit["selected"])
                    st.success('Tarea editada con éxito')

                else:

                    # Si la tarea no es recurrente, modificar solo la tarea actual
                    tasks_data[task_to_edit["selected_month"]][task_to_edit["index"]] = nueva_tarea
                    reiniciar_formulario()
                    Checklist.save_tasks(tasks_data, task_to_edit["selected"])
                    st.success('Tarea editada con éxito')
                    # Restablecer los valores del formulario
                    st.session_state.edit_task = None

            #--------------------------Para añadir un registro nuevo
            else:
                
                #Guardar la tarea en el estado de la sesión
                st.session_state.new_task_data = [nueva_tarea]

                # Si la tarea es recurrente, añadir 11 tareas más
                if es_recurrente:
                    for i in range(1, 12):
                        nueva_fecha = fecha + timedelta(days=30 * i)
                        tarea_recurrente = {
                            "descripcion": descripcion,
                            "monto": monto,
                            "fecha": nueva_fecha.strftime('%Y-%m-%d'),
                            "completado": False
                        }
                        st.session_state.new_task_data.append(tarea_recurrente)

        
                # Actualizar el archivo JSON con la nueva tarea
                tasks_data = Checklist.load_tasks(selected)  # Ajusta esto según la lógica de usuario

                # Por cada tarea en la lista de tareas nuevas, 
                # añadir a la lista de tareas del mes correspondiente
                for tarea in st.session_state.new_task_data:
                    año = datetime.strptime(tarea['fecha'], '%Y-%m-%d').strftime('%Y')
                    month = datetime.strptime(tarea['fecha'], '%Y-%m-%d').strftime('%B').capitalize()
                    month_without_Y = get_month_name(month)
                    mes = f"{month_without_Y} {año}"
                    if mes in tasks_data:
                        tasks_data[mes].append(tarea)
                    else:
                        tasks_data[mes] = [tarea]
                Checklist.save_tasks(tasks_data, selected)
                reiniciar_formulario()
                st.success('Tarea añadida con éxito')
                

            st.session_state.new_task_data = None
            st.session_state.wait_new_tarea = "Home"
            reiniciar_formulario()

    # Botón para volver al checklist
    if st.button('Volver al Checklist'):
        reiniciar_formulario()
        st.session_state.new_task_data = None
        st.session_state.wait_new_tarea = "Home"
        st.session_state.page = "Checklist"
        print("Current page:", st.session_state.page)  # Imprimir el cambio de página
