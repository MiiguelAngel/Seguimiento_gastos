import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def mostrar():
    
    # Configurar las credenciales de Google desde secrets
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials_info = st.secrets["gcp_service_account"]
    print(credentials_info)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    gc = gspread.authorize(credentials)

    # Conectar a la hoja de cálculo
    sheet = gc.open_by_key('1R44D-GHsUW7p_GiPai4gQh934c2FQKG4pdbj1TDWQVk').sheet1

    # Obtener todas las filas de la hoja de cálculo
    rows = sheet.get_all_records()

    # Convertir los datos a un dataframe de Pandas
    df = pd.DataFrame(rows)

    # Mostrar el dataframe en Streamlit
    st.title("Datos de la Google Sheet")

    st.expander("Ver datos", expanded=True)
    st.write(df)