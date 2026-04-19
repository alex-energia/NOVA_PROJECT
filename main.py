import os 
from flask import Flask, render_template_string, request 
import random, math 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(24.1, 26.3), random.uniform(415, 435) 
    biom = random.uniform(1.9, 2.7) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        chat_history.append((u_m, "NOVA_AI: Reporte de Ingenieria Generado.")) 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    h += "<button onclick='document.getElementById(\"modal\").style.display=\"block\"' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>EXPEDIENTE MAESTRO DE INVERSION</button>" 
    h += "<div id=\"modal\" style='display:none; position:fixed; top:2%; left:2%; width:96%; height:96%; background:#050505; color:white; padding:40px; border:3px solid yellow; overflow-y:scroll; z-index:2000; font-size:14px;'>" 
    h += "<button onclick='this.parentElement.style.display=\"none\"' style='float:right; background:red; color:white; padding:10px; border:none; cursor:pointer;'>CERRAR [X]</button>" 
    h += "<h1 style='color:yellow; text-align:center;'>N.O.V.A. - PROYECTO AGRO-TECNOLOGICO DISRUPTIVO</h1><hr style='border:1px solid #444;'>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:30px;'>" 
    h += "<div><h3 style='color:cyan;'>[1. VIABILIDAD Y RENTABILIDAD]</h3>" 
    h += "<p><b>Viabilidad:</b> El sistema opera con energia solar MPPT y sensores NDIR industriales. Reduce costos operativos en un 85 por ciento. <b>Rentabilidad:</b> ROI proyectado a 18 meses. El incremento del 20 por ciento en ganancia de peso animal y la venta de excedentes de biomasa aseguran un flujo de caja positivo desde el primer semestre.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[2. BIOTECNOLOGIA: REPELENTE NATURAL]</h3>" 
    h += "<p>El FVH producido por NOVA contiene extractos organicos integrados en el riego. Al ser consumido, altera el PH de la transpiracion del ganado. Resultado: Un repelente sistemico que elimina moscas y garrapatas de forma natural, suprimiendo el uso de quimicos toxicos e ivermectinas.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[3. AUDITORIA DE CO2 Y BONOS VERDES]</h3>" 
    h += "<p>El animal alimentado con NOVA tiene una digestion eficiente, reduciendo un 40 por ciento el gas metano. Nuestros nodos Field-Link certifican esta captura. Estos datos se convierten en Carbon Credits (Bonos Verdes) transables en mercados globales, cubriendo los gastos de mantenimiento.</p></div>" 
    h += "<div><h3 style='color:cyan;'>[4. INVERNADERO VERTICAL ROBOTIZADO]</h3>" 
    h += "<p>Dise¤o de 10 niveles optimizados. Rieles motorizados NEMA 23 desplazan las bandejas hacia modulos LED de espectro solar completo. El sistema es 100 por ciento autonomo, gestionado por inteligencia artificial para garantizar produccion constante los 365 dias del periodo anual.</p></div>" 
    h += "</div><h2 style='color:yellow; border-top:1px solid #444; margin-top:20px; padding-top:10px;'>[5. PROCESO DE SIEMBRA ROBOTICA PASO A PASO]</h2>" 
    h += "<p><b>Ingredientes:</b> Semilla tratada con O3, Solucion Mineral Kelp, Extracto de Neem. <br><b>Flujo:</b> 1. Desinfeccion Ozono | 2. Hidratacion Mineral | 3. Siembra Robot Alpha | 4. Germinacion Oscura | 5. Crecimiento Vertical.</p></div>" 
    h += "<h1 style='color:yellow;'> [N.O.V.A. - DASHBOARD OPERATIVO CENTRAL]</h1>" 
    h += "<div style='display:grid; grid-template-columns:1fr 1fr; gap:20px; border:2px solid #0f0; padding:20px; background:#050505;'>" 
    h += f"<div><p style='color:cyan;'>FIELD-LINK (POTREROS)</p><p> >> CO2 ACTUAL: {c:.2f} ppm</p><p> >> NODOS LORA: 5 ACTIVOS</p></div>" 
    h += f"<div><p style='color:cyan;'>GREEN-CORE (INVERNADERO)</p><p> >> BIOMASA: {biom:.2f} KG/B</p><p> >> TEMP: {t:.1f} C</p></div>" 
    h += "</div><div style='display:flex; gap:20px; margin:20px 0;'>" 
    h += "<a href='/invernadero' style='flex:1; padding:20px; border:2px solid #0f0; text-decoration:none; color:#0f0; text-align:center;'><h2>GREEN-CORE</h2></a>" 
    h += "<a href='/campo' style='flex:1; padding:20px; border:2px solid cyan; text-decoration:none; color:cyan; text-align:center;'><h2>FIELD-LINK</h2></a>" 
    h += "</div><div style='border:1px solid #444; padding:15px; background:#080808;'>" 
    h += "<h3>CHAT EXPERTO CENTRAL</h3>" 
    h += "<div style='height:120px; overflow-y:scroll;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><span style='color:yellow;'><b>N:</b> {{r}}</span></p>{% endfor %}</div>" 
    h += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0;'><button style='background:#0f0; color:#000; font-weight:bold;'>ENVIAR</button></form></div></body></html>" 
    return render_template_string(h, history=chat_history) 
@app.route('/invernadero') 
def invernadero(): 
    h = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[DETALLE GREEN-CORE]</h1><p>Control robotico de bandejas operativo.</p></body></html>" 
    return render_template_string(h) 
@app.route('/campo') 
def campo(): 
    h = "<html><body style='background:#000; color:cyan; font-family:monospace; padding:30px;'><a href='/' style='color:yellow;'><- VOLVER</a><h1>[DETALLE FIELD-LINK]</h1><p>Auditoria de carbono en tiempo real.</p></body></html>" 
    return render_template_string(h) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
