import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Cargar solo las columnas necesarias y ajustar nombres
columnas_utilizadas = ['Temperatura_C', 'Humedad', 'MQ135']
try:
        df = pd.read_csv('datos_calidad_aire.csv', header=0, names=[
        'ID', 'Fecha', 'Hora', 'Temperatura_C', 'Humedad',
        'MQ135', 'Rs_Ro', 'Calidad_Aire_ICA', 'Segundos_Desde_Inicio', 'Ubicacion'
    ], usecols=['Temperatura_C', 'Humedad', 'MQ135'], encoding='latin1')
        
except FileNotFoundError:
    print("Error: El archivo 'datos_calidad_aire.csv' no fue encontrado.")
    exit()

# Convertir a tipo numérico, forzando errores a NaN
df = df.apply(pd.to_numeric, errors='coerce')

# Eliminar filas que contengan al menos un NaN
df_sin_nan = df.dropna()

if df_sin_nan.empty:
    print("Error: No hay suficientes datos válidos para entrenar el modelo después de eliminar filas con NaN.")
    exit()

# Definir variables independientes y dependientes
X = df_sin_nan[['Temperatura_C', 'Humedad']]
y = df_sin_nan['MQ135']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar el modelo
modelo = LinearRegression()
modelo.fit(X_train, y_train)

# Realizar predicciones
y_pred = modelo.predict(X_test)

# Evaluar el modelo
print("🔍 Evaluación del modelo:")
print("MSE:", mean_squared_error(y_test, y_pred))
print("R²:", r2_score(y_test, y_pred))

# Graficar resultados
plt.figure(figsize=(10, 5))
plt.scatter(y_test, y_pred)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel("Valor Real de MQ135")
plt.ylabel("Valor Predicho de MQ135")
plt.title("Predicción de MQ135 vs. Valor Real")
plt.grid(True)
plt.tight_layout()
plt.show()

# Otra forma de graficar (series de tiempo) si los datos tienen un orden temporal
# plt.figure(figsize=(10, 5))
# plt.plot(y_test.values, label='Real', marker='o')
# plt.plot(y_pred, label='Predicción', marker='x')
# plt.title("Predicción de MQ135 (PM2.5 simulado)")
# plt.xlabel("Muestras")
# plt.ylabel("Valor MQ135")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()
