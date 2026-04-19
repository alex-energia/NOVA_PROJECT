import os 
from flask import Flask, render_template_string, request 
import random, math 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(23.5, 25.8), random.uniform(412, 428) 
    biom = random.uniform(1.8, 2.5) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        chat_history.append((u_m, "NOVA_AI: Accediendo a base de datos de ingenieria...")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='document.getElementById(\"modal\").style.display=\"block\"' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>ABRIR DOSSIER DE INVERSION ESTRATEGICA</button>" 
    h += "<div id=\"modal\" style='display:none; position:fixed; top:2%; left:2%; width:96%; height:96%; background:#050505; color:white; padding:40px; border:3px solid yellow; overflow-y:scroll; z-index:2000;'>" 
    h += "<button onclick='this.parentElement.style.display=\"none\"' style='float:right; background:red; color:white; padding:10px; border:none; cursor:pointer;'>CERRAR [X]</button>" 
    h += "<h1 style='color:yellow; text-align:center;'>N.O.V.A. - INFORME TECNICO DE ALTO NIVEL</h1><hr style='border:1px solid #333;'>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:30px;'>" 
    h += "<div><h2 style='color:cyan;'>[1. PROTOCOLO DE SIEMBRA ROBOTIZADA]</h2>" 
    h += "<p><b>Paso 1:</b> Desinfeccion mediante Ozono (O3) para eliminar patogenos sin quimicos.</p>" 
    h += "<p><b>Paso 2:</b> Preparacion del sustrato hidroponico con sales minerales, aminoacidos y extractos de neem/ajo (Repelente sistemico).</p>" 
    h += "<p><b>Paso 3:</b> Robot Alpha realiza siembra neumatica con una densidad de 1.2kg/bandeja.</p>" 
    h += "<p><b>Paso 4:</b> Germinacion en camara oscura con humedad del 95 por ciento.</p>" 
    h += "<p><b>Paso 5:</b> Cosecha automatizada al dia 7 mediante brazos mecanicos.</p></div>" 
    h += "<div><h2 style='color:cyan;'>[2. VIABILIDAD Y RENTABILIDAD (ROI)]</h2>" 
    h += "<pre style='background:#111; padding:10px; color:yellow;'>ROI ESTIMADO: 18 MESES\\nRentabilidad: 32 por ciento anual.\\nAhorro en suplementos: 85 por ciento.\\nIncremento peso animal: 22 por ciento.</pre>" 
    h += "<p>La viabilidad se sustenta en la autonomia energetica y la eliminacion de la cadena de suministro externa de forraje.</p></div>" 
    h += "<div><h2 style='color:cyan;'>[3. BIOTECNOLOGIA: EFECTO REPELENTE]</h2>" 
    h += "<p>El forraje NOVA no es solo alimento. Al estar enriquecido con compuestos organicos durante la siembra, el animal al ingerirlo modifica el olor de su transpiracion de forma imperceptible para humanos pero letal para moscas y garrapatas. <b>Reduccion del 90 por ciento en uso de ivermectinas.</b></p></div>" 
    h += "<div><h2 style='color:cyan;'>[4. AUDITORIA DE CARBONO (BONOS VERDES)]</h2>" 
    h += "<p>Nuestros sensores NDIR en potrero miden el balance neto. El animal alimentado con FVH emite 40 por ciento menos metano. Estos datos se certifican y se venden como Bonos de Carbono, pagando gran parte de la operacion.</p></div>" 
    h += "</div><h2 style='color:yellow; border-top:1px solid #333; padding-top:20px;'>[5. INVERNADERO VERTICAL ROBOTIZADO]</h2>" 
    h += "<p>Sistema modular con 10 niveles de produccion. Los rieles motorizados mueven las bandejas hacia la luz LED de espectro completo, simulando el ciclo solar perfecto los 365 dias del a¤o.</p></div>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - DASHBOARD CENTRAL]</h1>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:20px; border:2px solid #0f0; padding:20px; background:#050505;'>" 
    h += f"<div><p style='color:cyan;'>METRICAS DE CAMPO (FIELD-LINK)</p><p> >> CO2 POTRERO: {c:.2f} ppm</p><p> >> NODOS LORA: 5 ACTIVOS</p></div>" 
    h += f"<div><p style='color:cyan;'>METRICAS INVERNADERO (GREEN-CORE)</p><p> >> TEMP: {t:.1f} C</p><p style='color:yellow;'> >> BIOMASA: {biom:.2f} KG/B</p></div>" 
    h += "</div><div style='display:flex; gap:20px; margin:20px 0;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>ACCEDER GREEN-CORE</h2></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>ACCEDER FIELD-LINK</h2></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px; background:#080808;'>" 
    h += "<h3>SISTEMA DE CONSULTA NOVA AI</h3>" 
    h += "<div style='height:100px; overflow-y:scroll;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><span style='color:yellow;'><b>N:</b> {{r}}</span></p>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0;'><button style='background:#0f0; color:#000; font-weight:bold;'>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[DETALLE GREEN-CORE]</h1><p>Monitoreo de biomasa y control de riego nebulizado activo...</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[DETALLE FIELD-LINK]</h1><p>Escaneo diferencial de CO2 ambiental activo...</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
