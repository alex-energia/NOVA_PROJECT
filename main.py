import time
import datetime
import json
import random

class InvernaderoNova:
    """
    Motor Central de N.O.V.A. - Gestiona el Gemelo Digital y la Trazabilidad.
    """
    def __init__(self, id_lote):
        self.id_lote = id_lote
        self.dia_actual = 0
        self.altura_forraje_mm = 0
        self.proteina_pct = 0.0
        self.co2_mitigado_kg = 0.0
        self.energia_solar_kwh = 0.0
        self.estado_sistema = "STANDBY"
        self.log_trazabilidad = []
        
        # Parámetros Biotecnológicos
        self.mezcla_semillas = {"maiz": 105, "cebada": 15, "alfalfa": 5} # kg
        self.protocolo_defensa = "DESACTIVADO"
        self.nivel_hidratacion = 0
        
    def registrar_evento(self, fase, descripcion):
        evento = {
            "timestamp": datetime.datetime.now().isoformat(),
            "dia": self.dia_actual,
            "fase": fase,
            "descripcion": descripcion,
            "telemetria": {
                "altura": f"{self.altura_forraje_mm}mm",
                "proteina": f"{self.proteina_pct}%",
                "co2": f"{self.co2_mitigado_kg}kg"
            }
        }
        self.log_trazabilidad.append(evento)
        print(f">>> [DIA {self.dia_actual}] {fase}: {descripcion}")

    def ejecutar_ciclo_7_dias(self):
        print(f"--- INICIANDO CICLO BIOTECNOLÓGICO LOTE {self.id_lote} ---")
        
        for dia in range(8): # Del Día 0 al Día 7
            self.dia_actual = dia
            self.simular_procesos_diarios()
            time.sleep(1) # Simulación de paso de tiempo (1s = 1 día)

    def simular_procesos_diarios(self):
        # --- Lógica de Energía (Común a todos los días) ---
        self.energia_solar_kwh += round(random.uniform(12.5, 15.0), 2)

        if self.dia_actual == 0:
            self.estado_sistema = "CARGA_Y_ACTIVACION"
            self.nivel_hidratacion = 100
            self.registrar_evento("DÍA CERO", "Robot Stacker posiciona bandejas. Inicio de imbibición mineral.")

        elif self.dia_actual == 1:
            self.estado_sistema = "GERMINACION_OSCURA"
            self.altura_forraje_mm = 5
            self.registrar_evento("EMERGENCIA", "Radículas visibles. Temperatura estable en 21°C.")

        elif self.dia_actual == 2:
            self.estado_sistema = "DESARROLLO_RADICULAR"
            self.altura_forraje_mm = 25
            self.registrar_evento("ANCLAJE", "El tapete comienza a entrelazar raíces de alfalfa y gramíneas.")

        elif self.dia_actual == 3:
            self.estado_sistema = "FOTOSINTESIS_ACTIVA"
            self.altura_forraje_mm = 70
            self.proteina_pct = 12.5
            self.registrar_evento("LED_ON", "Activación de espectro completo. Inicio de síntesis proteica.")

        elif self.dia_actual == 4:
            self.estado_sistema = "BIOFORTIFICACION_SISTEMICA"
            self.protocolo_defensa = "ACTIVO"
            self.altura_forraje_mm = 130
            self.registrar_evento("INMUNIDAD", "Inyección de Neem y Ajo. La planta organifica los compuestos.")

        elif self.dia_actual == 5:
            self.estado_sistema = "CRECIMIENTO_EXPONENCIAL"
            self.altura_forraje_mm = 190
            self.proteina_pct = 18.0
            self.registrar_evento("BIOMASA", "Máxima absorción de CO2 detectada por sensores internos.")

        elif self.dia_actual == 6:
            self.estado_sistema = "MADURACION_NUTRICIONAL"
            self.altura_forraje_mm = 230
            self.proteina_pct = 21.5
            self.registrar_evento("PRE-COSECHA", "Nivel óptimo de minerales y aminoácidos alcanzado.")

        elif self.dia_actual == 7:
            self.estado_sistema = "COSECHA_Y_ENTREGA"
            self.altura_forraje_mm = 250
            self.co2_mitigado_kg = 4.5 # Meta lograda
            self.registrar_evento("ENTREGA", "Tapete listo para animal vacuno. Robot de despacho activo.")
            self.generar_reporte_trazabilidad()

    def generar_reporte_trazabilidad(self):
        filename = f"TRAZABILIDAD_{self.id_lote}.json"
        with open(filename, 'w') as f:
            json.dump(self.log_trazabilidad, f, indent=4)
        print(f"\n[ARCHIVO GENERADO] Reporte completo guardado en {filename}")

if __name__ == "__main__":
    nova_sim = InvernaderoNova("BATCH-001-ALPHA")
    nova_sim.ejecutar_ciclo_7_dias()