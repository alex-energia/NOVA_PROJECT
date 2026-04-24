import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-X-{random.randint(100,999)}"
        # Telemetría Invernadero
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "par": 0, "tanque": 100,
            "presion": 45.2, "mg": 15, "k": 20, "ca": 12, "hum_foliar": 85
        }
        # Telemetría Potrero
        self.pot = {
            "hum": 22.4, "ndvi": 0.65, "ch4": 0, "h2o_save": 0, 
            "carbono": 142.5, "evapo": 4.1, "nitrogeno": 18.2
        }
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg", "Bio": "2kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["par"] = random.randint(350, 650)
            self.pot["h2o_save"] += 850
            self.pot["ch4"] += 2.8
            self.inv["tanque"] -= 4
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V16, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V16, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V16 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v16 | Digital Twin</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #050505; --panel: rgba(10, 10, 10, 0.95); }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: var(--panel); border: 1px solid rgba(0, 255, 204, 0.3); 
               padding: 20px; backdrop-filter: blur(15px); border-radius: 12px; z-index: 100; }
        #ui-left { top: 20px; left: 20px; width: 340px; }
        #ui-right { top: 20px; right: 20px; width: 300px; }
        h2 { font-size: 12px; color: var(--neon); letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; border-bottom: 1px solid #333; padding-bottom: 5px; }
        .stat { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px; font-weight: 300; }
        .val { font-weight: 700; color: #fff; }
        button { background: var(--neon); color: #000; border: none; padding: 14px; width: 100%; border-radius: 6px; 
                 font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: 10px; transition: 0.3s; }
        button:hover { box-shadow: 0 0 20px var(--neon); }
        .grid-bg { position: absolute; width: 100%; height: 100%; z-index: -1; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>CENTRAL CORE | {{ bid }}</h2>
        <div class="stat">CICLO TEMPORAL: <span class="val">DÍA {{ d }} / 7</span></div>
        <hr style="opacity:0.1">
        {% if d == 0 %}
            <div style="color: #f1c40f; font-size: 11px; margin-bottom:10px; font-weight:900;">[ MODO: CARGA DE INGREDIENTES ]</div>
            {% for k,v in rec.items() %}<div class="stat">{{k}}: <span class="val">{{v}}</span></div>{% endfor %}
        {% else %}
            <div style="color: var(--neon); font-size: 11px; margin-bottom:10px; font-weight:900;">[ MODO: INSPECCIÓN BIOMASA ]</div>
            <div class="stat">ALTURA FORRAJE: <span class="val">{{ (d * 4.28)|round(1) }} cm</span></div>
            <div class="stat">DENSIDAD: <span class="val">{{ d * 14 }}%</span></div>
        {% endif %}
        <button onclick="location.href='/next'">Avanzar Ciclo</button>
        <button style="background:#222; color:#888; font-size:9px; margin-top:8px;" onclick="location.href='/?reset=1'">Reiniciar Sistema</button>
    </div>

    <div id="ui-right" class="hud">
        <h2>TELEMETRÍA AVANZADA</h2>
        <div class="stat">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
        <div class="stat">CO2 / PAR: <span class="val">{{ inv.co2 }} / {{ inv.par }}</span></div>
        <div class="stat">TANQUE / PSI: <span class="val">{{ inv.tanque }}% / {{ inv.presion }}</span></div>
        <div class="stat">HUM. FOLIAR: <span class="val">{{ inv.hum_foliar }}%</span></div>
        <hr style="opacity:0.1">
        <h2>POTRERO (FIELD-LINK)</h2>
        <div class="stat">NDVI VIGOR: <span class="val">{{ pot.ndvi }}</span></div>
        <div class="stat">H2O AHORRADA: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">NITRÓGENO: <span class="val">{{ pot.nitrogeno }} mg/kg</span></div>
        <div class="stat">METANO RED.: <span class="val">{{ pot.ch4 }} kg</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020202);
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ENTORNO ---
        const grid = new THREE.GridHelper(100, 40, 0x00ffcc, 0x111111);
        grid.position.y = -8;
        scene.add(grid);

        // --- TORRE INDUSTRIAL (CON EXOESQUELETO) ---
        const towerGroup = new THREE.Group();
        
        // Vigas de soporte (Columnas)
        const beamMat = new THREE.MeshStandardMaterial({color: 0x333333, metalness: 1, roughness: 0.2});
        for(let x of [-3.1, 3.1]) {
            for(let z of [-3.1, 3.1]) {
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.2, 22, 0.2), beamMat);
                beam.position.set(x, 2, z);
                towerGroup.add(beam);
            }
        }

        // Pisos y Cultivo
        for(let i=0; i<10; i++){
            const h = i * 2.1 - 8;
            const isAt = (i == {{ d }});
            
            // Piso Metálico
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), new THREE.MeshStandardMaterial({color: 0x1a1a1a}));
            floor.position.y = h;
            towerGroup.add(floor);

            // Resaltado de borde
            if(isAt) {
                const border = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.15, 6.2), new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true}));
                border.position.y = h;
                towerGroup.add(border);
            }

            // Forraje Dinámico
            const gH = ({{ d }} * 0.25) + 0.05;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(5.6, gH, 5.6), 
                          new THREE.MeshStandardMaterial({color: ({{d}} == 0 ? 0x443322 : 0x00ff44)}));
            grass.position.y = h + gH/2;
            towerGroup.add(grass);
        }
        scene.add(towerGroup);

        // --- ANIMAL (CUERPO ORGÁNICO) ---
        const cow = new THREE.Group();
        const cBody = new THREE.Mesh(new THREE.CapsuleGeometry(0.8, 2, 8, 16), new THREE.MeshStandardMaterial({color: 0x4b2c20}));
        cBody.rotation.z = Math.PI/2;
        const cHead = new THREE.Mesh(new THREE.SphereGeometry(0.6, 16, 16), new THREE.MeshStandardMaterial({color: 0x4b2c20}));
        cHead.position.set(1.8, 0.6, 0);
        cow.add(cBody, cHead);
        cow.position.set(32, -7, 0);
        scene.add(cow);

        // --- LOGÍSTICA ---
        const belt = new THREE.Mesh(new THREE.BoxGeometry(25, 0.2, 3), new THREE.MeshStandardMaterial({color: 0x222222}));
        belt.position.set(15, -7.9, 0);
        scene.add(belt);

        const tray = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.15, 2.5), new THREE.MeshStandardMaterial({color: 0x00ff44}));
        tray.position.set(5, -7.7, 0);
        tray.visible = ({{ d }} == 7);
        scene.add(tray);

        // --- ILUMINACIÓN ---
        const sun = new THREE.DirectionalLight(0xffffff, 1.5);
        sun.position.set(10, 20, 10);
        scene.add(sun, new THREE.AmbientLight(0x404040, 1.2));

        camera.position.set(25, 10, 25);

        function animate() {
            requestAnimationFrame(animate);
            const time = Date.now() * 0.001;

            if ({{ d }} < 7) {
                const targetY = ({{ d }} * 2.1 - 8);
                // Zoom dinámico al nivel activo
                camera.position.lerp(new THREE.Vector3(-12, targetY + 3, 12), 0.05);
                camera.lookAt(0, targetY, 0);
            } else {
                // Día 7: Cosecha y Despacho
                camera.position.lerp(new THREE.Vector3(38, 12, 38), 0.03);
                camera.lookAt(18, -5, 0);
                if(tray.position.x < 31) tray.position.x += 0.22;
                if(cow.position.x > 32.5) cow.position.x -= 0.12;
                cHead.rotation.x = Math.sin(time * 6) * 0.2; // Comiendo
            }
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
