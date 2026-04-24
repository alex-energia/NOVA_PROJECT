import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-1TON-{random.randint(100,999)}"
        # Variables Invernadero (Escala 1 Tonelada)
        self.inv = {
            "ph": 0.0, "ce": 0.0, "vpd": 0.0, "co2_int": 0, 
            "par": 0, "agua_total": 0, "temp": 0.0, "dli": 0.0,
            "flujo_aire": 0.0, "hum_rel": 0
        }
        # Variables La Joya (Potrero e Impacto)
        self.pot = {
            "co2_cap": 0.0, "co2_s": 0, "ch4_red": 0.0, 
            "h10": 0, "rad": 0, "ndvi": 0.0, "viento": 0.0,
            "presion": 0
        }
        self.h = 0.0
        self.p = 0.0 # Peso en KG
        self.mezcla = "Maíz 800kg + Cebada 150kg + Avena 50kg (Base 1 Ton)"

    def update(self):
        if self.standby:
            self.standby = False
            self.dia = 0
            self.inv.update({"ph": 5.9, "ce": 1.6, "vpd": 1.2, "co2_int": 480, "par": 950, "temp": 24.5, "hum_rel": 68, "flujo_aire": 1200})
            self.pot.update({"co2_s": 860, "h10": 26, "rad": 650, "ndvi": 0.70, "viento": 14.2, "presion": 1013})
        elif self.dia < 7:
            self.dia += 1
            # Crecimiento para llegar a 1000kg (1 Tonelada)
            self.h = round(self.dia * 4.6, 1)
            self.p = round(150 + (self.dia * 121.4), 1) # Inicia en 150kg semilla -> termina en ~1000kg
            self.pot["co2_cap"] = round(self.dia * 8.4, 2)
            self.pot["ch4_red"] = round(self.dia * 2.1, 2)
            self.inv["agua_total"] += 450 # Litros por día para 1 Ton
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V31, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p, standby=ctrl.standby)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V31, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p, standby=ctrl.standby)

# --- ESTRUCTURA HTML Y CSS ---
P1 = """
<!DOCTYPE html><html><head><title>NOVA v31 | 1 Ton Production</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono', monospace; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,20,20,0.95); border: 2px solid #00ffcc; padding: 15px; z-index: 100; border-radius: 5px; box-shadow: 0 0 20px #004444; }
    #left { top: 15px; left: 15px; width: 420px; }
    #right { top: 15px; right: 15px; width: 400px; border-right: 4px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; margin-bottom: 8px; color: #fff; text-transform: uppercase; border-bottom: 1px solid #00ffcc; }
    .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    
    /* DASHBOARD DE GRÁFICAS */
    #chart-panel { display:none; position:fixed; top:10%; left:10%; width:80%; height:80%; background:rgba(0,10,10,0.98); border:3px solid #00ffcc; z-index:500; padding:20px; overflow-y:auto; }
    .bar-container { width: 100%; background: #222; height: 20px; margin: 10px 0; border: 1px solid #444; }
    .bar-fill { height: 100%; background: #00ffcc; transition: 0.5s; }
    
    #controls { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); z-index: 200; display:flex; gap:10px; }
    button { background: #00ffcc; color: #000; border: none; padding: 15px 40px; font-weight: 900; cursor: pointer; font-family: 'Roboto Mono'; }
    .btn-alt { background: #ffd700; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

P2 = """
<div id="left" class="hud">
    <div class="title">SCADA PRODUCCIÓN: 1 TON/DÍA</div>
    <div class="data">LOTE: <span class="val">{{ bid }}</span> | DÍA: <span class="val">{{ d }}</span></div>
    <div class="data">ALTURA FORRAJE: <span class="val">{{ h }} CM</span></div>
    <div class="data">PESO ACTUAL: <span class="val">{{ p }} KG</span></div>
    <div class="data">PH/CE: <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
    <div class="data">RADIACIÓN PAR: <span class="val">{{ inv.par }}</span></div>
    <div class="data">CONSUMO H2O: <span class="val">{{ inv.agua_total }} L</span></div>
    <div class="data">FLUJO AIRE: <span class="val">{{ inv.flujo_aire }} m3/h</span></div>
    <div class="data">MEZCLA: <span class="val">{{ mez }}</span></div>
    <button style="margin-top:10px; width:100%;" onclick="document.getElementById('chart-panel').style.display='block'">📈 ABRIR ANALÍTICA AVANZADA</button>
</div>

<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: MÉTRICAS 1T</div>
    <div class="data">CO2 CAPTURADO: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">RED. METANO: <span class="joya-val">{{ pot.ch4_red }} KG</span></div>
    <div class="data">CO2 SUELO: <span class="val">{{ pot.co2_s }} PPM</span></div>
    <div class="data">NDVI SATELITAL: <span class="val">{{ pot.ndvi }}</span></div>
    <div class="data">VIENTO / PRES: <span class="val">{{ pot.viento }} km/h / {{ pot.presion }} hPa</span></div>
</div>

<div id="chart-panel">
    <button onclick="this.parentElement.style.display='none'" style="float:right">CERRAR X</button>
    <h2 style="color:#00ffcc">DASHBOARD DE RENDIMIENTO - 1 TONELADA</h2>
    <p>PROGRESO DE PESO (Meta 1000kg):</p>
    <div class="bar-container"><div class="bar-fill" style="width: {{ (p/1000)*100 }}%"></div></div>
    <p>CAPTURA DE CO2 ACUMULADA:</p>
    <div class="bar-container"><div class="bar-fill" style="width: {{ (pot.co2_cap/60)*100 }}%; background:#ffd700;"></div></div>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
        <div style="border:1px solid #444; padding:10px;">
            <h3>EFICIENCIA HÍDRICA</h3>
            <p>Consumo optimizado para 1000kg de forraje verde.</p>
        </div>
        <div style="border:1px solid #444; padding:10px;">
            <h3>TERMOGRAFÍA</h3>
            <p>Puntos de calor detectados: Normal (24.5°C)</p>
        </div>
    </div>
</div>

<div id="controls">
    <button onclick="location.href='/next'">{{ "INICIAR PROCESO 1T" if standby else ("COSECHAR" if d==7 else "AVANZAR DÍA") }}</button>
</div>
"""

P3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// LUZ QUE SIGUE A LA CÁMARA
const light = new THREE.DirectionalLight(0xffffff, 1.5);
scene.add(light);

// --- EL BIO-DOMO ---
const domeGroup = new THREE.Group();

// Base Industrial
const base = new THREE.Mesh(new THREE.CylinderGeometry(25, 25, 2, 32), new THREE.MeshLambertMaterial({color: 0x222222}));
base.position.y = -1;
domeGroup.add(base);

// Estructura Geodésica (Visible)
const shell = new THREE.Mesh(
    new THREE.SphereGeometry(25, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2),
    new THREE.MeshLambertMaterial({color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.4})
);
domeGroup.add(shell);

// Puertas de Cristal (Paneles que se abren)
const doorL = new THREE.Mesh(new THREE.SphereGeometry(25.1, 16, 8, 0, 1, 0, 1), new THREE.MeshLambertMaterial({color: 0x00ffff, transparent: true, opacity: 0.3}));
const doorR = new THREE.Mesh(new THREE.SphereGeometry(25.1, 16, 8, 1, 1, 0, 1), new THREE.MeshLambertMaterial({color: 0x00ffff, transparent: true, opacity: 0.3}));
domeGroup.add(doorL, doorR);

// BIOMASA (Crecimiento Semilla a 1 Ton)
const bioH = ({{ d }} * 2.0) + 0.5;
let bioCol = ({{ d }} == 0) ? 0xffaa00 : ({{ d }} < 3) ? 0xaaff00 : 0x00ff00;
const biomasa = new THREE.Mesh(
    new THREE.CylinderGeometry(22, 22, bioH, 32),
    new THREE.MeshLambertMaterial({color: bioCol, emissive: ({{d}}>4 ? 0xff0000 : 0x000000), emissiveIntensity: 0.2})
);
biomasa.position.y = bioH/2 - 1;
biomasa.visible = !{{ standby|lower }};
domeGroup.add(biomasa);

scene.add(domeGroup);

// Robot de Despacho
const robot = new THREE.Mesh(new THREE.BoxGeometry(2,10,2), new THREE.MeshLambertMaterial({color: 0xff00ff}));
robot.position.set(35, 0, 0); robot.visible = ({{d}} == 7);
scene.add(robot);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    light.position.copy(camera.position); // La luz siempre apunta donde miras

    if ({{ standby|lower }}) {
        camera.position.set(80 * Math.sin(t*0.3), 40, 80 * Math.cos(t*0.3));
        camera.lookAt(0, 0, 0);
    } else if ({{ d }} < 7) {
        // Zoom Interior
        camera.position.lerp(new THREE.Vector3(30, 15, 30), 0.05);
        camera.lookAt(0, 5, 0);
        // Abrir Puertas
        doorL.rotation.y = Math.sin(t) * 0.5;
        doorR.rotation.y = -Math.sin(t) * 0.5;
    } else {
        // Zoom Out y Robots
        camera.position.lerp(new THREE.Vector3(100, 30, 0), 0.02);
        camera.lookAt(0, 0, 0);
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_V31 = P1 + P2 + P3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)