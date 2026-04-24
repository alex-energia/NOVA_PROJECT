import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-500K-v35-{random.randint(100,999)}"
        self.inv = {"ph":0,"ce":0,"vpd":0,"co2":0,"par":0,"temp":0,"hum":0,"agua":0,"dli":0,"aire":0}
        self.pot = {"co2_cap":0,"co2_s":0,"ch4":0,"ndvi":0,"viento":0,"presion":0,"hum_f":0,"rad":0}
        self.h = 0; self.pb = 0; self.pt = 0; self.mezcla = "---"

    def update(self):
        if self.standby:
            self.standby = False
            self.dia = 0
            self.inv.update({"ph":5.8,"ce":1.4,"vpd":1.1,"co2":450,"par":850,"temp":24,"hum":65,"agua":100,"dli":22,"aire":1100})
            self.pot.update({"co2_s":840,"ch4":0.02,"ndvi":0.65,"viento":12,"presion":1012,"hum_f":45,"rad":610})
            self.mezcla = "Maíz (400kg) + Cebada (75kg) + Avena (25kg)"
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.5, 1)
            self.pb = round(2.5 + (self.dia * 1.8), 1)
            self.pt = round(80 + (self.dia * 60), 1)
            self.pot["co2_cap"] = round(self.dia * 4.8, 2)
        else: self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V35, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V35, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, h=ctrl.h, pb=ctrl.pb, pt=ctrl.pt, standby=ctrl.standby, mez=ctrl.mezcla)

HTML_V35 = """
<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono'; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,25,25,0.95); border: 2px solid #00ffcc; padding: 15px; z-index: 100; width: 420px; }
    #left { top: 10px; left: 10px; border-left: 5px solid #00ffcc; }
    #right { top: 10px; right: 10px; border-right: 5px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; border-bottom: 2px solid #00ffcc; margin-bottom: 8px; }
    .row { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; }
    .val { color: #fff; }
    .joya { color: #ffd700; }
    
    /* PANEL DE GRÁFICAS REAL */
    #chart-panel { display:none; position:fixed; top:15%; left:15%; width:70%; height:70%; background:#050505; border:3px solid #00ffcc; z-index:500; padding:25px; box-shadow: 0 0 50px #004444; }
    .bar-bg { width: 100%; background: #222; height: 20px; margin: 10px 0; border: 1px solid #444; }
    .bar-fill { height: 100%; background: #00ffcc; transition: 1s ease-out; }
    
    button { background: #00ffcc; border: none; padding: 10px; cursor: pointer; font-weight: 900; width: 100%; margin-top: 5px; }
    #main-btn { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); width: 280px; font-size: 16px; border-radius: 5px; box-shadow: 0 0 20px #00ffcc; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head><body>

<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO | 500KG</div>
    <div class="row"><span>DÍA / LOTE:</span> <span class="val">{{ d }} / {{ bid }}</span></div>
    <div class="row"><span>MEZCLA:</span> <span class="val">{{ mez }}</span></div>
    <div class="row"><span>ALTURA / PESO BAND:</span> <span class="val">{{ h }}cm / {{ pb }}kg</span></div>
    <div class="row"><span>PROD TOTAL:</span> <span class="val">{{ pt }} / 500 KG</span></div>
    <div class="row"><span>PH/CE:</span> <span class="val">{{ inv.ph }}/{{ inv.ce }}</span> | <span>VPD:</span> <span class="val">{{ inv.vpd }}</span></div>
    <div class="row"><span>CO2:</span> <span class="val">{{ inv.co2 }} PPM</span> | <span>TEMP:</span> <span class="val">{{ inv.temp }}°C</span></div>
    <div class="row"><span>HUM:</span> <span class="val">{{ inv.hum }}%</span> | <span>AIRE:</span> <span class="val">{{ inv.aire }} m3</span></div>
    <div class="row"><span>PAR:</span> <span class="val">{{ inv.par }}</span> | <span>DLI:</span> <span class="val">{{ inv.dli }}</span></div>
    <button onclick="document.getElementById('chart-panel').style.display='block'">📈 ABRIR ANALÍTICA DE CRECIMIENTO</button>
</div>

<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: MÉTRICAS DE IMPACTO</div>
    <div class="row"><span>CAPTURA CO2:</span> <span class="joya">{{ pot.co2_cap }} KG</span></div>
    <div class="row"><span>CO2 SUELO:</span> <span class="val">{{ pot.co2_s }}</span> | <span>CH4:</span> <span class="val">{{ pot.ch4 }}</span></div>
    <div class="row"><span>NDVI:</span> <span class="val">{{ pot.ndvi }}</span> | <span>RAD:</span> <span class="val">{{ pot.rad }}</span></div>
    <div class="row"><span>VIENTO:</span> <span class="val">{{ pot.viento }}km/h</span> | <span>PRES:</span> <span class="val">{{ pot.presion }}</span></div>
    <div class="row"><span>HUM FOLIAR:</span> <span class="val">{{ pot.hum_f }}%</span></div>
    <button onclick="document.getElementById('chart-panel').style.display='block'" style="background:#ffd700">📈 ANALÍTICA CARBONO</button>
</div>

<div id="chart-panel">
    <h2 style="color:#00ffcc">DASHBOARD OPERATIVO - UNIDAD 500KG</h2>
    <p>EFICIENCIA DE PRODUCCIÓN (Día {{d}}):</p>
    <div class="bar-bg"><div class="bar-fill" style="width:{{(pt/500)*100}}%"></div></div>
    <p>CAPTURA DE CARBONO (KG):</p>
    <div class="bar-bg"><div class="bar-fill" style="width:{{(pot.co2_cap/35)*100}}%; background:#ffd700;"></div></div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-top:20px; font-size:12px;">
        <div style="border:1px solid #444; padding:10px;"><h3>STATUS RIEGO</h3><p>Balance Hídrico: Óptimo</p></div>
        <div style="border:1px solid #444; padding:10px;"><h3>TERMOGRAFÍA</h3><p>Temp Media Foliar: {{inv.temp}}°C</p></div>
    </div>
    <button onclick="this.parentElement.style.display='none'" style="margin-top:20px;">CERRAR DASHBOARD</button>
</div>

<button id="main-btn" onclick="location.href='/next'">{{ "INICIAR PROCESO" if standby else "AVANZAR DÍA" }}</button>

<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// DOMO
const dome = new THREE.Mesh(
    new THREE.SphereGeometry(45, 32, 16, 0, Math.PI*2, 0, Math.PI/2),
    new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true, transparent:true, opacity:0.3})
);
scene.add(dome);

// BANDA
const belt = new THREE.Mesh(new THREE.BoxGeometry(100, 1, 15), new THREE.MeshBasicMaterial({color: 0x151515}));
belt.position.y = -5; scene.add(belt);

// BANDEJA CON COLCHÓN DE RAÍCES
const tray = new THREE.Group();
const trayBase = new THREE.Mesh(new THREE.BoxGeometry(16, 0.8, 11), new THREE.MeshBasicMaterial({color: 0x333333}));
tray.add(trayBase);

if ({{ d }} >= 1) {
    const rootH = ({{ d }} * 0.3) + 0.2;
    const roots = new THREE.Mesh(new THREE.BoxGeometry(15.5, rootH, 10.5), new THREE.MeshBasicMaterial({color: 0xeeeeee}));
    roots.position.y = 0.4 + rootH/2;
    tray.add(roots);
}

// CRECIMIENTO DETALLADO
if ({{ d }} == 0) {
    for(let i=0; i<100; i++) {
        const m = new THREE.Mesh(new THREE.SphereGeometry(0.25), new THREE.MeshBasicMaterial({color: 0xffcc00}));
        m.position.set((Math.random()-0.5)*14, 0.5, (Math.random()-0.5)*9);
        tray.add(m);
    }
} else {
    const grassH = ({{ d }} * 1.8);
    for(let i=0; i<400; i++) {
        const hVar = grassH * (0.8 + Math.random()*0.4);
        const blade = new THREE.Mesh(new THREE.BoxGeometry(0.1, hVar, 0.1), 
            new THREE.MeshBasicMaterial({color: ({{d}}<3?0xccff00:0x00ff44)}));
        blade.position.set((Math.random()-0.5)*15, 0.5 + hVar/2, (Math.random()-0.5)*10);
        tray.add(blade);
    }
}

if (!{{ standby|lower }}) scene.add(tray);

// ANIMAL
const animal = new THREE.Mesh(new THREE.CapsuleGeometry(3, 6, 8, 16), new THREE.MeshBasicMaterial({color: 0x4d2600}));
animal.position.set(85, -1, 0); scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    if ({{ standby|lower }}) {
        camera.position.set(110*Math.sin(t*0.2), 60, 110*Math.cos(t*0.2));
        camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        camera.position.lerp(new THREE.Vector3(35, 25, 35), 0.05);
        camera.lookAt(0,0,0);
    } else {
        if(tray.position.x < 80) tray.position.x += 0.4;
        camera.position.lerp(new THREE.Vector3(130, 45, 40), 0.05);
        camera.lookAt(animal.position);
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)