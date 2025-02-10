import streamlit as st
import pandas as pd
import plotly.express as px

# Ejemplo de datos
data = {
    'Categoria_AI': ['Alimentos', 'Transporte', 'Entretenimiento', 'Salud', 'Vivienda', 'Transporte', 'Alimentos'],
    'Monto': [500, 300, 150, 200, 450, 350, 400],
    'Fecha': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05', '2025-01-06', '2025-01-07']
}
df = pd.DataFrame(data)
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Crear la gráfica de torta con Plotly
fig = px.pie(df, names='Categoria_AI', values='Monto', title='Distribución de Montos por Categoría')

# Mostrar la gráfica en Streamlit
selection  = st.plotly_chart(fig, use_container_width=True)

print('Seleccionado')
# Capturar la selección con clickData
if selection is not None:
    selected_category = st.session_state.get("selected_category", "Ninguna selección aún")
    st.write(f"Categoría seleccionada: {selected_category}")

# Filtrar el DataFrame según la selección del usuario
if selected_category:
    selected_category = selected_category['points'][0]['label']
    df_filtered = df[df['Categoria_AI'] == selected_category]
    st.write(f"Filtrado por categoría: {selected_category}")
    st.write(df_filtered)
else:
    st.write("Seleccione una categoría en la gráfica para filtrar los datos.")

# Código de Streamlit para mostrar la selección y el DataFrame filtrado
st.write("Seleccione una categoría en la gráfica para filtrar los datos.")
st.plotly_chart(fig, use_container_width=True)