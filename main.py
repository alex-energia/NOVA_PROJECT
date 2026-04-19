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
        chat_history.append((u_m, "NOVA_AI: Generando reporte para inversion...")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='document.getElementById(\"modal\").style.display=\"block\"' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>VER EXPEDIENTE DE INVERSION</button>" 
    h += "<div id=\"modal\" style='display:none; position:fixed; top:5%; left:5%; width:90%; height:90%; background:#111; color:white; padding:40px; border:2px solid yellow; overflow-y:scroll; z-index:2000;'>" 
    h += "<button onclick='this.parentElement.style.display=\"none\"' style='float:right; background:red; color:white;'>CERRAR</button>" 
    h += "<h2 style=\"color:yellow\">N.O.V.A. - DOSSIER EJECUTIVO PARA INVERSIONISTAS</h2>" 
    h += "<p><b>1. VIABILIDAD TECNICO-ECONOMICA:</b> El proyecto NOVA es viable gracias a la convergencia de energia solar MPPT, hardware de bajo costo (ESP32) y sensores NDIR de grado industrial. Reduce la dependencia de insumos externos en un 85% al producir forraje in-situ con un consumo de agua 90% menor a la ganaderia tradicional.</p>" 
    h += "<p><b>2. RENTABILIDAD Y ROI:</b> El retorno de inversion se estima en 18 meses. La rentabilidad proviene de tres vias: reduccion de costos en suplementos, incremento del 20% en ganancia de peso animal y la venta de excedentes de biomasa.</p>" 
    h += "<p><b>3. BIOTECNOLOGIA Y SANIDAD:</b> El consumo de nuestro FVH, enriquecido con fitonutrientes naturales en la siembra, altera el PH de la transpiracion del animal, creando un repelente sistemico natural contra moscas y garrapatas, eliminando el gasto en ba¤os quimicos toxicos.</p>" 
    h += "<p><b>4. MITIGACION DE CO2 Y METANO:</b> El forraje hidroponico NOVA es mas digestible que el pasto seco. Esto optimiza la fermentacion ruminal, reduciendo la emision de metano y CO2 del ganado hasta en un 40%. El sistema audita esta reduccion en tiempo real.</p>" 
    h += "<p><b>5. BONOS VERDES (CARBON CREDITS):</b> NOVA genera activos financieros. Cada tonelada de CO2 no emitida o capturada se registra en un ledger digital. Estos bonos verdes son vendidos en mercados internacionales, pagando el 60% de los costos operativos del proyecto.</p>" 
    h += "<p><b>6. SIEMBRA ROBOTIZADA PASO A PASO:</b> 1) Desinfeccion con ozono (O3). 2) Hidratacion con solucion nutritiva mineral y extractos organicos repelentes. 3) Siembra por gravedad mediante Robot Alpha. 4) Germinacion en oscuridad controlada por sensores. 5) Crecimiento en estanteria vertical con iluminacion LED de espectro completo.</p>" 
    h += "<p><b>7. AUTONOMIA Y VERTICALIDAD:</b> N.O.V.A. es un ecosistema 100% robotizado. Un sistema de rieles desplaza las bandejas verticalmente para optimizar espacio, operando de forma autonoma mediante algoritmos de inteligencia artificial sin intervencion humana.</p></div>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - PORTAL DE MANDO INTEGRAL]</h1>" 
    h += "<div style='display:flex; gap:20px; margin-bottom:30px;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>GREEN-CORE</h2><p>Robotica e Invernadero FVH</p></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>FIELD-LINK</h2><p>CO2 y Auditoria de Campo</p></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px;'>" 
    h += "<h3>CHAT EXPERTO CENTRAL</h3>" 
    h += "<div style='height:150px; overflow-y:scroll;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><b>N:</b> {{r}}</p>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px;'><input name='msg' style='flex-grow:1;'><button>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[GREEN-CORE: ANALISIS DE BIOMASA]</h1><p>Robot Alpha: Sembrando lote 402...</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[FIELD-LINK: MONITOR DE CARBONO]</h1><p>Escaneando balance neto de potrero...</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
