import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-D30-{random.randint(1000,9999)}"
        self.inv = {
            "ph": 0.0, "ce": 0.0, "vpd": 0.0, "co2": 0.0, 
            "par": 0, "o2": 0.0, "temp": 0.0, "dli": 0.0
        }
        self.pot = {
            "co2_cap": 0.0, "co2_s": 0, "ch4": 0.0, 
            "h10": 0, "rad": 0, "ndvi": 0.0, "viento": 0.0
        }
        self.h = 0.0
        self.p = 0.0
        self.mezcla = "---"

    def update(self):
        if self.standby:
            self.standby = False
            self.dia = 0
            self.inv.update({"ph": 5.8, "ce": 1.4, "vpd": 1.1, "co2": 450, "par": 850, "o2": 8.2, "temp": 24.1, "dli": 22.5})
            self.pot.update({"co2_s": 840, "h10": 24, "rad": 610, "ndvi": 0.68, "viento": 12.5})
            self.mezcla = "Maíz 80% + Cebada 15% + Avena 5%"
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.5, 1)
            self.p = round(12.0 + (self.dia * 11.2), 1)
            self.pot["co2_cap"] = round(self.dia * 6.35, 2)
            self.pot["ndvi"] = min(0.98, 0.68 + (self.dia * 0.04))
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V30, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p, standby=ctrl.standby)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V30, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p, standby=ctrl.standby)

# Secciones de código para evitar errores de Render
H1 = """
<!DOCTYPE html><html><head><title>NOVA v30 | Bio-Dome SCADA</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono', monospace; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,15,15,0.92); border: 2px solid #00ffcc; padding: 15px; z-index: 100; border-radius: 8px; }
    #left { top: 20px; left: 20px; width: 420px; }
    #right { top: 20px; right: 20px; width: 400px; border-right: 4px solid #ffd700; }
    .title { font-weight: 700; font-size: 14px; margin-bottom: 12px; color: #fff; text-transform: uppercase; border-bottom: 2px solid #00ffcc; }
    .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px; }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    .btn-chart { background: transparent; border: 1px solid #00ffcc; color: #00ffcc; font-size: 9px; cursor: pointer; padding: 2px 8px; margin-top: 5px; }
    .btn-chart:hover { background: #00ffcc; color: #000; }
    #controls { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 200; }
    button#main-btn { background: #00ffcc; color: #000; border: none; padding: 20px 60px; font-weight: 900; cursor: pointer; font-size: 16px; border-radius: 50px; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

H2 = """
<div id="left" class="hud">
    <div class="title">INVERNADERO DIGITAL TWIN</div>
    <div class="data">DÍA: <span class="val">{{ d }}</span></div>
    <div class="data">ALTURA: <span class="val">{{ h }} CM</span></div>
    <div class="data">PESO: <span class="val">{{ p }} KG</span></div>
    <div class="data">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
    <div class="data">VPD / CO2: <span class="val">{{ inv.vpd }} / {{ inv.co2 }} PPM</span></div>
    <div class="data">O2 / DLI: <span class="val">{{ inv.o2 }} / {{ inv.dli }}</span></div>
    <div class="data">MEZCLA: <span class="val">{{ mez }}</span></div>
    <button class="btn-chart" onclick="alert('Cargando Historial SCADA...')">📈 VER GRÁFICAS DE CONTROL</button>
</div>
<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: MÉTRICAS DE IMPACTO</div>
    <div class="data">CAPTURA CO2: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">CH4 (METANO): <span class="val">{{ pot.ch4 }} mg</span></div>
    <div class="data">CO2 SUELO: <span class="val">{{ pot.co2_s }} PPM</span></div>
    <div class="data">NDVI / RAD: <span class="val">{{ pot.ndvi }} / {{ pot.rad }}</span></div>
    <div class="data">HUM. 10CM: <span class="val">{{ pot.h10 }}%</span></div>
    <div class="data">VIENTO: <span class="val">{{ pot.viento }} km/h</span></div>
    <button class="btn-chart" onclick="alert('Cargando Historial Carbono...')">📈 VER GRÁFICAS DE CARBONO</button>
</div>
<div id="controls"><button id="main-btn" onclick="location.href='/next'">{{ "INICIAR SISTEMA" if standby else ("COSECHAR" if d==7 else "AVANZAR DÍA") }}</button></div>
"""

H3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 5000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// --- ESTRUCTURA DOMO GEODÉSICO ---
const domeGroup = new THREE.Group();
const domeGeo = new THREE.IcosahedronGeometry(30, 2); // Estructura de domo
const domeMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.3});
const dome = new THREE.Mesh(domeGeo, domeMat);
dome.position.y = -5;
domeGroup.add(dome);

// Bandeja de Crecimiento (Base del domo)
const tray = new THREE.Mesh(new THREE.CylinderGeometry(20, 20, 1, 32), new THREE.MeshBasicMaterial({color: 0x111111}));
tray.position.y = -6;
domeGroup.add(tray);

// Biomasa
const bioH = ({{ d }} * 1.5) + 0.5;
let bioColor = 0x5c4033;
if ({{ d }} > 0 && {{ d }} < 3) bioColor = 0xbfff00;
if ({{ d }} >= 3) bioColor = 0x00ff44;

const biomasa = new THREE.Mesh(new THREE.CylinderGeometry(18, 18, bioH, 32), new THREE.MeshBasicMaterial({color: bioColor}));
biomasa.position.y = -6 + bioH/2;
if ({{ standby }} == true) biomasa.visible = false;
domeGroup.add(biomasa);

scene.add(domeGroup);

// Elementos Externos
const animal = new THREE.Mesh(new THREE.BoxGeometry(8,5,3), new THREE.MeshBasicMaterial({color: 0x442200}));
animal.position.set(100, -5, 0); scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    
    if ({{ standby }} == true) {
        camera.position.set(120 * Math.sin(t*0.2), 60, 120 * Math.cos(t*0.2));
        camera.lookAt(0,0,0);
    } else {
        // Zoom al interior del domo
        camera.position.lerp(new THREE.Vector3(45, 10, 45), 0.05);
        camera.lookAt(0, 0, 0);
        dome.rotation.y += 0.002;
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_V30 = H1 + H2 + H3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)