import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-B27-{random.randint(100,999)}"
        self.inv = {"ph": 5.8, "ce": 1.4, "vpd": 1.1, "co2": 450}
        self.pot = {"co2_cap": 0.0, "co2_suelo": 850, "hum": 24, "rad": 620, "par": 1100}
        self.mezcla = "Maíz (80%) + Cebada (15%) + Avena (5%)"

    def update(self):
        if self.dia < 7:
            self.dia += 1
            # Lógica de crecimiento real
            self.h = round(self.dia * 4.3, 1) if self.dia > 0 else 0.5
            self.p = round(12.0 + (self.dia * 10.5), 1)
            self.pot["co2_cap"] = round(self.dia * 6.1, 2)
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_FINAL, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=getattr(ctrl, 'h', 0.5), p=getattr(ctrl, 'p', 12))

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_FINAL, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p)

# Fragmentación para estabilidad en Render
HTML_HEAD = """
<!DOCTYPE html><html><head><title>NOVA v27 | Bio-Digital Twin</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono', monospace; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,25,25,0.9); border: 1px solid #00ffcc; padding: 18px; z-index: 100; box-shadow: 0 0 20px rgba(0,255,204,0.2); }
    #left { top: 15px; left: 15px; width: 360px; border-left: 4px solid #00ffcc; }
    #right { top: 15px; right: 15px; width: 320px; border-right: 4px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; margin-bottom: 12px; color: #fff; text-transform: uppercase; letter-spacing: 1px; }
    .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px; border-bottom: 1px solid rgba(0,255,204,0.1); }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    button { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); background: #00ffcc; color: #000; border: none; padding: 18px 50px; font-weight: 900; font-family: 'Roboto Mono'; cursor: pointer; z-index: 200; box-shadow: 0 0 15px #00ffcc; }
    button:hover { background: #fff; scale: 1.05; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

HTML_UI = """
<div id="left" class="hud">
    <div class="title">SISTEMA SCADA: {{ bid }}</div>
    <div class="data">CICLO BIOLÓGICO: <span class="val">DÍA {{ d }}</span></div>
    <div class="data">ESTADO SEMILLA: <span class="val">{% if d==0 %}INOCULACIÓN{% elif d<3 %}GERMINACIÓN{% else %}FORRAJE VERDE{% endif %}</span></div>
    <div class="data">ALTURA REAL: <span class="val">{{ h }} CM</span></div>
    <div class="data">PESO ESTIMADO: <span class="val">{{ p }} KG</span></div>
    <div class="data">MEZCLA BALANCEADA: <span class="val">{{ mez }}</span></div>
</div>
<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: BALANCE DE CARBONO</div>
    <div class="data">CAPTURA NETA CO2: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">CO2 AMBIENTAL: <span class="val">{{ inv.co2 }} PPM</span></div>
    <div class="data">CO2 FLUJO SUELO: <span class="val">{{ pot.co2_suelo }} PPM</span></div>
    <div class="data">RAD. FOTOSINTÉTICA: <span class="val">{{ pot.par }} µmol</span></div>
    <div class="data">HUMEDAD MATRIZ: <span class="val">{{ pot.hum }} %</span></div>
</div>
<button onclick="location.href='/next'">{{ "INICIAR COSECHA" if d == 7 else "AVANZAR DÍA" }}</button>
"""

HTML_JS = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 4000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const tower = new THREE.Group();
const floors = []; const doors = [];
const frameMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true});
const glassMat = new THREE.MeshStandardMaterial({color: 0x00ffff, transparent: true, opacity: 0.25, emissive: 0x00ffff, emissiveIntensity: 0.3});

for(let i=0; i<10; i++){
    const h = i * 6 - 20;
    const f = new THREE.Mesh(new THREE.BoxGeometry(12, 0.2, 12), frameMat); f.position.y = h;
    const tray = new THREE.Mesh(new THREE.BoxGeometry(11, 0.5, 11), new THREE.MeshStandardMaterial({color: 0x111111})); tray.position.y = h + 0.25;
    
    // EVOLUCIÓN VISUAL DE LA SEMILLA
    const gH = ({{ d }} * 0.8) + 0.2;
    let bioColor = 0xffcc33; // Día 0: Maíz (Oro/Café)
    if ({{ d }} > 0 && {{ d }} < 3) bioColor = 0xccff33; // Germinación
    if ({{ d }} >= 3) bioColor = 0x00ff44; // Forraje Verde

    const grass = new THREE.Mesh(new THREE.BoxGeometry(10.5, gH, 10.5), 
        new THREE.MeshStandardMaterial({
            color: bioColor, 
            emissive: ({{d}} > 4 ? 0xff3300 : 0x000000), 
            emissiveIntensity: 0.2 // Termografía sutil
        }));
    grass.position.y = h + 0.25 + gH/2;
    
    const dL = new THREE.Mesh(new THREE.BoxGeometry(5.8, 5.5, 0.1), glassMat); dL.position.set(-2.9, h+3, 6);
    const dR = new THREE.Mesh(new THREE.BoxGeometry(5.8, 5.5, 0.1), glassMat); dR.position.set(2.9, h+3, 6);
    
    tower.add(f, tray, grass, dL, dR); floors.push(h); doors.push({L: dL, R: dR});
}
scene.add(tower);
scene.add(new THREE.AmbientLight(0xffffff, 0.8));

// Goteo de micro-aspersión
const drip = new THREE.Points(
    new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0)]),
    new THREE.PointsMaterial({color: 0x00ffff, size: 0.1})
);
scene.add(drip); drip.visible = false;

const robot = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 8), new THREE.MeshBasicMaterial({color: 0xff00ff}));
scene.add(robot); robot.visible = false;

const animal = new THREE.Group();
const aBody = new THREE.Mesh(new THREE.CapsuleGeometry(1.2, 2.5, 8, 16), new THREE.MeshStandardMaterial({color: 0x442200}));
aBody.rotation.z = Math.PI/2; animal.add(aBody);
animal.position.set(70, -22, 0); scene.add(animal);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    if ({{ d }} == 0) {
        camera.position.lerp(new THREE.Vector3(90, 40, 90), 0.05); camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        const ty = floors[{{ d }}];
        camera.position.lerp(new THREE.Vector3(-25, ty + 10, 25), 0.05); camera.lookAt(0, ty, 0);
        doors[{{ d }}].L.position.x = -10; doors[{{ d }}].R.position.x = 10;
        drip.visible = true; drip.position.set(Math.sin(t*5)*2, ty + 5, Math.cos(t*5)*2);
    } else {
        camera.position.lerp(new THREE.Vector3(100, 20, 60), 0.02); camera.lookAt(50, -15, 0);
        robot.visible = true; robot.position.set(10, -15 + Math.sin(t*4), 0);
        if(animal.position.x > 60) animal.position.x -= 0.2;
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_FINAL = HTML_HEAD + HTML_UI + HTML_JS

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
