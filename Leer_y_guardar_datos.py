import serial
import csv
import time
import os
import json
from datetime import datetime

# 🔹 UBICACIÓN FIJA
ubicacion = "oficina"
if not os.path.exists("ro_config.json"):
    print("❌ No se encontró el archivo de calibración (ro_config.json). Ejecuta primero la calibración.")
    exit()

with open("ro_config.json", "r") as f:
    Ro = json.load(f)["Ro"]
print(f"✅ Ro cargado: {Ro:.2f}")

# Configurar puerto
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

filename = 'datos_calidad_aire.csv'
archivo_nuevo = not os.path.exists(filename)

def interpretar_calidad_ica_calibrado(relacion):
    if relacion > 5.0:
        return "Morado (Muy dañino a la salud)"
    elif 3.5 <= relacion <= 5.0:
        return "Rojo (Dañino a la salud)"
    elif 2.0 <= relacion < 3.5:
        return "Naranja (Dañino a la salud para grupos sensibles)"
    elif 1.0 <= relacion < 2.0:
        return "Amarillo (Moderado)"
    else:
        return "Verde (Bueno)"

# Iniciar archivo CSV
with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    if archivo_nuevo:
        writer.writerow([
            'ID', 'Fecha', 'Hora', 'Temperatura_C', 'Humedad',
            'MQ135', 'Rs_Ro', 'Calidad_Aire_ICA', 'Segundos_Desde_Inicio', 'Ubicacion'
        ])

    print("📡 Recolectando datos... Ctrl+C para detener.")
    id_muestra = 1
    inicio = time.time()

    try:
        while True:
            linea = arduino.readline().decode('utf-8').strip()
            if linea.count(',') == 2:
                datos = linea.split(',')
                try:
                    temp = float(datos[0])
                    hum = float(datos[1])
                    mq = float(datos[2])
                    relacion = round(mq / Ro, 2)
                    calidad_ica = interpretar_calidad_ica_calibrado(relacion)

                    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    segundos_transcurridos = round(time.time() - inicio, 2)

                    writer.writerow([
                        id_muestra,
                        ahora.split(' ')[0],
                        ahora.split(' ')[1],
                        temp, hum, mq, relacion, calidad_ica, segundos_transcurridos, ubicacion
                    ])

                    print(f"[{ahora}] Temp: {temp}°C | Hum: {hum}% | MQ: {mq} | Rs/Ro: {relacion:.2f} | Calidad Aire (ICA): {calidad_ica} | Ubicación: ({ubicacion})")
                    id_muestra += 1

                except Exception as e:
                    print("❌ Error en conversión de datos:", e)

    except KeyboardInterrupt:
        print(f"\n✅ Lectura detenida. Datos guardados en {filename}")
        arduino.close()
