import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-500K-{random.randint(100,999)}"
        # SCADA Completo (Meta 500kg)
        self.inv = {
            "ph": 0.0, "ce": 0.0, "vpd": 0.0, "co2": 450, 
            "par": 0, "o2": 0.0, "temp": 0.0, "agua": 0
        }
        # La Joya (Variables Recuperadas y Expandidas)
        self.pot = {
            "co2_cap": 0.0, "co2_s": 850, "ch4": 0.0, "h10": 24, 
            "rad": 620, "ndvi": 0.65, "viento": 12, "presion": 1012
        }
        self.h = 0.0
        self.p_bandeja = 0.0 # Peso de una sola bandeja
        self.p_total = 0.0   # Peso total del lote (Meta 500kg)
        self.mezcla = "Maíz 400kg + Cebada 75kg + Avena 25kg"

    def update(self):
        if self.standby:
            self.standby = False
            self.dia = 0
            self.inv.update({"ph": 5.8, "ce": 1.4, "temp": 24.2})
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.5, 1)
            self.p_bandeja = round(2.0 + (self.dia * 1.5), 1) 
            self.p_total = round(75 + (self.dia * 60.7), 1) # Proyección a 500kg
            self.pot["co2_cap"] = round(self.dia * 4.2, 2)
            self.inv["agua"] += 225
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V32, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.p_bandeja, pt=ctrl.p_total, standby=ctrl.standby)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V32, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.p_bandeja, pt=ctrl.p_total, standby=ctrl.standby)

# Estructura de Interfaz y Gráficos
P1 = """
<!DOCTYPE html><html><head><title>NOVA v32 | 500KG Unit</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono'; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,20,20,0.9); border: 1px solid #00ffcc; padding: 15px; z-index: 100; border-radius: 4px; }
    #left { top: 10px; left: 10px; width: 400px; }
    #right { top: 10px; right: 10px; width: 380px; border-right: 4px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; margin-bottom: 8px; color: #fff; text-transform: uppercase; border-bottom: 1px solid #333; }
    .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    #chart-panel { display:none; position:fixed; top:15%; left:15%; width:70%; height:70%; background:#050505; border:2px solid #00ffcc; z-index:500; padding:20px; }
    .bar { height: 15px; background: #00ffcc; margin: 10px 0; transition: 1s; }
    #controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 200; }
    button { background: #00ffcc; border: none; padding: 12px 30px; font-weight: 900; cursor: pointer; font-family: 'Roboto Mono'; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

P2 = """
<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO - {{ bid }}</div>
    <div class="data">DÍA: <span class="val">{{ d }}</span> | ALTURA: <span class="val">{{ h }} CM</span></div>
    <div class="data">PESO BANDEJA: <span class="val">{{ pb }} KG</span></div>
    <div class="data">PROD. TOTAL LOTE: <span class="val">{{ pt }} / 500 KG</span></div>
    <div class="data">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
    <div class="data">CO2 / VPD: <span class="val">{{ inv.co2 }} / {{ inv.vpd }}</span></div>
    <button onclick="document.getElementById('chart-panel').style.display='block'" style="width:100%; margin-top:5px;">📈 VER GRÁFICAS 500K</button>
</div>

<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: IMPACTO ECO</div>
    <div class="data">CO2 CAPTURADO: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">CO2 SUELO: <span class="val">{{ pot.co2_s }} PPM</span></div>
    <div class="data">METANO: <span class="val">{{ pot.ch4 }}</span> | NDVI: <span class="val">{{ pot.ndvi }}</span></div>
    <div class="data">HUM. 10CM: <span class="val">{{ pot.h10 }}%</span> | RAD: <span class="val">{{ pot.rad }}</span></div>
</div>

<div id="chart-panel">
    <h3 style="color:#00ffcc">ANALÍTICA DE PRODUCCIÓN</h3>
    <p>Eficiencia de Crecimiento (Día {{d}}):</p>
    <div class="bar" style="width: {{ (pt/500)*100 }}%"></div>
    <p>Captura de Carbono Relativa:</p>
    <div class="bar" style="width: {{ (pot.co2_cap/30)*100 }}%; background:#ffd700;"></div>
    <button onclick="this.parentElement.style.display='none'">CERRAR</button>
</div>

<div id="controls"><button onclick="location.href='/next'">{{ "AVANZAR" if not standby else "INICIAR 500K" }}</button></div>
"""

P3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const light = new THREE.PointLight(0xffffff, 1, 500);
scene.add(light);
scene.add(new THREE.AmbientLight(0x404040, 2));

const dome = new THREE.Mesh(
    new THREE.SphereGeometry(30, 32, 16, 0, Math.PI*2, 0, Math.PI/2),
    new THREE.MeshStandardMaterial({color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.2})
);
scene.add(dome);

// --- BANDEJA RECTANGULAR ---
const trayGroup = new THREE.Group();
const trayBase = new THREE.Mesh(new THREE.BoxGeometry(12, 0.5, 8), new THREE.MeshStandardMaterial({color: 0x111111}));
trayGroup.add(trayBase);

// MAÍZ (GRANOS DÍA 0 / FORRAJE DÍA 7)
let bio;
if ({{ d }} == 0) {
    const geo = new THREE.BufferGeometry();
    const pos = [];
    for(let i=0; i<500; i++) pos.push((Math.random()-0.5)*11, 0.5, (Math.random()-0.5)*7);
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    bio = new THREE.Points(geo, new THREE.PointsMaterial({color: 0xffaa00, size: 0.2}));
} else {
    const h = ({{ d }} * 1.2);
    bio = new THREE.Mesh(new THREE.BoxGeometry(11.5, h, 7.5), new THREE.MeshStandardMaterial({color: ({{d}}<3?0xccff00:0x00ff44)}));
    bio.position.y = h/2;
}
trayGroup.add(bio);
scene.add(trayGroup);

// Banda Transportadora y Animal
const belt = new THREE.Mesh(new THREE.BoxGeometry(60, 0.2, 10), new THREE.MeshStandardMaterial({color: 0x222222}));
belt.position.set(30, -0.5, 0); scene.add(belt);

const animal = new THREE.Mesh(new THREE.CapsuleGeometry(2, 4, 4, 8), new THREE.MeshStandardMaterial({color: 0x442200}));
animal.position.set(60, 2, 0); animal.rotation.z = Math.PI/2;
scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    light.position.copy(camera.position);

    if ({{ standby|lower }}) {
        camera.position.set(70*Math.sin(t*0.2), 30, 70*Math.cos(t*0.2));
        camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        camera.position.lerp(new THREE.Vector3(15, 12, 15), 0.05);
        camera.lookAt(0, 0, 0);
    } else {
        // MOVIMIENTO HACIA EL ANIMAL
        if(trayGroup.position.x < 55) trayGroup.position.x += 0.2;
        camera.position.lerp(new THREE.Vector3(80, 20, 30), 0.03);
        camera.lookAt(animal.position);
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_V32 = P1 + P2 + P3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)