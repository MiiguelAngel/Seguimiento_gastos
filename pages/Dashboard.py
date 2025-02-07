import streamlit as st
import pandas as pd
from pages import Tabla_de_trx
from streamlit_option_menu import option_menu
from datetime import datetime

def mostrar():

    st.session_state.page = "dashboard"

    mes_actual = datetime.now()
    primer_dia_mes = mes_actual.replace(day=1)


    bbdd = Tabla_de_trx.get_google_sheet_data()
    bbdd = bbdd.dropna(subset=['Mensaje completo']).copy()
    bbdd = bbdd[bbdd['Fecha'].astype(str) != '1/1/1000'].copy()
    #Convertir fecha a formato datetime %d/%m/%Y
    bbdd['Fecha'] = pd.to_datetime(bbdd['Fecha'], format='%d/%m/%Y')
    #Fecha en formato numero YYYYMM
    bbdd['mes'] = bbdd['Fecha'].dt.strftime('%B %Y')
    #ordenar por fecha
    bbdd = bbdd.sort_values(['Fecha'], ascending=False)

    # Encontrar los periodos de facturación
    periodos_facturacion = bbdd[bbdd['Mensaje completo'].str.lower().str.replace('ó','o').str.contains('nomina')].copy()

    periodos_facturacion = periodos_facturacion.sort_values(by='Fecha')
    # Agrupar por año y mes, y tomar el primer registro de cada grupo
    periodos_facturacion['anio_mes'] = periodos_facturacion['Fecha'].dt.to_period('M')
    periodos_facturacion = periodos_facturacion.groupby('anio_mes').first().reset_index()
    
    fechas_inicio = periodos_facturacion['Fecha'].tolist()
    fechas_fin = [date - pd.DateOffset(days=1) for date in fechas_inicio[1:]] + [None]  # La última fecha fin es None
    periodos = pd.DataFrame({
        'inicio': fechas_inicio,
        'fin': fechas_fin
    })
    periodos['periodo_facturacion'] = periodos['inicio'].dt.strftime('%d-%m-%Y') + ' - ' + periodos['fin'].dt.strftime('%d-%m-%Y').fillna(pd.to_datetime('today').strftime('%d-%m-%Y'))


    with st.expander("FILTROS ACTIVOS", expanded=True):

        col1,col2 = st.columns([1, 1])
        with col1:
            opciones = bbdd["Tipo de transacción"].unique().tolist()
            seleccionar_todo = 'Seleccionar todo'
            # Agregar la opción "Seleccionar todo" al inicio de la lista de opciones
            opciones.insert(0, seleccionar_todo)
            if bbdd.shape[0] > 0:
                #Consulta por Tipo                
                Tipo_select=st.multiselect(
                    "Selecciona el tipo de Transacción",
                    options=opciones,
                    default="Seleccionar todo"
                )

        with col2:
                #Consulta por año
                if bbdd.shape[0] > 0:
                    # Crear un selector de meses en Streamlit
                    periodo_seleccionado = st.selectbox('Selecciona un periodo de facturación', periodos['periodo_facturacion'].tolist())
                    # Extraer el periodo  convertirlo a tipo datetime
                    fecha_inicio_selected = pd.to_datetime( periodo_seleccionado.split(' - ')[0], format='%d-%m-%Y') 
                    fecha_fin_selected = pd.to_datetime( periodo_seleccionado.split(' - ')[1], format='%d-%m-%Y')


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

    # Filtrar el dataframe
    if bbdd.shape[0] > 0:
        if selected == "Amoorcitaaa":
            bbdd = bbdd[bbdd['Banco'].str.upper() == "BANCOLOMBIA"]
        else:
            bbdd = bbdd[bbdd['Banco'].str.upper() == "BANCO FALABELLA"]
    
    # CSS personalizado para el selectbox
    st.markdown("""
        <style>
        .stSelectbox div[data-baseweb="select"] {
            background-color: #f4f4f4;  /* Fondo gris claro */
            border: 2px solid #1f77b4;  /* Borde azul */
            border-radius: 5px;  /* Bordes redondeados */
            font-family: 'Arial', sans-serif;  /* Fuente elegante */
            font-size: 16px;  /* Tamaño de fuente */
            color: #000000;  /* Color del texto */
        }
        .stSelectbox div[data-baseweb="select"] div[role="option"] {
            background-color: #ffffff;  /* Fondo blanco para opciones */
            color: #000000;  /* Color del texto para opciones */
        }
        .stSelectbox div[data-baseweb="select"] div[role="option"]:hover {
            background-color: #1f77b4;  /* Fondo azul al pasar el ratón */
            color: #ffffff;  /* Color del texto al pasar el ratón */
        }
                
        .stSelectbox p {
            color: #1f77b4;  /* Color azul para el texto */
            font-size: 16px;  /* Tamaño de fuente */       
        }
        </style>
        """, unsafe_allow_html=True)


    # Filtrar el dataframe basado en el rango de fechas del mes seleccinado y en el tipo de transacción
    if "Seleccionar todo" in Tipo_select:
        df_filtrado = bbdd[bbdd['Fecha'].between(fecha_inicio_selected, fecha_fin_selected)]
    else:
        df_filtrado = bbdd[(bbdd['Fecha'].between(fecha_inicio_selected, fecha_fin_selected)) & (bbdd['Tipo de transacción'].isin(Tipo_select))]