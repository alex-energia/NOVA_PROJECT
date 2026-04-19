import os 
from flask import Flask, render_template_string, request 
import random 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(22, 26), random.uniform(45, 52) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = f"Experto NOVA: Captura en {c:.1f} ppm. Hardware NDIR activo." 
        chat_history.append((u_m, res)) 
    html = """<html><body style='background:#000; color:#0f0; font-family:monospace; padding:30px;'><button onclick='alert("NOVA: 1.NDIR 2.LoRa 3.Diferencial")' style='position:fixed; top:20px; right:20px; background:yellow; padding:10px; font-weight:bold;'>INFO NOVA</button><h1 style='color:yellow;'>[N.O.V.A. MONITOR]</h1><div style='border:1px solid #444; padding:20px; background:#0a0a0a;'><p>TEMP: """ + f"{t:.1f}" + """C -- CO2: """ + f"{c:.2f}" + """ ppm</p></div><div style='margin-top:30px; border:1px solid #0f0; padding:15px;'><h3 style='color:cyan;'>CHAT EXPERTO</h3><div style='height:100px; overflow-y:scroll; background:#000;'>{% for u, r in history %}<p><b>U:</b> {{u}}<br><b>N:</b> {{r}}</p>{% endfor %}</div><form method='post'><input name='msg' style='width:70%;'><button>ENVIAR</button></form></div></body></html>""" 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
