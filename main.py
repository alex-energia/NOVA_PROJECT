import os 
from flask import Flask, render_template_string 
import random 
app = Flask(__name__) 
@app.route('/') 
def home(): 
    t, c = random.uniform(22, 26), random.uniform(45, 52) 
    h = [random.randint(30, 60) for _ in range(5)] 
    b = " ".join([f"[#{'#' * (i // 10)}{'.' * (6 - i // 10)}]" for i in h]) 
    st = random.choice(["OPTIMO", "OPTIMO", "ALERTA: SE¥AL DEBIL"]) 
    html = f"<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><h1 style='color:yellow;'> [N.O.V.A. - MONITOR DE CAMPO]</h1><div style='border:1px solid #444; padding:20px; background:#0a0a0a;'><p> TEMP: {t:.1f}C -- CAPTURA: {c:.2f} ppm</p><hr style='border:0.1px solid #333;'><p style='letter-spacing:5px; color:cyan;'> {b} </p><p><small> T-5h   T-4h   T-3h   T-2h   T-1h </small></p></div><p style='text-align:center;'> ESTADO LORA: <span style='color:white; background:red; padding:2px;'>{st}</span></p><p style='color:#666;'> REGISTRO FLASH: ACTIVO </p></body></html>" 
    return html 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
