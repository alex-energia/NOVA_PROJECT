import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-X20-{random.randint(100,999)}"
        self.inv = {
            "ph": 5.8, "ce": 1.7, "co2": 420, "tanque": 100,
            "presion": 44.5, "peso": 12.0, "crecimiento": 0, "temp_foliar": 18.5
        }
        self.pot = {"h2o_save": 0, "ch4": 0, "ndvi": 0.68}
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["crecimiento"] = round(self.dia * 4.5, 1)
            self.inv["peso"] = round(12.0 + (self.dia * 9.8), 1)
            self.inv["temp_foliar"] = round(18 + (random.random() * 5), 1)
            self.pot["h2o_save"] += 850
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V20, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V20, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V20 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v20 | Thermal SCADA</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #000; --thermal: #ff3300; }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        
        .hud { position: absolute; background: rgba(5, 15, 15, 0.95); border: 2px solid var(--neon); padding: 20px; z-index: 100; box-shadow: 0 0 20px rgba(0,255,204,0.3); }
        #ui-left { top: 20px; left: 20px; width: 330px; }
        #ui-right { top: 20px; right: 20px; width: 290px; }
        
        h2 { font-family: 'Orbitron'; font-size: 13px; color: var(--neon); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; border-bottom: 1px solid #333; }
        .stat { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px; }
        .val { font-weight: 700; color: #fff; }
        
        button { background: var(--neon); color: #000; border: none; padding: 16px; width: 100%; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; margin-top: 10px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 30px var(--neon); }
        
        #thermal-label { position: absolute; bottom: 20px; left: 20px; font-size: 10px; color: var(--thermal); font-family: 'Orbitron'; background: rgba(0,0,0,0.8); padding: 10px; border: 1px solid var(--thermal); display: none; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>CENTRAL CORE | {{ bid }}</h2>
        <div class="stat">ESTADO: <span class="val">{{ "COSECHA" if d == 7 else "MODO INSPECCIÓN" if d > 0 else "VISTA GLOBAL" }}</span></div>
        <div class="stat">DÍA DE CICLO: <span class="val">{{ d }} / 7</span></div>
        <div class="stat">PESO BANDEJA: <span class="val">{{ inv.peso }} KG</span></div>
        <button onclick="location.href='/next'">{{ "SIGUIENTE FASE" if d < 7 else "REINICIAR" }}</button>
        <button style="background:#111; color:#444; font-size:9px; margin-top:5px;" onclick="location.href='/?reset=1'">FORZAR REINICIO</button>
    </div>

    <div id="ui-right" class="hud">
        <h2>DATA STREAM</h2>
        <div class="stat">CRECIMIENTO: <span class="val">{{ inv.crecimiento }} CM</span></div>
        <div class="stat">TEMP. FOLIAR: <span class="val">{{ inv.temp_foliar }} °C</span></div>
        <div class="stat">AHORRO H2O: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">NDVI VIGOR: <span class="val">{{ pot.ndvi }}</span></div>
    </div>

    <div id="thermal-label">CAMERA: FLIR-V20 | THERMAL FEED ACTIVE</div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1500);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ILUMINACIÓN ---
        scene.add(new THREE.AmbientLight(0xffffff, 0.4));
        const sun = new THREE.PointLight(0x00ffcc, 1.5, 200);
        sun.position.set(20, 40, 20);
        scene.add(sun);

        // --- TORRE SCADA ---
        const towerGroup = new THREE.Group();
        const metalMat = new THREE.MeshStandardMaterial({color: 0x222222, metalness: 1, roughness: 0.1});
        
        // Vigas Maestro
        for(let x of [-3.5, 3.5]) {
            for(let z of [-3.5, 3.5]) {
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.4, 30, 0.4), metalMat);
                beam.position.set(x, 5, z);
                towerGroup.add(beam);
                const neon = new THREE.Mesh(new THREE.BoxGeometry(0.05, 30.1, 0.05), new THREE.MeshBasicMaterial({color: 0x00ffcc}));
                neon.position.set(x, 5, z);
                towerGroup.add(neon);
            }
        }

        const trays = [];
        for(let i=0; i<10; i++){
            const h = i * 2.8 - 8;
            const floorGroup = new THREE.Group();
            
            // Bandeja con sensor de carga
            const tray = new THREE.Mesh(new THREE.BoxGeometry(6.6, 0.2, 6.6), metalMat);
            tray.position.y = h;
            floorGroup.add(tray);

            // Forraje con Termografía (Shader Simple)
            const gH = ({{ d }} * 0.35) + 0.1;
            let thermalColor = new THREE.Color(0x00ff44); // Verde normal
            if({{ d }} > 0 && i == {{ d }}) {
                thermalColor = new THREE.Color().setHSL(0.3 - ({{inv.temp_foliar}} - 18)*0.05, 1, 0.5);
            }
            
            const grass = new THREE.Mesh(new THREE.BoxGeometry(6.2, gH, 6.2), new THREE.MeshStandardMaterial({color: thermalColor, emissive: thermalColor, emissiveIntensity: 0.2}));
            grass.position.y = h + gH/2;
            floorGroup.add(grass);

            towerGroup.add(floorGroup);
            trays.push(h);
        }
        scene.add(towerGroup);

        // --- LOGÍSTICA (BANDA Y ANIMAL) ---
        const logistics = new THREE.Group();
        const belt = new THREE.Mesh(new THREE.BoxGeometry(40, 0.5, 5), new THREE.MeshStandardMaterial({color: 0x111111}));
        belt.position.set(25, -10, 0);
        
        // Rodillos de banda
        for(let r=0; r<15; r++){
            const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.2,0.2,5.2), metalMat);
            rod.rotation.z = Math.PI/2;
            rod.position.set(8 + r*2.5, -9.7, 0);
            logistics.add(rod);
        }

        const harvestTray = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.3, 3.5), new THREE.MeshStandardMaterial({color: 0x00ff44}));
        harvestTray.position.set(5, -9.5, 0);
        harvestTray.visible = ({{ d }} == 7);
        
        // Animal (Vaca Estilo Low Poly Industrial)
        const animal = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CapsuleGeometry(1, 2.5, 8, 16), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        body.rotation.z = Math.PI/2;
        const head = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1.2), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        head.position.set(2.2, 0.8, 0);
        animal.add(body, head);
        animal.position.set(45, -8.5, 0);

        logistics.add(belt, harvestTray, animal);
        scene.add(logistics);

        // --- CÁMARA LOGIC ---
        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now() * 0.001;
            
            if ({{ d }} == 0) {
                // VISTA GLOBAL AL INICIO
                camera.position.lerp(new THREE.Vector3(40, 20, 40), 0.03);
                camera.lookAt(0, 0, 0);
                document.getElementById('thermal-label').style.display = 'none';
            } else if ({{ d }} < 7) {
                // ZOOM A BANDEJA ESPECÍFICA
                const ty = trays[{{ d }}];
                camera.position.lerp(new THREE.Vector3(-12, ty + 4, 12), 0.05);
                camera.lookAt(0, ty, 0);
                document.getElementById('thermal-label').style.display = 'block';
            } else {
                // VISTA DE COSECHA
                camera.position.lerp(new THREE.Vector3(55, 15, 20), 0.02);
                camera.lookAt(30, -5, 0);
                if(harvestTray.position.x < 42) harvestTray.position.x += 0.2;
                head.rotation.x = Math.sin(t*8)*0.2;
            }

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
