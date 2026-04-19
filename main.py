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
        res = "Controlador Central: Seleccione modulo (Invernadero/Campo) para diagnostico especifico." 
        chat_history.append((u_m, res)) 
    return render_template_string(html, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    html = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[GREEN-CORE: CONTROL DE FORRAJE]</h1><p>Estado: Simulacion Robotica Activa...</p></body></html>" 
    return render_template_string(html) 
@app.route('/campo') 
def campo(): 
    html = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[FIELD-LINK: AUDITORIA DE CAMPO]</h1><p>Estado: Escaneando Nodos LoRa...</p></body></html>" 
    return render_template_string(html) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
