import datetime
import random
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

class InvernaderoNova:
    def __init__(self, id_lote):
        self.id_lote = id_lote
        self.dia_actual = 0
        self.altura_forraje_mm = 0
        self.proteina_pct = 0.0
        self.co2_mitigado_kg = 0.0
        self.energia_solar_kwh = 0.0
        self.estado_sistema = "INICIALIZANDO BANDA"
        
    def actualizar_datos(self):
        # Simulación de progresión día a día
        if self.dia_actual < 7:
            self.dia_actual += 1
            self.altura_forraje_mm += 35
            self.energia_solar_kwh += random.uniform(8.0, 12.0)
            
            if self.dia_actual == 0: self.estado_sistema = "DIA 0: ACTIVACIÓN MINERAL"
            elif self.dia_actual == 3: 
                self.estado_sistema = "DIA 3: FOTOSÍNTESIS LED"
                self.proteina_pct = 14.5
            elif self.dia_actual == 4: 
                self.estado_sistema = "DIA 4: BIO-INYECCIÓN NEEM/AJO"
                self.proteina_pct = 19.0
            elif self.dia_actual == 7: 
                self.estado_sistema = "DIA 7: COSECHA Y BONOS VERDES"
                self.proteina_pct = 22.5
                self.co2_mitigado_kg = 4.5
        else:
            self.dia_actual = 0 # Reinicio para demostración continua
            self.altura_forraje_mm = 0

# Instancia del motor
nova_motor = InvernaderoNova("BATCH-001-BIOTECH")

# --- INTERFAZ VISUAL (HTML/CSS) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA Dashboard</title>
    <meta http-equiv="refresh" content="3"> <style>
        body { font-family: sans-serif; background: #121212; color: white; text-align: center; }
        .container { display: flex; justify-content: space-around; padding: 20px; }
        .invernadero { border: 2px solid #27ae60; width: 300px; height: 500px; display: flex; flex-direction: column-reverse; }
        .piso { border: 1px solid #333; flex: 1; display: flex; align-items: center; justify-content: center; font-size: 10px; }
        .activo { background: #2ecc71; color: black; font-weight: bold; }
        .stats { text-align: left; background: #1e1e1e; padding: 20px; border-radius: 10px; }
        .biotech-alert { color: #f1c40f; font-weight: bold; animation: blink 1s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <h1>🛰️ N.O.V.A. DIGITAL TWIN</h1>
    <div class="container">
        <div class="invernadero">
            {% for i in range(10) %}
                <div class="piso {{ 'activo' if (i + 1) == dia else '' }}">PISO {{ i + 1 }}</div>
            {% endfor %}
        </div>
        <div class="stats">
            <h2>📊 Telemetría Lote: {{ lote }}</h2>
            <p><b>Día de Ciclo:</b> {{ dia }} / 7</p>
            <p><b>Estado:</b> <span class="biotech-alert">{{ estado }}</span></p>
            <hr>
            <p><b>Altura Biomasa:</b> {{ altura }} mm</p>
            <p><b>Proteína Estimada:</b> {{ proteina }}%</p>
            <p><b>Captura CO2:</b> {{ co2 }} kg</p>
            <p><b>Energía Solar:</b> {{ energia }} kWh</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    nova_motor.actualizar_datos()
    return render_template_string(HTML_TEMPLATE, 
                                 lote=nova_motor.id_lote,
                                 dia=nova_motor.dia_actual,
                                 estado=nova_motor.estado_sistema,
                                 altura=nova_motor.altura_forraje_mm,
                                 proteina=nova_motor.proteina_pct,
                                 co2=nova_motor.co2_mitigado_kg,
                                 energia=round(nova_motor.energia_solar_kwh, 2))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)