import streamlit as st
import pandas as pd
from pages import Tabla_de_trx
from streamlit_option_menu import option_menu
from datetime import datetime
import plotly.express as px

# Incluir el enlace a la hoja de estilos de Font Awesome
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """, unsafe_allow_html=True)


st.cache_data
def obtener_datos():
    bbdd = Tabla_de_trx.get_google_sheet_data()
    bbdd = bbdd.dropna(subset=['Mensaje completo']).copy()
    bbdd = bbdd[bbdd['Fecha'].astype(str) != '1/1/1000'].copy()
    #Convertir fecha a formato datetime %d/%m/%Y
    bbdd['Fecha'] = pd.to_datetime(bbdd['Fecha'], format='%d/%m/%Y', errors='coerce')
    #Fecha en formato numero YYYYMM
    bbdd['mes'] = bbdd['Fecha'].dt.strftime('%B %Y')
    #ordenar por fecha
    bbdd = bbdd.sort_values(['Fecha'], ascending=False)

    return bbdd


def obtener_periodos_facturacion(bbdd, selected):
    # Encontrar los periodos de facturación
    # periodos_facturacion = bbdd[bbdd['Tipo de transacción'] == 'Ingreso'].copy()
    if selected == "Amoorcitaaa":
        periodos_facturacion = bbdd[bbdd['Mensaje completo'].astype(str).str.replace('ó','o').str.lower().str.contains('nomina')]
    elif selected == "Amooorcitooo":
        periodos_facturacion = bbdd[bbdd['Monto']>=6e6]

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

    return periodos

def display_watchlist_plotly(df, name):

    if name == 'ingresos':
        title = 'Ingresos Mensuales'
        df['eje_y'] = df['ingresos']
        label = 'Ingresos'

    elif name == 'gastos':
        title = 'Gastos Mensuales'
        df['eje_y'] = df['gastos']
        label = 'Gastos'

    elif name == 'balance':
        title = 'Balance Mensual'
        df['eje_y'] = df['balance_acumulado']
        label = 'Balance'
    # Crear la gráfica con Plotly
    # Crear la gráfica de barras con Plotly
    fig = px.line(df, x='Fecha', y='eje_y', labels={'ingresos': label}, 
             title=title, 
             color_discrete_sequence=['#008000'])

    # Personalizar el layout
    fig.update_layout(
        plot_bgcolor='white',  # Fondo blanco
        paper_bgcolor='white',  # Fondo blanco del área de dibujo
        xaxis=dict(showgrid=False, showticklabels=False, title=''),  # Ocultar líneas de guía, etiquetas y título en el eje X
        yaxis=dict(showgrid=False, showticklabels=False, title=''),  # Ocultar líneas de guía, etiquetas y título en el eje Y
        # showlegend=False,  # Ocultar la leyenda
        margin=dict(l=0, r=0, t=0, b=0),  # Márgenes ajustados
        autosize=True,  # Ajustar al tamaño del contenedor
        height=100  # Altura de la gráfica
    )

    return fig

def display_watchlist_cards(df,name,monto):
    df_watch = df.copy()
    with st.container(border=True):
        st.html(f'<span class="watchlist_card"></span>')

        #Texto moderno con tamaño de letra ajustable
        # st.markdown(f"{name}")
        icon = ''
        label = ''
        if name == 'ingresos':
            icon = '<i class="fas fa-coins"></i>'  # Icono de ingresos (monedas)
            label = 'Ingresos'
        elif name == 'gastos':
            icon = '<i class="fas fa-chart-line"></i>'  # Icono de gastos (línea de gráfico descendente)
            label = 'Gastos'
        elif name == 'balance':
            icon = '<i class="fas fa-balance-scale"></i>'  # Icono de balance (balanza)
            label = 'Balance'

        # Usar markdown para mostrar la etiqueta, el icono y el monto centrado y más grande
        st.markdown(
            f"""
            <div style='text-align: center;'>
                <div style='font-size: 20px;'>{label}</div>
                <span style='font-size: 30px;'>{icon} $ {monto:.0f}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
            
        
        figure = display_watchlist_plotly(df_watch, name)
        st.plotly_chart(figure, use_container_width=False, key=name)


def mostrar():

    st.session_state.page = "dashboard"
     # Obtener los datos de ambas hojas
    bbdd = obtener_datos()

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
    
    #Obtener los periodos de facturacion
    periodos = obtener_periodos_facturacion(bbdd, selected)

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


    df_ingresos = bbdd[(bbdd['Tipo de transacción'] == 'Ingreso') &
                       bbdd['Fecha'].between(fecha_inicio_selected, fecha_fin_selected)].copy()
    df_gastos = bbdd[(bbdd['Tipo de transacción'] != 'Ingreso') &
                     bbdd['Fecha'].between(fecha_inicio_selected, fecha_fin_selected)].copy()

    # Agrupar por fecha y calcular la suma de ingresos y gastos
    ingresos_diarios = df_ingresos.groupby('Fecha')['Monto'].sum().reset_index()
    gastos_diarios = df_gastos.groupby('Fecha')['Monto'].sum().reset_index()

    # Unir ingresos y gastos en un solo DataFrame
    balance_diario = pd.merge(ingresos_diarios, gastos_diarios, on='Fecha', how='outer', suffixes=('_ingresos', '_gastos')).fillna(0)

    # Crear tres tarjetas horizontales
    col1, col2, col3 = st.columns(3)

    with col1:
        ingresos_diarios['ingresos'] = ingresos_diarios['Monto']
        display_watchlist_cards(ingresos_diarios, 'ingresos', ingresos_diarios['ingresos'].cumsum().max())

    with col2:
        gastos_diarios['gastos'] = gastos_diarios['Monto']
        display_watchlist_cards(gastos_diarios, 'gastos', gastos_diarios['gastos'].cumsum().max())

    with col3:
        # Calcular el balance diario
        balance_diario['balance'] = balance_diario['Monto_ingresos'] - balance_diario['Monto_gastos']
        #Ordernar el datafrae por Fecha
        balance_diario = balance_diario.sort_values(by='Fecha')
        balance_diario['balance_acumulado'] = balance_diario['balance'].cumsum()
        balance_final = balance_diario.iloc[-1]['balance_acumulado']
        display_watchlist_cards(balance_diario, 'balance', balance_final)

    st.markdown('---')

    #-------------------------------------------------------------------------------------------------------------------------------

    opciones = bbdd["Categoria_AI"].unique().tolist()
    seleccionar_todo = 'Seleccionar todo'
    # Agregar la opción "Seleccionar todo" al inicio de la lista de opciones
    opciones.insert(0, seleccionar_todo)
    if bbdd.shape[0] > 0:
        #Consulta por Tipo                
        Categoria_select=st.multiselect(
            "Selecciona el tipo de Gasto",
            options=opciones,
            default="Seleccionar todo"
        )

    # Filtrar el dataframe basado en el rango de fechas del mes seleccinado y en el tipo de transacción
    if "Seleccionar todo" in Tipo_select:
        df_filtrado = bbdd[bbdd['Fecha'].between(fecha_inicio_selected, fecha_fin_selected)]
    else:
        df_filtrado = bbdd[(bbdd['Fecha'].between(fecha_inicio_selected, fecha_fin_selected)) & 
                           (bbdd['Tipo de transacción'].isin(Tipo_select))]

    if "Seleccionar todo" in Categoria_select:
        df_filtrado = df_filtrado.copy()
    else:
        df_filtrado = df_filtrado[(df_filtrado['Categoria_AI'].isin(Categoria_select))]

    # Crear la gráfica de torta con Plotly
    fig = px.pie(df_filtrado, names='Categoria_AI', values='Monto', title='Distribución de Montos por Categoría')

    # Mostrar la gráfica en Streamlit
    figure  = st.plotly_chart(fig, use_container_width=True)

    st.write(df_filtrado)

