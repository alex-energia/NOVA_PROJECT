import os 
from flask import Flask, render_template_string, request 
import random 
app = Flask(__name__) 
chat_history = [] 
@app.route('/', methods=['GET', 'POST']) 
def home(): 
    global chat_history 
    t, c = random.uniform(22, 26), random.uniform(45, 52) 
    h = [random.randint(30, 60) for _ in range(5)] 
    b = " ".join([f"[#{'#' * (i // 10)}{'.' * (6 - i // 10)}]" for i in h]) 
    if request.method == 'POST': 
        u_m = request.form.get('msg') 
        res = f"Experto NOVA: Captura en {c:.1f} ppm. Hardware NDIR activo." 
        chat_history.append((u_m, res)) 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
