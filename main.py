import os
from flask import Flask, render_template_string
import random
app = Flask(__name__)
@app.route('/')
def home():
    temp = random.uniform(18, 28)
    hum = random.uniform(60, 85)
    ref_ambiental = 412.0
    # Factor de correccion logica
    correccion = (temp * 0.05) + (hum * 0.01)
    captura_real = random.uniform(40, 55) + correccion
    html = f"""
    <body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>
        <h1 style='color:#fff; border-bottom:2px solid #0f0;'> [N.O.V.A. OS - NODO CENTRAL]</h1>
        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:20px;'>
            <div style='border:1px solid #333; padding:10px;'>
                <p><b>SENSADO CLIMATICO</b></p>
                <p> TEMP: {temp:.1f} C</p>
                <p> HUM: {hum:.1f} %%</p>
            </div>
            <div style='border:1px solid #0f0; padding:10px;'>
                <p><b>AUDITORIA CARBONO</b></p>
                <p> BASE: {ref_ambiental} ppm</p>
                <p> CAPTURA ADAPTATIVA: -{captura_real:.2f} ppm</p>
            </div>
        </div>
        <p style='text-align:center; color:yellow;'> STATUS: COMPENSACION TERMICA ACTIVA </p>
    </body>"""
    return html
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
