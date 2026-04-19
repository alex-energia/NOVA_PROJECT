# -- PROTOCOLO DE BLINDAJE N.O.V.A --
from flask import Flask, render_template_string
import os

# Diccionario Maestro de Configuracion
NOVA_DATA = {
    "identidad": "N.O.V.A.",
    "mision": "Nano Organico Vertical Automatizado + Sostenible",
    "objetivos": {
        "proteina": "22%",
        "carbono": "Captura CO2 - Bonos Verdes",
        "repelencia": "Sistemica Nano-Botanica",
        "automatizacion": "100% Robotica"
    },
    "web": {
        "host": "0.0.0.0",
        "port": int(os.environ.get("PORT", 10000))
    }
}

app = Flask(__name__)

@app.route('/')
def home():
    # Estructura visual blindada
    return render_template_string("""
    <body style="background:#000; color:#0f0; font-family:monospace; padding:20px;">
        <h1>SISTEMA {{ d.identidad }} ACTIVO</h1>
        <p>{{ d.mision }}</p>
        <hr>
        <ul>
            <li>PROV: {{ d.objetivos.proteina }}</li>
            <li>ENV: {{ d.objetivos.carbono }}</li>
            <li>SAFE: {{ d.objetivos.repelencia }}</li>
            <li>AUTO: {{ d.objetivos.automatizacion }}</li>
        </ul>
        <br>
        <small>URL GENERADA PARA RENDER - MODO SIMULACION</small>
    </body>
    """, d=NOVA_DATA)

if __name__ == "__main__":
    app.run(host=NOVA_DATA["web"]["host"], port=NOVA_DATA["web"]["port"])
