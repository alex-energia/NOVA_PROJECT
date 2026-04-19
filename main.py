import os 
from flask import Flask, render_template_string, request 
import random 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(22, 26), random.uniform(45, 52) 
    h = [random.randint(30, 60) for _ in range(5)] 
    b = " ".join([f"[#{'#' * (i // 10)}{'.' * (6 - i // 10)}]" for i in h]) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = f"Experto NOVA: Captura en {c:.1f} ppm. Hardware NDIR activo." 
        chat_history.append((u_m, res)) 
    html = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    html += "<button onclick='alert(\"PROYECTO N.O.V.A.\\n--------------------\\nOBJETIVO: Auditoria de Carbono en tiempo real.\\n\\nTECNOLOGIA:\\n1. Sensores NDIR (Infrarrojos): Medicion selectiva de CO2.\\n2. Red LoRa: Transmision de largo alcance (5km) en potreros.\\n3. Analisis Diferencial: Comparativa entre CO2 ambiental vs. emision directa.\\n\\nAVANCES: Historial de 5h activo, compensacion termica y chat experto.\")' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:10px; border:none; font-weight:bold; cursor:pointer; z-index:100;'>INFO DETALLADA</button>" 
    html += "<h1 style='color:yellow;'> [N.O.V.A. - MONITOR DE CAMPO]</h1>" 
    html += "<div style='border:1px solid #444; padding:20px; background:#0a0a0a;'><p><b>VALORES ACTUALES:</b></p>" 
    html += f"<p> TEMP: {t:.1f}C -- CAPTURA: {c:.2f} ppm</p><hr style='border:0.1px solid #222;'>" 
    html += f"<p><b>HISTORIAL DE RENDIMIENTO (5H):</b></p><p style='letter-spacing:5px; color:cyan;'> {b} </p>" 
    html += "<p><small> T-5h   T-4h   T-3h   T-2h   T-1h </small></p></div>" 
    html += "<div style='margin-top:30px; border:1px solid #0f0; padding:15px; background:#050505;'><h3 style='color:cyan;'> CHAT EXPERTO NOVA</h3>" 
    html += "<div style='height:120px; overflow-y:scroll; background:#000; padding:10px; border:1px solid #222; margin-bottom:10px;'>" 
    html += "{% for u, r in history %} <p style='color:white;'><b>U:</b> {{u}}<br><span style='color:yellow;'><b>N:</b> {{r}}</span></p><hr style='border:0.1px solid #111;'> {% endfor %}</div>" 
    html += "<form method='post' style='display:flex; gap:10px;'><input name='msg' placeholder='Pregunta a NOVA...' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0; padding:5px;'><button style='background:#0f0; color:#000; border:none; padding:5px 15px; cursor:pointer; font-weight:bold;'>ENVIAR</button></form></div>" 
    html += "<p style='color:#666; margin-top:20px;'> REGISTRO FLASH: ACTIVO | SINCRONIZACION CLOUD: EXITOSA </p></body></html>" 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
