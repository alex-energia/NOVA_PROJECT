import os 
from flask import Flask, render_template_string, request 
import random, math 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = "NOVA_AI: En linea. Seleccione modulo para diagnostico detallado." 
        chat_history.append((u_m, res)) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='alert(\"PROYECTO N.O.V.A. - MANIFIESTO COMPLETO\\n1. FORRAJE (REY): Captura intensiva en invernadero.\\n2. AUDITORIA: Medicion diferencial de CO2.\\n3. ROBOTICA: Siembra y desplazamiento automatizado.\\n4. LORA: Conectividad total en campo.\")' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>INFO PROYECTO</button>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - SISTEMA DE GESTION INTEGRAL]</h1>" 
    h += "<div style='display:flex; gap:20px; margin-bottom:30px;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>GREEN-CORE</h2><p>Forraje y Robotica</p></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>FIELD-LINK</h2><p>CO2 y Medicion Exterior</p></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px; background:#080808;'>" 
    h += "<h3 style='color:yellow;'>CHAT EXPERTO NOVA (CENTRAL)</h3>" 
    h += "<div style='height:150px; overflow-y:scroll; border-left:4px solid #0f0; padding-left:15px;'>" 
    h += "{% for u, r in history %}<p><b>U:</b> {{u}}<br><span style='color:yellow;'><b>N:</b> {{r}}</span></p><hr style='border:0.1px solid #222;'>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' placeholder='Consulta global...' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0; padding:10px;'><button style='background:#0f0; color:#000; border:none; padding:10px 20px; font-weight:bold;'>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    dia = random.randint(1, 7) 
    biomasa = 1.5 * (1.6 ** dia) 
    h = f"<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow; text-decoration:none;'><- VOLVER AL PORTAL</a><h1>[GREEN-CORE: MODULO DE FORRAJE]</h1>" 
    h += f"<div style='border:2px solid #0f0; padding:20px;'><h3>ESTADO DE PRODUCCION ROBOTICA</h3><p>>> DIA DEL CICLO: {dia}</p><p>>> ESTACION: SIEMBRA/CRECIMIENTO</p>" 
    h += f"<p style='color:yellow;'>>> BIOMASA ESTIMADA: {biomasa:.2f} kg</p>" 
    h += "<p>[######....] 60% Eficiencia Fotosintetica</p></div></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    co2 = random.uniform(410, 480) 
    h = f"<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow; text-decoration:none;'><- VOLVER AL PORTAL</a><h1>[FIELD-LINK: AUDITORIA EXTERIOR]</h1>" 
    h += f"<div style='border:2px solid cyan; padding:20px;'><h3>MONITOREO DE CARBONO EN POTRERO</h3><p>>> CO2 AMBIENTAL: {co2:.2f} ppm</p>" 
    h += "<p>>> ESTADO RED LoRa: OPTIMO (Nodos 1-5)</p>" 
    h += "<p style='color:white;'>[HISTORIAL: ####.####.####]</p></div></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
