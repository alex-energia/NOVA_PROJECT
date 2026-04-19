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
        user_msg = request.form.get('msg') 
        resp = f"Como experto en NOVA, confirmo procesamiento de {c:.1f} ppm de carbono. El hardware NDIR esta listo. Deseas analizar mas?" 
        chat_history.append((user_msg, resp)) 
    return render_template_string(html, history=chat_history) 
if __name__ == "__main__": 
    port = int(os.environ.get("PORT", 10000)) 
    app.run(host="0.0.0.0", port=port) 
