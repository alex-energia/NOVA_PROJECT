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
        chat_history.append((u_m, "NOVA_AI: Generando reporte estrategico...")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='document.getElementById(\"modal\").style.display=\"block\"' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>VER EXPEDIENTE DE INVERSION</button>" 
    h += "<div id=\"modal\" style='display:none; position:fixed; top:5%; left:5%; width:90%; height:90%; background:#111; color:white; padding:40px; border:2px solid yellow; overflow-y:scroll; z-index:2000;'>" 
    h += "<button onclick='this.parentElement.style.display=\"none\"' style='float:right; background:red; color:white; padding:10px;'>CERRAR</button>" 
    h += "<h2 style=\"color:yellow\">N.O.V.A. - DOSSIER EJECUTIVO DE INVERSION</h2>" 
    h += "<p><b>1. VIABILIDAD:</b> El proyecto NOVA es viable mediante la convergencia de energia solar y hardware de bajo costo. Reduce la dependencia de insumos externos en un 85 por ciento con un consumo de agua 90 por ciento menor a la ganaderia tradicional.</p>" 
    h += "<p><b>2. RENTABILIDAD:</b> El ROI se estima en 18 meses. Proviene de la reduccion de costos en suplementos, incremento del 20 por ciento en ganancia de peso y venta de excedentes de biomasa.</p>" 
    h += "<p><b>3. BIOTECNOLOGIA:</b> El consumo de nuestro FVH enriquecido altera el PH de la transpiracion del animal, creando un repelente sistemico natural contra moscas y garrapatas, eliminando gastos en quimicos toxicos.</p>" 
    h += "<p><b>4. MITIGACION DE CO2:</b> El forraje NOVA optimiza la fermentacion ruminal, reduciendo la emision de metano y CO2 del ganado hasta en un 40 por ciento. El sistema audita esta reduccion en tiempo real.</p>" 
    h += "<p><b>5. BONOS VERDES:</b> NOVA genera activos financieros. Cada tonelada de CO2 capturada se registra en un ledger digital para su venta en mercados internacionales de Carbon Credits.</p>" 
    h += "<p><b>6. SIEMBRA ROBOTIZADA:</b> 1-Desinfeccion con ozono. 2-Hidratacion con nutrientes y extractos organicos. 3-Siembra automatica Robot Alpha. 4-Germinacion controlada. 5-Crecimiento vertical LED.</p>" 
    h += "<p><b>7. AUTONOMIA:</b> Ecosistema 100 por ciento robotizado con inteligencia artificial. Optimizacion de espacio vertical sin intervencion humana constante.</p></div>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - PORTAL DE MANDO]</h1>" 
    h += "<div style='display:flex; gap:20px; margin-bottom:30px;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>GREEN-CORE</h2><p>Robotica y FVH</p></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>FIELD-LINK</h2><p>Auditoria de Campo</p></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px;'><h3>CHAT EXPERTO</h3>" 
    h += "<div style='height:150px; overflow-y:scroll;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><b>N:</b> {{r}}</p>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px;'><input name='msg' style='flex-grow:1;'><button>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[GREEN-CORE]</h1><p>Robot Alpha: Activo</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[FIELD-LINK]</h1><p>LoRa: Online</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
