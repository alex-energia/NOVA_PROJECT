import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()
        self.standby = True  # Inicia en modo espera (Todo en 0)

    def reset(self):
        self.dia = 0
        self.standby = True
        self.batch_id = f"NOVA-X29-{random.randint(1000,9999)}"
        # SCADA Completo
        self.inv = {
            "ph": 0.0, "ce": 0.0, "vpd": 0.0, "co2": 0.0, 
            "par": 0, "o2_dis": 0.0, "temp": 0.0, "hum_rel": 0
        }
        # La Joya Completa
        self.pot = {
            "co2_cap": 0.0, "co2_suelo": 0, "ch4": 0.0, 
            "h10": 0, "h30": 0, "h60": 0, "rad": 0, "ndvi": 0.0
        }
        self.h = 0.0
        self.p = 0.0
        self.mezcla = "---"

    def update(self):
        if self.standby:
            self.standby = False
            self.dia = 0
            # Valores iniciales Día 0
            self.inv.update({"ph": 5.8, "ce": 1.2, "vpd": 0.8, "co2": 420, "par": 400, "o2_dis": 8.5, "temp": 22.0, "hum_rel": 70})
            self.pot.update({"co2_suelo": 820, "h10": 25, "h30": 20, "h60": 18, "rad": 450, "ndvi": 0.65})
            self.mezcla = "80% Maíz + 15% Cebada + 5% Avena"
        elif self.dia < 7:
            self.dia += 1
            self.h = round(self.dia * 4.4, 1)
            self.p = round(12.0 + (self.dia * 10.8), 1)
            # Incrementales de la Joya
            self.pot["co2_cap"] = round(self.dia * 6.25, 2)
            self.pot["ndvi"] = min(0.95, 0.65 + (self.dia * 0.04))
            self.inv["co2"] += random.randint(-10, 10)
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    return render_template_string(HTML_V29, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p, standby=ctrl.standby)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V29, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla, h=ctrl.h, p=ctrl.p, standby=ctrl.standby)

# HTML Estructurado para máxima estabilidad en Render
P1 = """
<!DOCTYPE html><html><head><title>NOVA v29 | Industrial SCADA</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
    body { margin: 0; background: #000; color: #00ffcc; font-family: 'Roboto Mono', monospace; overflow: hidden; }
    .hud { position: absolute; background: rgba(0,10,10,0.9); border: 1px solid #00ffcc; padding: 15px; z-index: 100; box-shadow: 0 0 20px rgba(0,255,204,0.2); }
    #left { top: 10px; left: 10px; width: 400px; }
    #right { top: 10px; right: 10px; width: 380px; border-right: 4px solid #ffd700; }
    .title { font-weight: 700; font-size: 13px; margin-bottom: 10px; color: #fff; text-transform: uppercase; border-bottom: 1px solid #333; }
    .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; }
    .val { color: #fff; font-weight: bold; }
    .joya-val { color: #ffd700; font-weight: bold; }
    #controls { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 200; }
    button { background: #00ffcc; color: #000; border: none; padding: 15px 50px; font-weight: 900; font-family: 'Roboto Mono'; cursor: pointer; font-size: 14px; box-shadow: 0 0 15px #00ffcc; transition: 0.2s; }
    button:hover { background: #fff; scale: 1.05; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script></head><body>
"""

P2 = """
<div id="left" class="hud">
    <div class="title">SCADA INVERNADERO BIOMASA | {{ bid }}</div>
    <div class="data">DÍA: <span class="val">{{ d if not standby else 0 }}</span></div>
    <div class="data">ALTURA: <span class="val">{{ h }} CM</span></div>
    <div class="data">PESO: <span class="val">{{ p }} KG</span></div>
    <div class="data">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }} mS</span></div>
    <div class="data">VPD / CO2: <span class="val">{{ inv.vpd }} / {{ inv.co2 }} PPM</span></div>
    <div class="data">RADIACIÓN PAR: <span class="val">{{ inv.par }} µmol/m²</span></div>
    <div class="data">O2 DISUELTO: <span class="val">{{ inv.o2_dis }} mg/L</span></div>
    <div class="data">TEMP/HUM: <span class="val">{{ inv.temp }}°C / {{ inv.hum_rel }}%</span></div>
    <div class="data">MEZCLA: <span class="val">{{ mez }}</span></div>
</div>
<div id="right" class="hud">
    <div class="title" style="color:#ffd700">LA JOYA: ECO-SISTEMA & CARBONO</div>
    <div class="data">CAPTURA CO2: <span class="joya-val">{{ pot.co2_cap }} KG</span></div>
    <div class="data">CO2 SUELO: <span class="val">{{ pot.co2_suelo }} PPM</span></div>
    <div class="data">METANO (CH4): <span class="val">{{ pot.ch4 }} mg/m³</span></div>
    <div class="data">HUM. SUELO (10/30/60): <span class="val">{{ pot.h10 }}/{{ pot.h30 }}/{{ pot.h60 }}%</span></div>
    <div class="data">RAD. GLOBAL: <span class="val">{{ pot.rad }} W/m²</span></div>
    <div class="data">ÍNDICE NDVI: <span class="val">{{ pot.ndvi }}</span></div>
</div>
<div id="controls"><button onclick="location.href='/next'">{{ "INICIAR SISTEMA" if standby else ("DESPACHAR" if d == 7 else "AVANZAR DÍA") }}</button></div>
"""

P3 = """
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 5000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// ILUMINACIÓN CONSTANTE PARA LA TORRE
const towerGroup = new THREE.Group();
const floors = []; const doors = [];
const glowMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true});
const glassMat = new THREE.MeshBasicMaterial({color: 0x00ffff, transparent: true, opacity: 0.15});

for(let i=0; i<10; i++){
    const h = i * 7 - 25;
    // Estructura auto-iluminada (MeshBasic no necesita luces)
    const frame = new THREE.Mesh(new THREE.BoxGeometry(15, 0.2, 15), glowMat);
    frame.position.y = h;
    
    const tray = new THREE.Mesh(new THREE.BoxGeometry(13, 0.5, 13), new THREE.MeshBasicMaterial({color: 0x111111}));
    tray.position.y = h + 0.3;
    
    // EVOLUCIÓN VISUAL
    let bioColor = 0x5c4033; // Tierra/Maíz
    if ({{ d }} > 0 && {{ d }} < 3) bioColor = 0xbfff00;
    if ({{ d }} >= 3) bioColor = 0x00ff44;
    
    const gH = ({{ d }} * 1.2) + 0.3;
    const grass = new THREE.Mesh(new THREE.BoxGeometry(12, gH, 12), new THREE.MeshBasicMaterial({color: bioColor}));
    grass.position.y = h + 0.3 + gH/2;
    if ({{ standby }} == true) grass.visible = false;

    const dL = new THREE.Mesh(new THREE.BoxGeometry(7, 6.8, 0.1), glassMat); dL.position.set(-3.7, h+3.6, 7.5);
    const dR = new THREE.Mesh(new THREE.BoxGeometry(7, 6.8, 0.1), glassMat); dR.position.set(3.7, h+3.6, 7.5);
    
    towerGroup.add(frame, tray, grass, dL, dR);
    floors.push(h); doors.push({L: dL, R: dR});
}
scene.add(towerGroup);

// ROBOT Y ELEMENTOS EXTERNOS
const animal = new THREE.Mesh(new THREE.BoxGeometry(5,3,2), new THREE.MeshBasicMaterial({color: 0x442200}));
animal.position.set(90, -30, 0); scene.add(animal);
const trayH = new THREE.Mesh(new THREE.BoxGeometry(6,0.3,6), new THREE.MeshBasicMaterial({color:0x00ff44}));
trayH.position.set(10, -30, 0); trayH.visible = ({{d}}==7); scene.add(trayH);

function animate() {
    requestAnimationFrame(animate);
    const t = Date.now() * 0.001;
    if ({{ standby }} == true) {
        camera.position.lerp(new THREE.Vector3(150, 80, 150), 0.05);
        camera.lookAt(0,0,0);
    } else if ({{ d }} < 7) {
        const ty = floors[{{ d }}];
        camera.position.lerp(new THREE.Vector3(-40, ty + 15, 40), 0.05);
        camera.lookAt(0, ty, 0);
        doors[{{ d }}].L.position.x = -15; doors[{{ d }}].R.position.x = 15;
    } else {
        camera.position.lerp(new THREE.Vector3(160, 40, 100), 0.03);
        camera.lookAt(70, -20, 0);
        if(animal.position.x > 70) animal.position.x -= 0.3;
    }
    renderer.render(scene, camera);
}
animate();
</script></body></html>
"""

HTML_V29 = P1 + P2 + P3

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)