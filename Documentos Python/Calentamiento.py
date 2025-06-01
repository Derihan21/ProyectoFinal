import serial
import time
from datetime import datetime

# Configura el puerto COM
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

# Calentamiento (10 minutos = 600 segundos)
tiempo_calentamiento = 600
print(f"🔥 Calentando sensor durante {tiempo_calentamiento // 60} minutos...")

inicio_calentamiento = time.time()
while time.time() - inicio_calentamiento < tiempo_calentamiento:
    tiempo_restante = int(tiempo_calentamiento - (time.time() - inicio_calentamiento))
    print(f"⌛ Tiempo restante para iniciar calibración: {tiempo_restante} segundos", end='\r')
    time.sleep(1)

print("\n✅ Calentamiento finalizado. Iniciando calibración...")

# Calibración
tiempo_calibracion = 15
valores_calibracion = []
inicio_calibracion = time.time()

while time.time() - inicio_calibracion < tiempo_calibracion:
    linea = arduino.readline().decode('utf-8').strip()
    if linea.count(',') == 2:
        datos = linea.split(',')
        try:
            mq_valor = float(datos[2])
            valores_calibracion.append(mq_valor)
            print(f"📏 Valor calibración: {mq_valor}")
        except:
            continue

if not valores_calibracion:
    print("❌ No se obtuvieron valores válidos para calibración.")
    arduino.close()
    exit()

Ro = sum(valores_calibracion) / len(valores_calibracion)
print(f"✅ Calibración completada. Ro estimado: {Ro:.2f}")

# Función de interpretación
def interpretar_calidad_relativa(mq):
    relacion = mq / Ro
    if relacion > 6.0:
        return "Excelente"
    elif relacion > 4.0:
        return "Buena"
    elif relacion > 2.5:
        return "Regular"
    elif relacion > 1.5:
        return "Mala"
    else:
        return "Muy Contaminado"

print("📡 Iniciando lectura continua... Ctrl+C para salir.")

try:
    while True:
        linea = arduino.readline().decode('utf-8').strip()
        if linea.count(',') == 2:
            datos = linea.split(',')
            try:
                temp = float(datos[0])
                hum = float(datos[1])
                mq = float(datos[2])
                rs_ro = mq / Ro
                calidad = interpretar_calidad_relativa(mq)

                ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{ahora}] Temp: {temp}°C | Hum: {hum}% | MQ: {mq} | Rs/Ro: {rs_ro:.2f} | Calidad: {calidad}")
            except:
                continue

except KeyboardInterrupt:
    print("\n🛑 Lectura finalizada por el usuario.")
    arduino.close()
