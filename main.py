import os 
from flask import Flask, render_template_string, request 
import random 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(23, 25), random.uniform(48, 51) 
    h = [random.randint(40, 70) for _ in range(7)] 
    b = " ".join([f"[#{'#' * (i // 10)}{'.' * (7 - i // 10)}]" for i in h]) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = f"Experto NOVA: Analizando {c:.1f} ppm. Simulador activo en modo Real-Time." 
        chat_history.append((u_m, res)) 
    html = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    html += "<button onclick='alert(\"PROYECTO N.O.V.A. (Nodo Operativo de Vigilancia Ambiental)\\n\\n1. OBJETIVO GENERAL: Cuantificar la captura y emision de carbono en ecosistemas ganaderos mediante sensores NDIR de alta precision.\\n\\n2. ALCANCE: Cobertura de 50 hectareas mediante nodos LoRa autonomos, integrando compensacion termica y humedad para evitar falsos positivos.\\n\\n3. METODOLOGIA: Medicion diferencial. Comparamos aire ambiental (Base 412ppm) vs Medicion Directa para calcular la Tasa de Captura Adaptativa.\\n\\n4. IMPACTO: Generar certificados de carbono verificables para ganaderia sostenible.\")' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:10px; border:none; font-weight:bold; cursor:pointer; z-index:100;'>INFO PROYECTO</button>" 
    html += "<h1 style='color:yellow;'> [N.O.V.A. - SIMULADOR EN TIEMPO REAL]</h1>" 
    html += "<div style='border:2px solid #0f0; padding:20px; background:#050505;'>" 
    html += f"<p style='color:cyan;'>[STATUS: EJECUTANDO SIMULACION DINAMICA]</p>" 
    html += f"<p> >> TEMPERATURA_NODO: {t:.1f}C</p>" 
    html += f"<p> >> CAPTURA_CARBONO: {c:.2f} ppm</p>" 
    html += "<hr style='border:1px dashed #333;'>" 
    html += f"<p><b>TENDENCIA DE CAPTURA (Ultimas 7 mediciones):</b></p><p style='letter-spacing:3px; color:cyan;'> {b} </p>" 
    html += "<p><small> T-7h   T-6h   T-5h   T-4h   T-3h   T-2h   T-1h </small></p></div>" 
    html += "<div style='margin-top:20px; border:1px solid #444; padding:15px;'>" 
    html += "<h3 style='color:yellow;'> INTERFAZ DE CONSULTA EXPERTA</h3>" 
    html += "<div style='height:100px; overflow-y:scroll; background:#000; padding:10px;'>" 
    html += "{% for u, r in history %} <p><b>U:</b> {{u}}<br><span style='color:white;'><b>N:</b> {{r}}</span></p> {% endfor %}</div>" 
    html += "<form method='post' style='display:flex; gap:5px; margin-top:10px;'><input name='msg' placeholder='Comando...' style='flex-grow:1; background:#111; color:#0f0; border:1px solid #0f0;'><button style='background:#0f0; color:#000; border:none; padding:5px 15px; font-weight:bold;'>ENVIAR</button></form></div>" 
    html += "<p style='color:#444; font-size:10px; margin-top:10px;'> NOVA_OS v2.4 | MODO_SIMULADOR: ON | ENERGIA: EXTERNA </p></body></html>" 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
