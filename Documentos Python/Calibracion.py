import serial
import time
import json
import os

# Configuración del puerto serie
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

# Calibrar durante 15 segundos
tiempo_calibracion = 15
valores_calibracion = []

print(f"🌿 Iniciando calibración durante {tiempo_calibracion} segundos...")
inicio_calibracion = time.time()

while time.time() - inicio_calibracion < tiempo_calibracion:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea.count(',') == 2:
            datos = linea.split(',')
            mq_valor = float(datos[2])
            valores_calibracion.append(mq_valor)
            print("Lectura:", mq_valor)
    except:
        continue

arduino.close()

if len(valores_calibracion) == 0:
    print("❌ No se obtuvieron datos.")
    exit()

Ro = sum(valores_calibracion) / len(valores_calibracion)
print(f"✅ Ro calibrado: {Ro:.2f}")

# Guardar en archivo
with open('ro_config.json', 'w') as f:
    json.dump({"Ro": Ro}, f)

print("💾 Ro guardado en ro_config.json")
