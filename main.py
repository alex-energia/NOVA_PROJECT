import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-500K-v36-{random.randint(100,999)}"
        # SCADA INVERNADERO (10 Variables)
        self.inv = {"ph":0,"ce":0,"vpd":0,"co2":0,"par":0,"temp":0,"hum":0,"agua":0,"dli":0,"aire":0}
        # LA JOYA (8 Variables Completas)
        self.pot = {"co2_cap":0,"co2_s":0,"ch4":0,"ndvi":0,"viento":0,"presion":0,"hum_f":0,"rad":0}
        self.h = 0; self.pb = 0; self.pt = 0; self.mezcla = "---"

    def update(self):
        if self.standby:
            self.standby = False
            self.inv.update({"ph":5.8,"ce":1.4,"vpd":1.1,"co2":450,"par":850,"temp":24.2,"hum":65,"agua":100,"dli":22,"aire":1100})
            self.pot.update({"co2_s":840,"ch4":0.02,"ndvi":0.65,"viento":12.5,"presion":1012,"hum_f":45,"rad":610})
            self.mezcla = "Maíz (400kg) + Cebada (75kg) + Avena (25kg)"
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.4, 1)
            self.pb = round(2.5 + (self.dia * 1.8), 1)
            self.pt = round(80 + (self.dia * 60), 1)
            self.pot["co2_cap"] = round(self.dia * 4.6, 2)
            self.pot["ndvi"] = min(0.98, 0.65 + (self.dia * 0.04))
        else: self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V36, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V36, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

HTML_V36 = """
<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono'; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,20,20,0.95); border: 2px solid #00ffcc; padding: 15px; z-index: 100; width: 420px; box-shadow: 0 0 20px #004444; }
    #left { top: 10px; left: 10px; border-left: 5px solid #00ffcc; }
    #right { top: 10px; right: 10px; border-right: 5px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; border-bottom: 2px solid #00ffcc; margin-bottom: 8px; color: #fff; text-transform: uppercase; }
    .row { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; border-bottom: 1px solid rgba(0,255,204,0.1); }
    .val { color: #fff; }
    .joya { color: #ffd700; }
    
    /* DASHBOARD */
    #chart-panel { display:none; position:fixed; top:10%; left:10%; width:80%; height:80%; background:#050505; border:3px solid #00ffcc; z-index:500; padding:30px; }
    .bar-bg { width: 100%; background: #222; height: 25px; margin: 15px 0; border: 1px solid #444; }
    .bar-fill { height: 100%; background: #00ffcc; transition: 1s ease-out; }
    
    button { background: #00ffcc; border: none; padding: 12px; cursor: pointer; font-weight: 900; width: 100%; margin-top: 10px; }
    #main-btn { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); width: 300px; font-size: 18px; border-radius: 5px; box-shadow: 0 0 30px #00ffcc; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head><body>

<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO (500KG/D)</div>
    <div class="row"><span>DÍA / LOTE:</span> <span class="val">{{ d }} / {{ bid }}</span></div>
    <div class="row"><span>MEZCLA BASE:</span> <span class="val">{{ mez }}</span></div>
    <div class="row"><span>ALTURA / PESO BAND:</span> <span class="val">{{ h }}cm / {{ pb }}kg</span></div>
    <div class="row"><span>PROD TOTAL:</span> <span class="val">{{ pt }} / 500 KG</span></div>
    <div class="row"><span>PH / CE:</span> <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
    <div class="row"><span>VPD / CO2:</span> <span class="val">{{ inv.vpd }} / {{ inv.co2 }} PPM</span></div>
    <div class="row"><span>TEMP / HUM:</span> <span class="val">{{ inv.temp }} / {{ inv.hum }}</span></div>
    <div class="row"><span>PAR / DLI:</span> <span class="val">{{ inv.par }} / {{ inv.dli }}</span></div>
    <div class="row"><span>AGUA / AIRE:</span> <span class="val">{{ inv.agua }} / {{ inv.aire }}</span></div>
    <button onclick="document.getElementById('chart-panel').style.display='block'">📈 VER ANALÍTICA OPERATIVA</button>
</div>

<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: MÉTRICAS POTRERO</div>
    <div class="row"><span>CAPTURA CO2:</span> <span class="joya">{{ pot.co2_cap }} KG</span></div>
    <div class="row"><span>CO2 SUELO:</span> <span class="val">{{ pot.co2_s }}</span> | <span>CH4:</span> <span class="val">{{ pot.ch4 }}</span></div>
    <div class="row"><span>NDVI:</span> <span class="val">{{ pot.ndvi }}</span> | <span>RAD:</span> <span class="val">{{ pot.rad }}</span></div>
    <div class="row"><span>VIENTO / PRESION:</span> <span class="val">{{ pot.viento }} / {{ pot.presion }}</span></div>
    <div class="row"><span>HUM FOLIAR:</span> <span class="val">{{ pot.hum_f }}%</span></div>
    <button onclick="document.getElementById('chart-panel').style.display='block'" style="background:#ffd700">📈 ANALÍTICA CARBONO</button>
</div>

<div id="chart-panel">
    <h2 style="color:#00ffcc">SISTEMA DE CONTROL NOVA v36</h2>
    <p>RENDIMIENTO DE BIOMASA (Meta 500kg):</p>
    <div class="bar-bg"><div class="bar-fill" style="width:{{(pt/500)*100}}%"></div></div>
    <p>IMPACTO CARBONO (Captura Acumulada):</p>
    <div class="bar-bg"><div class="bar-fill" style="width:{{(pot.co2_cap/40)*100}}%; background:#ffd700;"></div></div>
    <button onclick="this.parentElement.style.display='none'">CERRAR DASHBOARD</button>
</div>

<button id="main-btn" onclick="location.href='/next'">{{ "INICIAR SISTEMA" if standby else "AVANZAR DÍA" }}</button>

<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// DOMO AUTO-ILUMINADO (Material Basic no falla)
const dome = new THREE.Mesh(
    new THREE.SphereGeometry(45, 32, 16, 0, Math.PI*2, 0, Math.PI/2),
    new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true, transparent:true, opacity:0.4})
);
scene.add(dome);

// BANDA
const belt = new THREE.Mesh(new THREE.BoxGeometry(120, 1, 15), new THREE.MeshBasicMaterial({color: 0x111111}));
belt.position.y = -5.5; scene.add(belt);

// BANDEJA DINÁMICA
const tray = new THREE.Group();
const trayBase = new THREE.Mesh(new THREE.BoxGeometry(16, 0.8, 11), new THREE.MeshBasicMaterial({color: 0x333333}));
tray.add(trayBase);

// COLCHÓN DE RAÍCES BLANCO
if ({{ d }} >= 1) {
    const rH = ({{ d }} * 0.4);
    const roots = new THREE.Mesh(new THREE.BoxGeometry(15.5, rH, 10.5), new THREE.MeshBasicMaterial({color: 0xffffff}));
    roots.position.y = 0.4 + rH/2;
    tray.add(roots);
}

// CRECIMIENTO (GRANOS O PASTO)
if ({{ d }} == 0) {
    for(let i=0; i<150; i++) {
        const grain = new THREE.Mesh(new THREE.SphereGeometry(0.2), new THREE.MeshBasicMaterial({color: 0xffcc00}));
        grain.position.set((Math.random()-0.5)*15, 0.5, (Math.random()-0.5)*10);
        tray.add(grain);
    }
} else {
    const grassH = ({{ d }} * 2.0);
    for(let i=0; i<500; i++) {
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.1, grassH, 0.1), new THREE.MeshBasicMaterial({color: ({{d}}<4?0xccff00:0x00ff44)}));
        blade.position.set((Math.random()-0.5)*15, 0.5 + grassH/2, (Math.random()-0.5)*10);
        tray.add(blade);
    }
}
if (!{{ standby|lower }}) scene.add(tray);

// RIEGO (PARTÍCULAS)
const rainGeo = new THREE.BufferGeometry();
const rainPos = [];
for(let i=0; i<200; i++) rainPos.push((Math.random()-0.5)*16, 20, (Math.random()-0.5)*11);
rainGeo.setAttribute('position', new THREE.Float32BufferAttribute(rainPos, 3));
const rainCol = ({{ d }} < 3) ? 0x00ffff : 0xaa8822; // Ajo + Nutrientes
const rain = new THREE.Points(rainGeo, new THREE.PointsMaterial({color: rainCol, size: 0.2}));
if (!{{ standby|lower }}) scene.add(rain);

// ANIMAL
const animal = new THREE.Mesh(new THREE.CapsuleGeometry(3, 7, 8, 16), new THREE.MeshBasicMaterial({color: 0x4d2600}));
animal.position.set(90, -1, 0); scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;

    // Animación de Riego
    if (rain.visible) {
        const positions = rain.geometry.attributes.position.array;
        for(let i=1; i<positions.length; i+=3) {
            positions[i] -= 0.5;
            if (positions[i] < 0) positions[i] = 20;
        }
        rain.geometry.attributes.position.needsUpdate = true;
    }

    if ({{ standby|lower }}) {
        camera.position.set(110*Math.sin(t*0.2), 60, 110*Math.cos(t*0.2));
        camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        camera.position.lerp(new THREE.Vector3(35, 20, 35), 0.05);
        camera.lookAt(0,0,0);
    } else {
        if(tray.position.x < 85) tray.position.x += 0.5;
        camera.position.lerp(new THREE.Vector3(140, 50, 40), 0.05);
        camera.lookAt(animal.position);
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
