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
        chat_history.append((u_m, "Portal Central: Redireccionando consulta...")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - PORTAL DE MANDO CENTRAL]</h1>" 
    h += "<div style='display:flex; gap:20px; margin-bottom:30px;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>MODULE: GREEN-CORE</h2><p>Control de Forraje y Robotica</p></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>MODULE: FIELD-LINK</h2><p>Red LoRa y Auditoria Exterior</p></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px;'><h3>CONSOLA GLOBAL</h3>" 
    h += "{% for u, r in history %}<p><b>U:</b> {{u}}<br><b>N:</b> {{r}}</p>{% endfor %}</div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[GREEN-CORE: CONTROL DE FORRAJE]</h1><p>Estado: Sistema de siembra robotica inicializado...</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[FIELD-LINK: AUDITORIA DE CAMPO]</h1><p>Estado: Escaneando nodos remotos...</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
