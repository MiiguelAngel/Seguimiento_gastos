import streamlit as st
import pandas as pd
from pages import Tabla_de_trx

def mostrar():

    bbdd = Tabla_de_trx.get_google_sheet_data()
    bbdd = bbdd.dropna(subset=['Mensaje completo']).copy()
    bbdd = bbdd[bbdd['Fecha'].astype(str) != '1/1/1000'].copy()
    bbdd['Fecha'] = pd.to_datetime(bbdd['Fecha'], errors='coerce')

    with st.expander("Ver datos", expanded=True):

        col1,col2,col3 = st.columns([1, 1, 1])
        with col1:
            opciones = bbdd["Tipo de transacción"].unique()
            seleccionar_todo = 'Seleccionar todo'
            # Agregar la opción "Seleccionar todo" al inicio de la lista de opciones
            opciones.insert(0, seleccionar_todo)
            if bbdd.shape[0] > 0:
                print('Si entro')
                #Consulta por Tipo
                st.header("Consulta por Tipo de gasto")
                Tipo_select=st.multiselect(
                    "Selecciona el tipo de Providencia",
                    options=opciones,
                    default=bbdd["Tipo de transacción"].unique()
                )

        with col2:
                #Consulta por año
                if bbdd.shape[0] > 0:
                    print('Si entro')
                    min_date = bbdd['Fecha'].min()
                    max_date = bbdd['Fecha'].max()
                    a_date = st.date_input("Consulta por fecha específica", (min_date, max_date))
                    if len(a_date) <2:
                        a_date_2 = list(a_date)
                        a_date_2.append(a_date[0])
                    else:
                        a_date_2 = a_date

    st.session_state.page = "dashboard"
    st.title("Dashboard")
    st.write("Aquí puedes ver el dashboard de tus gastos.")