import time
import datetime
import json
import random
from flask import Flask, jsonify # Importamos Flask para la interfaz web

# --- INICIALIZACIÓN DE LA APP PARA RENDER ---
app = Flask(__name__)

class InvernaderoNova:
    def __init__(self, id_lote):
        self.id_lote = id_lote
        self.dia_actual = 0
        self.altura_forraje_mm = 0
        self.proteina_pct = 0.0
        self.co2_mitigado_kg = 0.0
        self.energia_solar_kwh = 0.0
        self.estado_sistema = "INICIANDO_CONEXION"
        self.log_trazabilidad = []
        
    def obtener_telemetria(self):
        """Devuelve el estado actual para el mímico de la URL."""
        return {
            "lote": self.id_lote,
            "dia": self.dia_actual,
            "estado": self.estado_sistema,
            "altura": f"{self.altura_forraje_mm}mm",
            "proteina": f"{self.proteina_pct}%",
            "co2_capturado": f"{self.co2_mitigado_kg}kg",
            "energia_acumulada": f"{self.energia_solar_kwh}kWh",
            "timestamp": datetime.datetime.now().isoformat()
        }

    def actualizar_ciclo(self):
        """Lógica de progresión biotecnológica día por día."""
        if self.dia_actual > 7: return

        # Simulación de crecimiento y biotecnología según la Hoja de Ruta
        if self.dia_actual == 0:
            self.estado_sistema = "DIA_0: ACTIVACION_MINERAL"
        elif self.dia_actual == 3:
            self.estado_sistema = "DIA_3: FOTOSINTESIS_LED"
            self.altura_forraje_mm = 75
            self.proteina_pct = 12.0
        elif self.dia_actual == 4:
            self.estado_sistema = "DIA_4: INYECCION_NEEM_AJO"
            self.altura_forraje_mm = 135
            self.proteina_pct = 18.5
        elif self.dia_actual == 7:
            self.estado_sistema = "DIA_7: COSECHA_Y_BONOS_VERDES"
            self.altura_forraje_mm = 250
            self.proteina_pct = 22.5
            self.co2_mitigado_kg += 4.5
        
        self.energia_solar_kwh += random.uniform(5.0, 10.0)
        self.dia_actual += 1

# Instancia global del motor NOVA
nova_motor = InvernaderoNova("BATCH-001-BIOTECH")

# --- RUTAS PARA LA URL DE NOVA ---

@app.route('/')
def home():
    return "N.O.V.A. System Online - Motor de Trazabilidad Activo"

@app.route('/api/telemetria')
def api_telemetria():
    """Esta ruta será consultada por el mímico visual cada vez que necesite actualizarse."""
    nova_motor.actualizar_ciclo() # Avanza un día en cada consulta para la simulación
    return jsonify(nova_motor.obtener_telemetria())

if __name__ == "__main__":
    # Para pruebas locales
    app.run(host='0.0.0.0', port=5000)
