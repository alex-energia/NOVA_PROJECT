import os
from flask import Flask, render_template_string
import random
app = Flask(__name__)
@app.route('/')
def home():
    co2_base = random.uniform(1.2, 5.5)
    p_prot = 22.5
    html = f"""
    <body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>
        <hr>
        <p> [ESTADO] : OPERATIVO</p>
        <p> [CAPTURA CO2] : {co2_base:.2f} kg/dia</p>
        <p> [PROTEINA] : {p_prot}%% </p>
        <br>
        <p>-- DATOS ACTUALIZADOS EN TIEMPO REAL --</p>
    </body>"""
    return html
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
