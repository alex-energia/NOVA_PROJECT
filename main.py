import os 
from flask import Flask, render_template_string, request 
import random, math 
from datetime import datetime 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    hr = datetime.now().hour 
    temp_sim = 20 + 5 * math.sin(math.pi * (hr - 6) / 12) + random.uniform(-0.5, 0.5) 
    base_c = 412.0 
    biomasa_factor = 15.5 * (1 + math.cos(math.pi * hr / 12)) 
    captura_neta = biomasa_factor + random.uniform(30, 40) 
    h = [int(50 + 20 * math.sin(i)) for i in range(10)] 
    b_bars = " ".join([f"[#{'#' * (i // 10)}{'.' * (10 - i // 10)}]" for i in h]) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = f"NOVA_AI: Analizando ciclo circadiano (Hora:{hr}:00). Captura neta optimizada por biomasa." 
        chat_history.append((u_m, res)) 
    html = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    html += "<h1 style='color:yellow;'> [N.O.V.A. OS - NODO DE SIMULACION BIOLOGICA]</h1>" 
    html += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:20px;'>" 
    html += "<div style='border:2px solid #0f0; padding:20px; background:#050505;'>" 
    html += "<p style='color:cyan; border-bottom:1px solid #0f0;'>[MODULO DE SENSADO DINAMICO]</p>" 
    html += f"<p> >> HORA_SIMULADA: {hr}:00</p>" 
    html += f"<p> >> TEMPERATURA_AMBIENTE: {temp_sim:.2f} C</p>" 
    html += f"<p> >> CO2_REFERENCIA: {base_c} ppm</p>" 
    html += f"<p style='color:yellow;'> >> CAPTURA_ADAPTATIVA: -{captura_neta:.2f} ppm</p></div>" 
    html += "<div style='border:2px solid #0f0; padding:20px; background:#050505;'>" 
    html += "<p style='color:cyan; border-bottom:1px solid #0f0;'>[ANALISIS DE TENDENCIA CIRCADIANA]</p>" 
    html += f"<p style='letter-spacing:2px;'> {b_bars} </p>" 
    html += "<p><small> [Historial extendido: 10 Ciclos de Muestreo] </small></p></div></div>" 
    html += "<div style='margin-top:20px; border:1px solid #444; padding:15px; background:#080808;'>" 
    html += "<h3 style='color:yellow;'> CONSOLA DE COMANDOS EXPERTOS</h3>" 
    html += "<div style='height:120px; overflow-y:scroll; border-left:4px solid #0f0; padding-left:15px;'>" 
    html += "{% for u, r in history %} <p style='color:#aaa;'><b>USER_CMD:</b> {{u}}</p><p style='color:#0f0;'><b>NOVA_LOG:</b> {{r}}</p><hr style='border:0.1px solid #222;'> {% endfor %}</div>" 
    html += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' placeholder='Escribir comando de auditoria...' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0; padding:10px;'><button style='background:#0f0; color:#000; border:none; padding:10px 20px; font-weight:bold; cursor:pointer;'>EJECUTAR</button></form></div>" 
    html += "<p style='color:#444; font-size:12px;'> KERNEL: 4.19.0-NOVA | COMMS: LoRaWAN_READY | STORAGE: FLASH_SECURE </p></body></html>" 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
