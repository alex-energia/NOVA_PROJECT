import os 
from flask import Flask, render_template_string, request 
import random, math 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(22, 26), random.uniform(410, 430) 
    biomasa_fv = random.uniform(1.5, 2.2) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        chat_history.append((u_m, "NOVA_AI: Generando reporte estrategico...")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='document.getElementById(\"modal\").style.display=\"block\"' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>VER EXPEDIENTE DE INVERSION</button>" 
    h += "<div id=\"modal\" style='display:none; position:fixed; top:2%; left:2%; width:96%; height:96%; background:#000; color:white; padding:40px; border:3px solid yellow; overflow-y:scroll; z-index:2000; font-size:14px;'>" 
    h += "<button onclick='this.parentElement.style.display=\"none\"' style='float:right; background:red; color:white; padding:15px; font-weight:bold;'>CERRAR [X]</button>" 
    h += "<h2 style=\"color:yellow; text-align:center;\">N.O.V.A. - DOSSIER MAESTRO PARA INVERSIONISTAS</h2><hr style='border:1px solid yellow;'>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:30px; margin-top:20px;'>" 
    h += "<div><h3 style='color:cyan;'>[1. GRAFICA DE PROYECCION FINANCIERA (ROI)]</h3>" 
    h += "<pre style='font-size:12px; line-height:1.2; background:#080808; padding:10px;'>ROI_18M:    ^\\nPROYECCION_RENTABILIDAD:    ^\\n(Millones USD)  |         _--*\\n   3.0 -        |      _-*\\n   2.0 -        |   _-*\\n   1.0 -        |_-*\\n   0.0 -  ______|___________>\\n          Start  12M    24M\\n>> Inversion Inicial: $1.2M USD.\\n>> ROI Estimado: 18 Meses.</pre>" 
    h += "<h3 style='color:cyan; margin-top:20px;'>[2. VIABILIDAD TECNICA]</h3><p>Optimizaci¢n energetica MPPT Solar, hardware ESP32 con Deep Sleep y sensores NDIR. Reduce insumos externos 85% y agua 90%. Ecosistema 100% robotizado.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[3. MECATRONICA VERTICAL (GREEN-CORE)]</h3>" 
    h += "<pre style='font-size:12px; line-height:1.2; background:#080808; padding:10px;'>      (Cosecha) -> [###]\\n      [###] <- (Dia 7: Final)\\n      [###]\\nRAIL  [###] <- (Dia 4: Crecimiento)\\nSYSTEM [###]\\n      [###]\\n      [###] <- (Dia 1: Siembra: Robot Alpha)</pre>" 
    h += "<p>Invernadero vertical automatizado. Rieles motorizados NEMA 23 desplazan bandejas optimizando espacio y gestionando fotoperiodo.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[4. SANIDAD ANIMAL Y BIOTECNOLOGIA]</h3><pre style='font-size:12px; line-height:1.2; background:#080808; padding:10px;'>     (Metabolismo Animal)\\n       |       \\n [Consumo FVH] -> [Cambio PH transpiracion]\\n       |              ^\\n       |         [Repelencia Garrapatas]\\n     (Output CO2) -> -40% (Metano)</pre>" 
    h += "<p>El FVH enriquecido actua como repelente sistemico natural, eliminando quimicos toxicos. Optimiza fermentacion ruminal reduciendo CO2 y metano 40%.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[5. FLUJO DE FINANCIACION (BONOS VERDES)]</h3><pre style='font-size:12px; line-height:1.2; background:#080808; padding:10px;'>    (Medicion NDIR) -> (Validacion Digital)\\n        |                    |\\n[Dato crudo CO2] -> [Certificado Bono Carbono] -> [Venta Mercado Int.]</pre>" 
    h += "<p>Cada tonelada capturada se registra en un ledger digital. Los Carbon Credits financian el 60% de los costos operativos, blindando la rentabilidad.</p></div></div>" 
    h += "<div style='background:#111; padding:20px; border:1px solid yellow; margin-top:30px;'><h3 style='color:yellow; text-align:center;'>SECRETO INDUSTRIAL DE SIEMBRA (STEP-BY-STEP)</h3>" 
    h += "<p style='text-align:center;'>1-Ozonado (O3) | 2-Nutricion Mineral y Organica | 3-Siembra Robot Alpha | 4-Germinacion Controlada | 5-Crecimiento LED Espectro Completo.</p></div></div>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - DASHBOARD CENTRAL DE MANDO]</h1>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:20px; border:2px solid #0f0; padding:20px; background:#050505;'>" 
    h += f"<p> >> TEMP_NODO_CENTRAL: {t:.1f}C</p><p> >> CO2_AMBIENTAL: {c:.2f} ppm</p>" 
    h += f"<p style='color:yellow;'> >> CAPTURA_FORRAJE (DIA 7): -{biomasa_fv * 12:.1f} ppm</p><p> >> BIOMASA_POR_BANDEJA: {biomasa_fv:.2f} kg</p>" 
    h += "</div><div style='display:flex; gap:20px; margin:20px 0;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>GREEN-CORE</h2><p>Forraje y Robotica</p></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>FIELD-LINK</h2><p>CO2 Potrero y LoRa</p></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px; background:#080808;'>" 
    h += "<h3 style='color:yellow;'>CHAT EXPERTO CENTRAL</h3>" 
    h += "<div style='height:150px; overflow-y:scroll;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><span style='color:yellow;'><b>N:</b> {{r}}</span></p><hr style='border:0.1px solid #222;'>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' style='flex-grow:1; padding:10px;'><button>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow; text-decoration:none;'><- VOLVER</a><h1>[GREEN-CORE: MODULO DE FORRAJE]</h1><p>Robot Alpha: Ejecutando siembra de precision...</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow; text-decoration:none;'><- VOLVER</a><h1>[FIELD-LINK: AUDITORIA EXTERIOR]</h1><p>Escaneando nodos LoRa en Deep Sleep...</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
