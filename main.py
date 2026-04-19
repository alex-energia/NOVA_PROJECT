import os 
from flask import Flask, render_template_string, request 
import random, math 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, h_rel = random.uniform(26, 29), random.uniform(65, 80) 
    fvh_crecimiento = random.uniform(1.2, 1.8) 
    co2_fvh = 400 - (fvh_crecimiento * 45) 
    hist = [int(random.uniform(40, 80)) for _ in range(10)] 
    b = " ".join([f"[#{'#' * (i // 10)}{'.' * (10 - i // 10)}]" for i in hist]) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = f"NOVA_AI: Analizando metabolismo FVH. Eficiencia fotosintetica: {fvh_crecimiento:.2f} mg/m2/s." 
        chat_history.append((u_m, res)) 
    html = "<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'>" 
    html += "<button onclick='alert(\"PROYECTO N.O.V.A. - EXPEDIENTE TECNICO MAESTRO\\n\\n1. EL FORRAJE (EL REY): Utilizacion de Zea mays y Hordeum vulgare en bandejas de alta densidad. El objetivo es maximizar el Area Foliar (LAI) para convertir el invernadero en un pulmon de captura negativa.\\n\\n2. DINAMICA DEL INVERNADERO: Control microclimatico automatizado. Sensores NDIR monitorean la caida de CO2 durante el fotoperiodo, validando la eficiencia del forraje como sumidero de carbono.\\n\\n3. BALANCE DE CARBONO: Se mide la diferencia entre el CO2 inyectado (o ambiental) vs el CO2 residual tras pasar por las camas de forraje. El objetivo es lograr una captura neta superior al 30% respecto al ciclo tradicional.\\n\\n4. ESCALABILIDAD: Modulos automatizados de riego por nebulizacion con agua enriquecida, optimizando la transpiracion y la fijacion de carbono en biomasa radicular.\")' style='position:fixed; top:20px; right:20px; background:yellow; color:black; padding:15px; border:4px solid #fff; font-weight:bold; cursor:pointer; z-index:1000;'>DOCUMENTACION MAESTRA</button>" 
    html += "<h1 style='color:yellow;'> [N.O.V.A. - CONTROL DE INVERNADERO FVH]</h1>" 
    html += "<div style='display:grid; grid-template-columns: 1fr 1fr; gap:20px;'>" 
    html += "<div style='border:2px solid #0f0; padding:20px; background:#050505;'>" 
    html += "<p style='color:cyan; border-bottom:1px solid #0f0;'>[METRICAS DEL INVERNADERO]</p>" 
    html += f"<p> >> TEMP_INTERNA: {t:.1f}C</p><p> >> HUMEDAD_RELATIVA: {h_rel:.1f}%</p>" 
    html += f"<p style='color:yellow;'> >> CO2_POST_FORRAJE: {co2_fvh:.2f} ppm</p>" 
    html += f"<p> >> TASA_CRECIMIENTO: {fvh_crecimiento:.2f} cm/dia</p></div>" 
    html += "<div style='border:2px solid #0f0; padding:20px; background:#050505;'>" 
    html += "<p style='color:cyan; border-bottom:1px solid #0f0;'>[HISTORIAL DE CAPTURA BIOMASA]</p>" 
    html += f"<p style='letter-spacing:2px; color:cyan;'> {b} </p><p><small> T-10h . . . . . . . . . T-1h </small></p></div></div>" 
    html += "<div style='margin-top:20px; border:1px solid #444; padding:15px;'>" 
    html += "<h3 style='color:yellow;'> CHAT EXPERTO EN FORRAJE</h3>" 
    html += "<div style='height:120px; overflow-y:scroll; background:#000; padding:10px;'>" 
    html += "{% for u, r in history %}<p style='color:white;'><b>U:</b> {{u}}<br><span style='color:#0f0;'><b>N:</b> {{r}}</span></p><hr style='border:0.1px solid #222;'>{% endfor %}</div>" 
    html += "<form method='post' style='display:flex; gap:10px; margin-top:10px;'><input name='msg' placeholder='Consultar sobre metabolismo FVH...' style='flex-grow:1; background:#000; color:#0f0; border:1px solid #0f0; padding:10px;'><button style='background:#0f0; color:#000; border:none; padding:10px 20px; font-weight:bold;'>EJECUTAR</button></form></div>" 
    html += "<p style='color:#444; font-size:12px;'> FVH_MODULE: ACTIVE | SENSOR_NDIR: CALIBRATED | PUMP_STATUS: STANDBY </p></body></html>" 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
