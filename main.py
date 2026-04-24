import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-B28-{random.randint(1000,9999)}"
        # SCADA Expandido
        self.inv = {
            "ph": 5.8, "ce": 1.4, "vpd": 1.1, "co2": 450, 
            "temp_aire": 24.5, "hum_rel": 65, "luz_par": 850
        }
        # La Joya Expandida (Carbono y Potrero)
        self.pot = {
            "co2_cap": 0.0, "co2_suelo": 850, "hum_10": 24, 
            "rad_global": 620, "eficiencia_foto": 92, "biomasa_estimada": 0,
            "flujo_carbono": 0.52
        }
        self.mezcla = "Maíz (80%) + Cebada (15%) + Avena (5%)"

    def update(self):
        if self.dia < 7:
            self.dia += 1
            # Crecimiento real
            self.h = round(self.dia * 4.3, 1) if self.dia > 0 else 0.5
            self.p = round(12.0 + (self.dia * 10.5), 1)
            # Incremento en la Joya
            self.pot["co2_cap"] = round(self.dia * 6.1, 2)
            self.pot["biomasa_estimada"] = round(self.p * 0.85, 2)
            self.pot["eficiencia_foto"] = min(99, 92 + self.dia)
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_COMPLETO, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=getattr(ctrl, 'h', 0.5), p=getattr(ctrl, 'p', 12))

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_COMPLETO, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p)

# Fragmentación del HTML para evitar errores de búfer en Render
P1 = """
<!DOCTYPE html><html><head><title>NOVA v28 | Professional SCADA</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono', monospace; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,20,20,0.95); border: 2px solid #00ffcc; padding: 20px; z-index: 100; box-shadow: 0 0 25px rgba(0,255,204,0.3); }
    #left { top: 20px; left: 20px; width: 380px; border-left: 6px solid #00ffcc; }
    #right { top: 20px; right: 20px; width: 350px; border-right: 6px solid #ffd700; }
    .title { font-weight: 700; font-size: 14px; margin-bottom: 15px; color: #fff; text-transform: uppercase; border-bottom: 1px solid #00ffcc; padding-bottom: 5px; }
    .data { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; border-bottom: 1px solid rgba(0,255,204,0.1); }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    #btn-container { position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); z-index: 200; }
    button { background: #00ffcc; color: #000; border: none; padding: 20px 60px; font-weight: 900; font-family: 'Roboto Mono'; cursor: pointer; font-size: 16px; box-shadow: 0 0 20px #00ffcc; transition: 0.3s; }
    button:hover { background: #fff; transform: scale(1.05); }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

P2 = """
<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO | {{ bid }}</div>
    <div class="data">DÍA DEL CICLO: <span class="val">{{ d }} / 7</span></div>
    <div class="data">ALTURA BIOMASA: <span class="val">{{ h }} CM</span></div>
    <div class="data">PESO NETO LOTE: <span class="val">{{ p }} KG</span></div>
    <div class="data">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }} mS</span></div>
    <div class="data">VPD: <span class="val">{{ inv.vpd }} kPa</span></div>
    <div class="data">TEMP / HUM: <span class="val">{{ inv.temp_aire }}°C / {{ inv.hum_rel }}%</span></div>
    <div class="data">MEZCLA: <span class="val">{{ mez }}</span></div>
</div>
<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: MONITOR DE CARBONO</div>
    <div class="data">CO2 CAPTURADO: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">FLUJO CARBONO: <span class="joya-val">{{ pot.flujo_carbono }} mg/s</span></div>
    <div class="data">EFICIENCIA FOTO: <span class="val">{{ pot.eficiencia_foto }} %</span></div>
    <div class="data">CO2 SUELO/AMB: <span class="val">{{ pot.co2_suelo }} / {{ inv.co2 }} PPM</span></div>
    <div class="data">RAD. GLOBAL: <span class="val">{{ pot.rad_global }} W/m²</span></div>
    <div class="data">HUM. MATRIZ: <span class="val">{{ pot.hum_10 }} %</span></div>
</div>
<div id="btn-container"><button onclick="location.href='/next'">{{ "INICIAR DESPACHO" if d == 7 else "AVANZAR DÍA" }}</button></div>
"""

P3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 5000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const tower = new THREE.Group();
const floors = []; const doors = [];
const frameMat = new THREE.MeshStandardMaterial({color: 0x00ffcc, emissive: 0x00ffcc, emissiveIntensity: 0.5, wireframe: true});
const glassMat = new THREE.MeshStandardMaterial({color: 0x00ffff, transparent: true, opacity: 0.3, emissive: 0x00ffff, emissiveIntensity: 0.4});

for(let i=0; i<10; i++){
    const h = i * 7 - 25;
    const f = new THREE.Mesh(new THREE.BoxGeometry(14, 0.2, 14), frameMat); f.position.y = h;
    const tray = new THREE.Mesh(new THREE.BoxGeometry(12, 0.6, 12), new THREE.MeshStandardMaterial({color: 0x050505, emissive: 0x00ffcc, emissiveIntensity: 0.1})); 
    tray.position.y = h + 0.3;
    
    // EVOLUCIÓN DE SEMILLA
    const gH = ({{ d }} * 1.0) + 0.2;
    let bCol = 0xffaa00; // Día 0: Maíz
    if ({{ d }} > 0 && {{ d }} < 3) bCol = 0xbfff00; // Germinando
    if ({{ d }} >= 3) bCol = 0x00ff44; // Maduro
    
    const grass = new THREE.Mesh(new THREE.BoxGeometry(11.5, gH, 11.5), 
        new THREE.MeshStandardMaterial({
            color: bCol, 
            emissive: ({{d}} > 4 ? 0xff4400 : 0x000000), 
            emissiveIntensity: 0.3
        }));
    grass.position.y = h + 0.3 + gH/2;
    
    const dL = new THREE.Mesh(new THREE.BoxGeometry(6.8, 6.5, 0.1), glassMat); dL.position.set(-3.5, h+3.5, 7);
    const dR = new THREE.Mesh(new THREE.BoxGeometry(6.8, 6.5, 0.1), glassMat); dR.position.set(3.5, h+3.5, 7);
    
    tower.add(f, tray, grass, dL, dR); floors.push(h); doors.push({L: dL, R: dR});
}
scene.add(tower);
scene.add(new THREE.AmbientLight(0xffffff, 1.0));

// ROBÓTICA Y LOGÍSTICA
const robot = new THREE.Group();
const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 10), new THREE.MeshStandardMaterial({color: 0xff00ff, emissive: 0xff00ff}));
robot.add(arm); scene.add(robot); robot.visible = false;

const animal = new THREE.Group();
const body = new THREE.Mesh(new THREE.CapsuleGeometry(1.5, 3, 10, 20), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
body.rotation.z = Math.PI/2; animal.add(body);
animal.position.set(80, -25, 0); scene.add(animal);

const belt = new THREE.Mesh(new THREE.BoxGeometry(100, 0.5, 10), new THREE.MeshStandardMaterial({color: 0x111111}));
belt.position.set(50, -30, 0); scene.add(belt);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    
    if ({{ d }} == 0) {
        camera.position.lerp(new THREE.Vector3(120, 60, 120), 0.05); camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        const ty = floors[{{ d }}];
        camera.position.lerp(new THREE.Vector3(-35, ty + 12, 35), 0.05); camera.lookAt(0, ty, 0);
        // Puertas abren al máximo
        doors[{{ d }}].L.position.x = -12; doors[{{ d }}].R.position.x = 12;
    } else {
        // CICLO 7: ZOOM OUT NATURAL Y DESPACHO
        camera.position.lerp(new THREE.Vector3(140, 30, 80), 0.02); camera.lookAt(60, -20, 0);
        robot.visible = true; robot.position.set(10, -10 + Math.sin(t*5)*5, 0);
        if(animal.position.x > 65) animal.position.x -= 0.25;
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_COMPLETO = P1 + P2 + P3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)