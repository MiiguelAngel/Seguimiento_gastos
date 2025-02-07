import pandas as pd

# Ejemplo de datos con registros de ingresos y fechas
data = {
    'fecha': ['2025-01-31', '2025-02-28', '2025-03-31', '2025-04-30', '2025-05-31'],
    'tipo': ['ingreso', 'ingreso', 'ingreso', 'ingreso', 'ingreso'],
    'monto': [1000, 1200, 1100, 1300, 1150]
}
df = pd.DataFrame(data)
df['fecha'] = pd.to_datetime(df['fecha'])

# Ordenar por fecha
df = df.sort_values(by='fecha')

# Crear listas para las fechas de inicio y fin de los periodos de facturación
fechas_inicio = df['fecha'].tolist()
fechas_fin = [date - pd.DateOffset(days=1) for date in fechas_inicio[1:]] + [None]  # La última fecha fin es None

# Crear un nuevo DataFrame con los periodos de facturación
periodos = pd.DataFrame({
    'inicio': fechas_inicio,
    'fin': fechas_fin
})

# Mostrar los periodos de facturación
print(periodos)
