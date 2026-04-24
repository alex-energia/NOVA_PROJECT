import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-500K-v33-{random.randint(100,999)}"
        # PANEL SCADA (10 VARIABLES)
        self.inv = {
            "ph": 0.0, "ce": 0.0, "vpd": 0.0, "co2": 0, "par": 0, 
            "temp": 0.0, "hum": 0, "agua": 0, "dli": 0.0, "aire": 0
        }
        # PANEL LA JOYA (8 VARIABLES)
        self.pot = {
            "co2_cap": 0.0, "co2_s": 0, "ch4": 0.0, "ndvi": 0.0, 
            "viento": 0.0, "presion": 0, "hum_f": 0, "rad": 0
        }
        self.h = 0.0
        self.pb = 0.0 # Peso Bandeja
        self.pt = 0.0 # Peso Total Lote
        self.mezcla = "---"

    def update(self):
        if self.standby:
            self.standby = False
            self.dia = 0
            self.inv.update({"ph": 5.8, "ce": 1.4, "vpd": 1.1, "co2": 450, "par": 850, "temp": 24.0, "hum": 65, "agua": 100, "dli": 22.1, "aire": 1100})
            self.pot.update({"co2_s": 840, "ch4": 0.02, "ndvi": 0.65, "viento": 12.5, "presion": 1012, "hum_f": 45, "rad": 610})
            self.mezcla = "Maíz (400kg) + Cebada (75kg) + Avena (25kg)"
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.4, 1)
            self.pb = round(2.0 + (self.dia * 1.6), 1)
            self.pt = round(75 + (self.dia * 60.5), 1)
            self.pot["co2_cap"] = round(self.dia * 4.35, 2)
            self.pot["ndvi"] = min(0.98, 0.65 + (self.dia * 0.04))
            self.inv["agua"] += 215
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V33, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V33, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

# --- INTERFAZ AVANZADA ---
P1 = """
<!DOCTYPE html><html><head><title>NOVA v33 | 500KG Full Control</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono'; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,15,15,0.95); border: 2px solid #00ffcc; padding: 15px; z-index: 100; box-shadow: 0 0 15px #004444; }
    #left { top: 10px; left: 10px; width: 420px; border-left: 5px solid #00ffcc; }
    #right { top: 10px; right: 10px; width: 400px; border-right: 5px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; margin-bottom: 10px; color: #fff; text-transform: uppercase; border-bottom: 1px solid #00ffcc; }
    .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; border-bottom: 1px solid rgba(0,255,204,0.1); }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    .btn-g { background: transparent; border: 1px solid #00ffcc; color: #00ffcc; font-size: 10px; cursor: pointer; padding: 5px; width: 100%; margin-top: 5px; }
    .btn-g:hover { background: #00ffcc; color: #000; }
    #controls { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 200; }
    button#main { background: #00ffcc; border: none; padding: 15px 40px; font-weight: 900; cursor: pointer; border-radius: 5px; box-shadow: 0 0 15px #00ffcc; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

P2 = """
<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO - {{ bid }}</div>
    <div class="data">DÍA: <span class="val">{{ d }}</span> | MEZCLA: <span class="val">{{ mez }}</span></div>
    <div class="data">ALTURA: <span class="val">{{ h }} CM</span> | PESO BAND: <span class="val">{{ pb }} KG</span></div>
    <div class="data">PROD. TOTAL: <span class="val">{{ pt }} / 500 KG</span></div>
    <div class="data">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
    <div class="data">VPD / CO2: <span class="val">{{ inv.vpd }} / {{ inv.co2 }} PPM</span></div>
    <div class="data">TEMP / HUM: <span class="val">{{ inv.temp }}°C / {{ inv.hum }}%</span></div>
    <div class="data">PAR / DLI: <span class="val">{{ inv.par }} / {{ inv.dli }}</span></div>
    <div class="data">AGUA / AIRE: <span class="val">{{ inv.agua }} L / {{ inv.aire }} m3</span></div>
    <button class="btn-g" onclick="alert('Historial SCADA 500kg cargando...')">📈 VER GRÁFICAS DE CONTROL</button>
</div>

<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: MÉTRICAS POTRERO</div>
    <div class="data">CAPTURA CO2: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">CO2 SUELO: <span class="val">{{ pot.co2_s }} PPM</span></div>
    <div class="data">METANO (CH4): <span class="val">{{ pot.ch4 }} mg</span></div>
    <div class="data">NDVI / RAD: <span class="val">{{ pot.ndvi }} / {{ pot.rad }}</span></div>
    <div class="data">VIENTO / PRES: <span class="val">{{ pot.viento }} km/h / {{ pot.presion }}</span></div>
    <div class="data">HUM. FOLIAR: <span class="val">{{ pot.hum_f }}%</span></div>
    <button class="btn-g" style="border-color:#ffd700; color:#ffd700;" onclick="alert('Analítica de Carbono cargando...')">📈 ANALÍTICA DE CARBONO</button>
</div>

<div id="controls"><button id="main" onclick="location.href='/next'">{{ "INICIAR CICLO 500K" if standby else "AVANZAR DÍA" }}</button></div>
"""

P3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 2000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// ILUMINACIÓN INDUSTRIAL
const ambient = new THREE.AmbientLight(0xffffff, 0.8); scene.add(ambient);
const spot = new THREE.PointLight(0xffffff, 1); scene.add(spot);

// --- EL BIO-DOMO (VISIBLE) ---
const dome = new THREE.Mesh(
    new THREE.SphereGeometry(40, 32, 20, 0, Math.PI*2, 0, Math.PI/2),
    new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.5})
);
scene.add(dome);

// --- BANDEJA Y BANDA ---
const belt = new THREE.Mesh(new THREE.BoxGeometry(100, 0.5, 15), new THREE.MeshBasicMaterial({color: 0x222222}));
belt.position.set(40, -1, 0); scene.add(belt);

const tray = new THREE.Group();
const trayBase = new THREE.Mesh(new THREE.BoxGeometry(15, 0.8, 10), new THREE.MeshBasicMaterial({color: 0x111111}));
tray.add(trayBase);

// BIOMASA: SEMILLA O FORRAJE
let bio;
if ({{ d }} == 0) {
    const geo = new THREE.BufferGeometry();
    const pos = [];
    for(let i=0; i<1000; i++) pos.push((Math.random()-0.5)*14, 0.5, (Math.random()-0.5)*9);
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    bio = new THREE.Points(geo, new THREE.PointsMaterial({color: 0xffcc00, size: 0.15}));
} else {
    const h = ({{ d }} * 1.5) + 0.5;
    bio = new THREE.Mesh(new THREE.BoxGeometry(14, h, 9), new THREE.MeshBasicMaterial({color: ({{d}}<4?0xccff00:0x00ff44)}));
    bio.position.y = h/2;
}
tray.add(bio);
if (!{{ standby|lower }}) scene.add(tray);

// ANIMAL
const animal = new THREE.Mesh(new THREE.CapsuleGeometry(3, 5, 8, 16), new THREE.MeshBasicMaterial({color: 0x4d2600}));
animal.position.set(90, 3, 0); animal.rotation.z = Math.PI/2;
scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    spot.position.copy(camera.position);

    if ({{ standby|lower }}) {
        camera.position.set(120*Math.sin(t*0.2), 60, 120*Math.cos(t*0.2));
        camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        camera.position.lerp(new THREE.Vector3(30, 20, 30), 0.05);
        camera.lookAt(0, 0, 0);
    } else {
        if(tray.position.x < 85) tray.position.x += 0.3;
        camera.position.lerp(new THREE.Vector3(120, 40, 50), 0.03);
        camera.lookAt(animal.position);
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_V33 = P1 + P2 + P3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)