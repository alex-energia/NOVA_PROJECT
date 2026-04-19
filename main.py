import os
from flask import Flask, render_template_string
import random
app = Flask(__name__)
@app.route('/')
def home():
    co2_ambiente = random.uniform(400, 450)
    co2_vacunos = random.uniform(500, 700)
    captura_interna = random.uniform(5.5, 12.8)
    balance = (co2_vacunos + co2_ambiente) - (captura_interna * 10)
    html = f"""
    <body style='background:#000; color:#0f0; font-family:monospace; padding:30px; line-height:1.6;'>
        <h1 style='color:#fff; border-bottom:1px solid #0f0;'> [SISTEMA N.O.V.A. - MONITOR MULTI-SENSOR]</h1>
        <div style='border:1px solid #333; padding:15px; background:#050505;'>
            <p><b>[ENTORNO EXTERIOR]</b></p>
            <p> > CO2 ATMOSFERICO: {co2_ambiente:.2f} ppm</p>
            <p> > EMISION VACUNOS: {co2_vacunos:.2f} ppm</p>
        <hr style='border:0.5px dashed #333;'>
            <p><b>[SISTEMA INVERNADERO]</b></p>
            <p> > CAPTURA ACTIVA: {captura_interna:.2f} kg/dia</p>
            <p> > BALANCE NETO: {balance:.2f} pts</p>
        </div>
        <br>
        <marquee scrollamount='3'> >>> ANALIZANDO FLUJO DE GASES... OPTIMIZANDO CAPTURA DE CARBONO... </marquee>
    </body>"""
    return html
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
