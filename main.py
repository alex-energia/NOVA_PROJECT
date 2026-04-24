import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-500K-v34-{random.randint(100,999)}"
        # SCADA (10 Variables)
        self.inv = {"ph":0,"ce":0,"vpd":0,"co2":0,"par":0,"temp":0,"hum":0,"agua":0,"dli":0,"aire":0}
        # LA JOYA (8 Variables)
        self.pot = {"co2_cap":0,"co2_s":0,"ch4":0,"ndvi":0,"viento":0,"presion":0,"hum_f":0,"rad":0}
        self.h = 0; self.pb = 0; self.pt = 0; self.mezcla = "---"

    def update(self):
        if self.standby:
            self.standby = False
            self.inv.update({"ph":5.8,"ce":1.4,"vpd":1.1,"co2":450,"par":850,"temp":24,"hum":65,"agua":100,"dli":22,"aire":1100})
            self.pot.update({"co2_s":840,"ch4":0.02,"ndvi":0.65,"viento":12,"presion":1012,"hum_f":45,"rad":610})
            self.mezcla = "Maíz (400kg) + Cebada (75kg) + Avena (25kg)"
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.5, 1)
            self.pb = round(2 + (self.dia * 1.5), 1)
            self.pt = round(75 + (self.dia * 60), 1)
            self.pot["co2_cap"] = round(self.dia * 4.3, 2)
        else: self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V34, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V34, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

# --- INTERFAZ TOTAL ---
HTML_V34 = """
<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono'; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,20,20,0.9); border: 2px solid #00ffcc; padding: 15px; z-index: 100; width: 400px; }
    #left { top: 10px; left: 10px; }
    #right { top: 10px; right: 10px; border-right: 4px solid #ffd700; }
    .title { font-weight: 700; font-size: 14px; border-bottom: 2px solid #00ffcc; margin-bottom: 10px; padding-bottom: 5px; }
    .row { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 5px; }
    .val { color: #fff; }
    .joya { color: #ffd700; }
    button { background: #00ffcc; border: none; padding: 10px; cursor: pointer; font-weight: 900; width: 100%; margin-top: 5px; }
    #main-btn { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); width: 300px; font-size: 18px; border-radius: 50px; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head><body>

<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO 500KG</div>
    <div class="row"><span>DÍA:</span> <span class="val">{{ d }}</span></div>
    <div class="row"><span>MEZCLA:</span> <span class="val">{{ mez }}</span></div>
    <div class="row"><span>ALTURA:</span> <span class="val">{{ h }} CM</span></div>
    <div class="row"><span>PESO BAND:</span> <span class="val">{{ pb }} KG</span></div>
    <div class="row"><span>PROD TOTAL:</span> <span class="val">{{ pt }} / 500 KG</span></div>
    <div class="row"><span>PH / CE:</span> <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
    <div class="row"><span>VPD / CO2:</span> <span class="val">{{ inv.vpd }} / {{ inv.co2 }}</span></div>
    <div class="row"><span>TEMP / HUM:</span> <span class="val">{{ inv.temp }} / {{ inv.hum }}</span></div>
    <div class="row"><span>PAR / DLI:</span> <span class="val">{{ inv.par }} / {{ inv.dli }}</span></div>
    <div class="row"><span>AGUA / AIRE:</span> <span class="val">{{ inv.agua }} / {{ inv.aire }}</span></div>
    <button onclick="alert('Gráficas SCADA')">📈 VER GRÁFICAS</button>
</div>

<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: POTRERO</div>
    <div class="row"><span>CAPTURA CO2:</span> <span class="joya">{{ pot.co2_cap }} KG</span></div>
    <div class="row"><span>CO2 SUELO:</span> <span class="val">{{ pot.co2_s }}</span></div>
    <div class="row"><span>METANO:</span> <span class="val">{{ pot.ch4 }}</span></div>
    <div class="row"><span>NDVI:</span> <span class="val">{{ pot.ndvi }}</span></div>
    <div class="row"><span>VIENTO:</span> <span class="val">{{ pot.viento }}</span></div>
    <div class="row"><span>PRESION:</span> <span class="val">{{ pot.presion }}</span></div>
    <div class="row"><span>HUM FOLIAR:</span> <span class="val">{{ pot.hum_f }}</span></div>
    <div class="row"><span>RAD GLOBAL:</span> <span class="val">{{ pot.rad }}</span></div>
    <button onclick="alert('Gráficas Carbono')" style="background:#ffd700">📈 ANALÍTICA CARBONO</button>
</div>

<button id="main-btn" onclick="location.href='/next'">{{ "INICIAR" if standby else "AVANZAR DÍA" }}</button>

<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// DOMO (Visible sin luces)
const dome = new THREE.Mesh(
    new THREE.SphereGeometry(40, 32, 16, 0, Math.PI*2, 0, Math.PI/2),
    new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true})
);
scene.add(dome);

// BANDA TRANSPORTADORA
const belt = new THREE.Mesh(new THREE.BoxGeometry(100, 1, 15), new THREE.MeshBasicMaterial({color: 0x222222}));
belt.position.y = -5; scene.add(belt);

// BANDEJA
const tray = new THREE.Group();
const trayBase = new THREE.Mesh(new THREE.BoxGeometry(15, 1, 10), new THREE.MeshBasicMaterial({color: 0x555555}));
tray.add(trayBase);

// MAÍZ / FORRAJE
if ({{ d }} == 0) {
    for(let i=0; i<50; i++) {
        const m = new THREE.Mesh(new THREE.SphereGeometry(0.3), new THREE.MeshBasicMaterial({color: 0xffcc00}));
        m.position.set((Math.random()-0.5)*13, 0.6, (Math.random()-0.5)*8);
        tray.add(m);
    }
} else {
    const h = ({{ d }} * 1.5) + 1;
    const f = new THREE.Mesh(new THREE.BoxGeometry(14, h, 9), new THREE.MeshBasicMaterial({color: ({{d}}<4?0xccff00:0x00ff00)}));
    f.position.y = h/2; tray.add(f);
}
if (!{{ standby|lower }}) scene.add(tray);

// ANIMAL
const animal = new THREE.Mesh(new THREE.BoxGeometry(8,6,4), new THREE.MeshBasicMaterial({color: 0x4d2600}));
animal.position.set(80, -2, 0); scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    if ({{ standby|lower }}) {
        camera.position.set(100*Math.sin(t*0.2), 50, 100*Math.cos(t*0.2));
        camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        camera.position.lerp(new THREE.Vector3(30, 20, 30), 0.05);
        camera.lookAt(0,0,0);
    } else {
        if(tray.position.x < 75) tray.position.x += 0.5;
        camera.position.lerp(new THREE.Vector3(120, 40, 50), 0.05);
        camera.lookAt(animal.position);
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)