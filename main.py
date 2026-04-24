import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-B25-{random.randint(100,999)}"
        self.inv = {"ph": 5.8, "vpd": 1.2, "etc": 3.4, "peso": 12.0, "co2": 450, "h_semilla": 0.5}
        self.pot = {"co2_captura": 15.2, "co2_suelo": 850, "hum": 22, "rad": 650}
        self.mezcla = "80% Maíz + 15% Cebada + 5% Avena"

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["h_semilla"] = round(0.5 + (self.dia * 4.5), 1)
            self.inv["peso"] = round(12.0 + (self.dia * 10.5), 1)
            self.pot["co2_captura"] += 5.4
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_CORE, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_CORE, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla)

# --- FRACCIONAMIENTO PARA EVITAR SYNTAX ERROR ---
HTML_PART1 = """
<!DOCTYPE html><html><head><title>NOVA v25</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
<style>
:root { --neon: #00ffcc; --gold: #ffd700; --bg: #000; }
body { margin: 0; background: var(--bg); color: white; font-family: 'Orbitron'; overflow: hidden; }
.hud { position: absolute; background: rgba(0, 15, 15, 0.9); border: 2px solid var(--neon); padding: 15px; z-index: 100; }
#ui-left { top: 10px; left: 10px; width: 320px; }
#ui-right { top: 10px; right: 10px; width: 280px; }
.stat { display: flex; justify-content: space-between; font-size: 10px; margin-bottom: 5px; }
.val { color: #fff; }
button { background: var(--neon); border: none; padding: 12px; width: 100%; cursor: pointer; font-family: 'Orbitron'; font-weight: 900; margin-top: 5px; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

HTML_PART2 = """
<div id="ui-left" class="hud">
    <h2>CORE: {{ bid }}</h2>
    <div class="stat">DÍA: <span class="val">{{ d }} / 7</span></div>
    {% if d == 0 %}<div class="stat" style="color:var(--gold)">MEZCLA: <span class="val">{{ mez }}</span></div>{% endif %}
    <div class="stat">ALTURA: <span class="val">{{ inv.h_semilla }} CM</span></div>
    <div class="stat">PESO: <span class="val">{{ inv.peso }} KG</span></div>
    <button onclick="location.href='/next'">{{ "COSECHAR" if d == 6 else "SIGUIENTE" if d < 7 else "REINICIAR" }}</button>
</div>
<div id="ui-right" class="hud">
    <h2 style="color:var(--gold)">LA JOYA: CO2</h2>
    <div class="stat">CAPTURA: <span class="val">{{ pot.co2_captura }} KG</span></div>
    <div class="stat">CO2 SUELO: <span class="val">{{ pot.co2_suelo }} PPM</span></div>
    <div class="stat">RAD: <span class="val">{{ pot.rad }} W/m²</span></div>
</div>
"""

HTML_PART3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 3000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);
scene.add(new THREE.AmbientLight(0xffffff, 0.5));

const tower = new THREE.Group();
const floors = []; const doors = [];
const frameMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true});
const glassMat = new THREE.MeshStandardMaterial({color: 0x00ffff, transparent: true, opacity: 0.4, emissive: 0x00ffff, emissiveIntensity: 0.5});

for(let i=0; i<10; i++){
    const h = i * 4.5 - 15;
    const f = new THREE.Mesh(new THREE.BoxGeometry(9, 0.2, 9), frameMat); f.position.y = h;
    const tray = new THREE.Mesh(new THREE.BoxGeometry(8, 0.4, 8), new THREE.MeshStandardMaterial({color: 0x222222, emissive: 0x00ffcc, emissiveIntensity: 0.1}));
    tray.position.y = h + 0.2;
    const gH = ({{ d }} * 0.6) + 0.2;
    const g = new THREE.Mesh(new THREE.BoxGeometry(7.5, gH, 7.5), new THREE.MeshStandardMaterial({color: ({{d}}==0?0x5c4033:0x00ff44)}));
    g.position.y = h + 0.2 + gH/2;
    const dL = new THREE.Mesh(new THREE.BoxGeometry(4.2, 4, 0.1), glassMat); dL.position.set(-2.1, h+2.2, 4.5);
    const dR = new THREE.Mesh(new THREE.BoxGeometry(4.2, 4, 0.1), glassMat); dR.position.set(2.1, h+2.2, 4.5);
    tower.add(f, tray, g, dL, dR); floors.push(h); doors.push({L: dL, R: dR});
}
scene.add(tower);

const animal = new THREE.Group();
animal.add(new THREE.Mesh(new THREE.SphereGeometry(1.2, 16, 16), new THREE.MeshStandardMaterial({color: 0x442200})));
animal.position.set(60, -18, 0); scene.add(animal);
const belt = new THREE.Mesh(new THREE.BoxGeometry(60, 0.4, 6), new THREE.MeshStandardMaterial({color: 0x111111}));
belt.position.set(30, -19.5, 0); scene.add(belt);
const trayH = new THREE.Mesh(new THREE.BoxGeometry(4, 0.2, 4), new THREE.MeshBasicMaterial({color: 0x00ff44}));
trayH.position.set(5, -19, 0); trayH.visible = ({{ d }} == 7); scene.add(trayH);

const robot = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 5), new THREE.MeshBasicMaterial({color: 0xff00ff}));
scene.add(robot); robot.visible = false;

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    if ({{ d }} == 0) {
        camera.position.lerp(new THREE.Vector3(75, 30, 75), 0.05); camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        const ty = floors[{{ d }}];
        camera.position.lerp(new THREE.Vector3(-18, ty + 6, 18), 0.05); camera.lookAt(0, ty, 0);
        doors[{{ d }}].L.position.x = -6.5; doors[{{ d }}].R.position.x = 6.5;
    } else {
        camera.position.lerp(new THREE.Vector3(85, 20, 50), 0.02); camera.lookAt(40, -10, 0);
        robot.visible = true; robot.position.set(5, -15 + Math.sin(t*2), 0);
        if(trayH.position.x < 55) trayH.position.x += 0.3;
        if(animal.position.x > 57) animal.position.x -= 0.15;
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_CORE = HTML_PART1 + HTML_PART2 + HTML_PART3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)