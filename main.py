import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-X-{random.randint(100,999)}"
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "par": 0, "tanque": 100,
            "presion": 45.2, "mg": 15, "k": 20, "ca": 12
        }
        self.pot = {
            "hum": 22.4, "ndvi": 0.65, "ch4": 0, "h2o_save": 0, "carbono": 142.5
        }
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg", "Bio": "2kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["par"] = random.randint(300, 600)
            self.pot["h2o_save"] += 800
            self.pot["ch4"] += 2.5
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
    <title>NOVA v16 | Deep Inspection</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #050505; --panel: rgba(10, 10, 10, 0.9); }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: var(--panel); border: 1px solid rgba(0, 255, 204, 0.3); 
               padding: 20px; backdrop-filter: blur(15px); border-radius: 8px; z-index: 100; }
        #ui-left { top: 20px; left: 20px; width: 330px; }
        #ui-right { top: 20px; right: 20px; width: 300px; }
        h2 { font-size: 11px; color: var(--neon); letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; border-bottom: 1px solid #333; }
        .stat { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px; }
        .val { font-weight: 700; color: #fff; }
        button { background: var(--neon); color: #000; border: none; padding: 12px; width: 100%; border-radius: 4px; 
                 font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: 10px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>CENTRAL CONTROL | {{ bid }}</h2>
        <div class="stat">DÍA DE CICLO: <span class="val">{{ d }} / 7</span></div>
        <hr style="opacity:0.1">
        {% if d == 0 %}
            <div style="color: #f1c40f; font-size: 10px; margin-bottom:10px;">ESTADO: CARGA DE SEMILLAS</div>
            {% for k,v in rec.items() %}<div class="stat">{{k}}: <span class="val">{{v}}</span></div>{% endfor %}
        {% else %}
            <div style="color: var(--neon); font-size: 10px; margin-bottom:10px;">ESTADO: CRECIMIENTO ACTIVO</div>
            <div class="stat">ALTURA: <span class="val">{{ d * 4.3 }} cm</span></div>
        {% endif %}
        <button onclick="location.href='/next'">AVANZAR CICLO</button>
        <button style="background:#222; color:#888; font-size:9px; margin-top:5px;" onclick="location.href='/?reset=1'">REINICIAR SISTEMA</button>
    </div>

    <div id="ui-right" class="hud">
        <h2>TELEMETRÍA INVERNADERO</h2>
        <div class="stat">PH / CE: <span class="val">{{ inv.ph }} / {{ inv.ce }}</span></div>
        <div class="stat">CO2 / PAR: <span class="val">{{ inv.co2 }} / {{ inv.par }}</span></div>
        <div class="stat">Mg / K / Ca: <span class="val">{{ inv.mg }}/{{ inv.k }}/{{ inv.ca }}</span></div>
        <hr style="opacity:0.1">
        <h2>FIELD-LINK (POTRERO)</h2>
        <div class="stat">AHORRO H2O: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">CH4 REDUCIDO: <span class="val">{{ pot.ch4 }} kg</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ENTORNO ---
        const grid = new THREE.GridHelper(100, 50, 0x00ffcc, 0x111111);
        grid.position.y = -8;
        scene.add(grid);

        // --- ESTRUCTURA DE LA TORRE (SOLUCIÓN A "NO SE VE") ---
        const towerStructure = new THREE.Group();
        const frameMat = new THREE.MeshStandardMaterial({color: 0x333333, metalness: 1});
        
        // Columnas de la torre
        for(let x of [-3.2, 3.2]) {
            for(let z of [-3.2, 3.2]) {
                const col = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 20), frameMat);
                col.position.set(x, 2, z);
                towerStructure.add(col);
            }
        }

        // Pisos y Forraje
        for(let i=0; i<10; i++){
            const floorH = i * 2 - 8;
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), new THREE.MeshStandardMaterial({color: 0x1a1a1a}));
            floor.position.y = floorH;
            towerStructure.add(floor);

            // Forraje dinámico
            const hGrass = ({{ d }} * 0.25) + 0.05;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(5.8, hGrass, 5.8), 
                          new THREE.MeshStandardMaterial({color: ({{d}} == 0 ? 0x4d3319 : 0x00ff44)}));
            grass.position.y = floorH + hGrass/2;
            towerStructure.add(grass);
        }
        scene.add(towerStructure);

        // --- ANIMAL ORGÁNICO ---
        const cow = new THREE.Group();
        const cowBody = new THREE.Mesh(new THREE.CapsuleGeometry(0.8, 2, 8, 16), new THREE.MeshStandardMaterial({color: 0x4b2c20}));
        cowBody.rotation.z = Math.PI/2;
        const cowHead = new THREE.Mesh(new THREE.SphereGeometry(0.6, 16, 16), new THREE.MeshStandardMaterial({color: 0x4b2c20}));
        cowHead.position.set(1.8, 0.6, 0);
        cow.add(cowBody, cowHead);
        cow.position.set(30, -7, 0);
        scene.add(cow);

        // --- BANDA Y BANDEJA ---
        const belt = new THREE.Mesh(new THREE.BoxGeometry(25, 0.2, 3), new THREE.MeshStandardMaterial({color: 0x222222}));
        belt.position.set(15, -7.9, 0);
        scene.add(belt);

        const tray = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.15, 2.5), new THREE.MeshStandardMaterial({color: 0x00ff44}));
        tray.position.set(5, -7.7, 0);
        tray.visible = ({{ d }} == 7);
        scene.add(tray);

        // --- LUCES ---
        const sun = new THREE.DirectionalLight(0xffffff, 1.5);
        sun.position.set(10, 20, 10);
        scene.add(sun, new THREE.AmbientLight(0x404040, 1.2));

        camera.position.set(25, 10, 25);

        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now() * 0.001;

            if ({{ d }} < 7) {
                const targetH = ({{ d }} * 2 - 8);
                // Zoom de inspección
                camera.position.lerp(new THREE.Vector3(-12, targetH + 3, 10), 0.05);
                camera.lookAt(0, targetH, 0);
            } else {
                // Día 7: Cosecha
                camera.position.lerp(new THREE.Vector3(35, 15, 35), 0.03);
                camera.lookAt(15, -5, 0);
                if(tray.position.x < 30) tray.position.x += 0.2;
                if(cow.position.x > 31) cow.position.x -= 0.1;
                cowHead.rotation.x = Math.sin(t * 6) * 0.2;
            }
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>