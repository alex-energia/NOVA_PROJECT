import os 
from flask import Flask, render_template_string, request 
import random, math 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(24.5, 26.1), random.uniform(410, 430) 
    biom = random.uniform(1.8, 2.4) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        chat_history.append((u_m, "NOVA_AI: Accediendo a los protocolos maestros...")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='document.getElementById(\"modal\").style.display=\"block\"' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>EXPEDIENTE TECNICO DE INVERSION</button>" 
    h += "<div id=\"modal\" style='display:none; position:fixed; top:2%; left:2%; width:96%; height:96%; background:#050505; color:white; padding:40px; border:3px solid yellow; overflow-y:scroll; z-index:2000; font-size:14px;'>" 
    h += "<button onclick='this.parentElement.style.display=\"none\"' style='float:right; background:red; color:white; padding:10px; border:none;'>CERRAR [X]</button>" 
    h += "<h1 style='color:yellow; text-align:center;'>N.O.V.A. - DOSSIER ESTRATEGICO PARA INVERSIONISTAS</h1><hr style='border:1px solid #444;'>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:30px;'>" 
    h += "<div><h3 style='color:cyan;'>[1. VIABILIDAD Y RENTABILIDAD]</h3>" 
    h += "<p>El proyecto NOVA es viable mediante el uso de energia solar y hardware de bajo costo. Reduce los insumos externos al 85 por ciento. ROI proyectado: 18 meses. Rentabilidad directa por ahorro en nutricion y venta de excedentes de biomasa.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[2. BIOTECNOLOGIA: REPELENTE NATURAL]</h3>" 
    h += "<p>El forraje NOVA incluye extractos de neem y ajo. Al ser consumido, modifica el PH de la transpiracion del animal, creando un repelente natural contra moscas y garrapatas. Esto elimina el gasto en quimicos toxicos e ivermectinas.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[3. AUDITORIA DE CARBONO Y BONOS VERDES]</h3>" 
    h += "<p>La digestion optimizada con FVH reduce el metano y CO2 animal en un 40 por ciento. Los nodos Field-Link certifican esta reduccion para la emision de Carbon Credits (Bonos Verdes) que financian la operacion.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[4. ARQUITECTURA VERTICAL ROBOTIZADA]</h3>" 
    h += "<p>Sistema de 10 niveles con rieles motorizados NEMA 23. Desplazamiento inteligente hacia luz LED de espectro solar. El sistema es totalmente automatizado y gestionado por inteligencia artificial.</p></div>" 
    h += "</div><div style='background:#111; padding:20px; border:1px solid yellow; margin-top:20px;'>" 
    h += "<h3 style='color:yellow;'>[5. PROCESO DE SIEMBRA ROBOTICA]</h3>" 
    h += "<p>Ingredientes: Semilla certificada, Ozono (O3), Solucion Mineral y Extractos Organicos. <br>Flujo: Desinfeccion -> Hidratacion Nutritiva -> Siembra Robot Alpha -> Germinacion en Oscuridad -> Crecimiento Vertical Progresivo.</p></div></div>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - DASHBOARD OPERATIVO]</h1>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:20px; border:2px solid #0f0; padding:20px; background:#050505;'>" 
    h += f"<div><p style='color:cyan;'>FIELD-LINK (CAMPOS)</p><p> >> CO2_AMBIENTAL: {c:.2f} ppm</p><p> >> NODOS_LORA: 5 ACTIVOS</p></div>" 
    h += f"<div><p style='color:cyan;'>GREEN-CORE (INVERNADERO)</p><p> >> BIOMASA_TOTAL: {biom:.2f} KG/B</p><p> >> TEMP_CONTROL: {t:.1f} C</p></div>" 
    h += "</div><div style='display:flex; gap:20px; margin:20px 0;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>GREEN-CORE</h2></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>FIELD-LINK</h2></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px; background:#080808;'>" 
    h += "<h3>CHAT EXPERTO MAESTRO</h3>" 
    h += "<div style='height:120px; overflow-y:scroll;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><span style='color:yellow;'><b>N:</b> {{r}}</span></p><hr style='border:0.1px solid #222;'>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0;'><button style='background:#0f0; color:#000; font-weight:bold;'>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[DETALLE GREEN-CORE]</h1><p>Sistema robotico de siembra y riego activo.</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[DETALLE FIELD-LINK]</h1><p>Escaneo de carbono en potreros activo.</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
