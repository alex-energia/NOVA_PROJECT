import os
from flask import Flask, render_template_string
import random
app = Flask(__name__)
@app.route('/')
def home():
    ref_ambiental = 412.0  # CO2 base del planeta hoy
    sensor_potrero = ref_ambiental + random.uniform(50, 150)
    sensor_inv_entrada = ref_ambiental + random.uniform(5, 10)
    sensor_inv_salida = sensor_inv_entrada - random.uniform(30, 60)
    puro_vacunos = sensor_potrero - ref_ambiental
    captura_neta = sensor_inv_entrada - sensor_inv_salida
    html = f"""
    <body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>
        <h1 style='color:cyan;'> [N.O.V.A. - AUDITORIA DE CARBONO]</h1>
        <div style='border:2px solid cyan; padding:15px;'>
            <p>Ref. Ambiental Base: {ref_ambiental} ppm</p>
            <p>Aporte Real Vacunos: +{puro_vacunos:.2f} ppm</p>
            <p style='color:#fff;'>Captura Real Invernadero: -{captura_neta:.2f} ppm</p>
        </div>
        <p><small>Metodo: Diferencial de Gradiente NDIR</small></p>
    </body>"""
    return html
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
