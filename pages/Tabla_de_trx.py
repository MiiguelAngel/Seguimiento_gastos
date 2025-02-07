import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Función para obtener datos de Google Sheets y cachearlos
@st.cache_data
def get_google_sheet_data():
    # Configurar las credenciales de Google desde secrets
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credentials_info = st.secrets["gcp_service_account"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_info, scope)
    gc = gspread.authorize(credentials)

    # Conectar a la hoja de cálculo
    sheet = gc.open_by_key('1R44D-GHsUW7p_GiPai4gQh934c2FQKG4pdbj1TDWQVk')

    # Obtener datos de la primera hoja
    sheet1 = sheet.get_worksheet(0)  # Primera hoja
    rows1 = sheet1.get_all_records()
    df1 = pd.DataFrame(rows1)

    # Obtener datos de la segunda hoja
    sheet2 = sheet.get_worksheet(1)  # Segunda hoja
    rows2 = sheet2.get_all_records()
    df2 = pd.DataFrame(rows2)

    df = df1.merge(df2, on='Mensaje completo', how='left')
    df = df.sort_values(['Fecha','Monto','Banco'], ascending=False)

    return df


def mostrar():

    # Obtener los datos de ambas hojas
    df = get_google_sheet_data()

    # Mostrar el dataframe en Streamlit
    st.title("Datos de la Google Sheet")

    st.expander("Ver datos", expanded=True)
    st.write(df[['Fecha','Banco','Monto','Comercio','Categoria_AI']] )