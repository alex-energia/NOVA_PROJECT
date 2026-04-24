import random
from flask import Flask, render_template_string

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.dia = 0
        self.lote = "NOVA-INSTR-001"
        # Variables de Instrumentación Invernadero
        self.sensores = {
            "caudal": 1.2, "ph": 5.8, "ce": 1.8, "hum_aire": 85,
            "lux": 12000, "co2_ppm": 450, "temp_agua": 18.5
        }
        # Variables de Instrumentación Potrero
        self.campo = {
            "hum_suelo": 22.1, "nitratos": 14.2, "carbono": 142.8
        }
        self.receta = {"Maiz": 105, "Cebada": 15, "Quelatos": 2}

    def update(self):
        self.dia = (self.dia + 1) if self.dia < 7 else 0
        self.sensores["caudal"] = round(random.uniform(1.1, 1.4), 2)
        self.sensores["co2_ppm"] = random.randint(400, 600)
        self.campo["hum_suelo"] += random.uniform(-0.5, 0.5)

control = ControladorNOVA()

HTML_INSTR = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Real-Time Instrumentation</title>
    <style>
        :root { --neon: #00ffcc; --dark: #020202; --panel: rgba(10,10,10,0.9); }
        body { margin: 0; background: var(--dark); color: var(--neon); font-family: 'Orbitron', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: var(--panel); border: 1px solid var(--neon); padding: 15px; backdrop-filter: blur(10px); z-index: 100; pointer-events: auto; }
        #control-panel { top: 20px; left: 20px; width: 340px; }
        #sensor-grid { top: 20px; right: 20px; width: 300px; }
        .data-box { border-left: 3px solid var(--neon); padding-left: 10px; margin: 10px 0; }
        .val { color: white; float: right; }
        .active-cycle { background: rgba(0, 255, 204, 0.2); border: 1px solid var(--neon); padding: 5px; }
        button { background: var(--neon); color: black; border: none; padding: 12px; width: 100%; font-weight: 900; cursor: pointer; font-family: 'Orbitron'; }
        h3 { font-size: 14px; margin: 0 0 10px 0; border-bottom: 1px solid #333; padding-bottom: 5px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
</head>
<body>
    <div id="control-panel" class="hud">
        <h3>DASHBOARD PRINCIPAL</h3>
        <div class="data-box active-cycle">CICLO ACTUAL: <span class="val">DÍA {{ dia }}</span></div>
        
        {% if dia == 0 %}
        <h3>📦 LOGÍSTICA DE CARGA</h3>
        {% for k, v in receta.items() %}
        <div class="data-box">{{ k }}: <span class="val">{{ v }} kg</span></div>
        {% endfor %}
        {% elif dia == 7 %}
        <h3 style="color:#f1c40f">🚚 FASE DE DESPACHO</h3>
        <div class="data-box">ESTADO: <span class="val">BANDA ACTIVA</span></div>
        {% else %}
        <h3>🧬 BIOTECNOLOGÍA</h3>
        <div class="data-box">ESTADO: <span class="val">CRECIMIENTO</span></div>
        <div class="data-box">SUPLEMENTO: <span class="val">{{ 'NEEM/AJO' if dia == 4 else 'NPK BASE' }}</span></div>
        {% endif %}
        
        <button onclick="window.location.href='/'">AVANZAR CICLO</button>
    </div>

    <div id="sensor-grid" class="hud">
        <h3>TELEMETRÍA REAL</h3>
        <div class="data-box">PH AGUA: <span class="val">{{ s.ph }}</span></div>
        <div class="data-box">COND. ELÉC: <span class="val">{{ s.ce }} mS</span></div>
        <div class="data-box">CAUDAL: <span class="val">{{ s.caudal }} L/min</span></div>
        <div class="data-box">CO2: <span class="val">{{ s.co2_ppm }} PPM</span></div>
        <hr>
        <h3>FIELD-LINK (POTRERO)</h3>
        <div class="data-box">HUM. SUELO: <span class="val">{{ c.hum_suelo|round(1) }}%</span></div>
        <div class="data-box">CARBONO: <span class="val">{{ c.carbono }} T</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- INVERNADERO ---
        const tower = new THREE.Group();
        for(let i=0; i<10; i++) {
            const is_active = (i == {{ dia }});
            const floorMat = new THREE.MeshStandardMaterial({
                color: is_active ? 0x00ffcc : 0x111111,
                emissive: is_active ? 0x00ffcc : 0x000000,
                emissiveIntensity: is_active ? 0.5 : 0
            });
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), floorMat);
            floor.position.y = i * 1.6 - 7;
            tower.add(floor);
            
            // Tuberías
            const pipe = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 6), new THREE.MeshStandardMaterial({color:0x888888}));
            pipe.rotation.z = Math.PI/2;
            pipe.position.set(0, floor.position.y + 1.2, -2.8);
            tower.add(pipe);
        }
        scene.add(tower);

        // --- ANIMAL MEJORADO ---
        const cow = new THREE.Group();
        const body = new THREE.Mesh(new THREE.BoxGeometry(3.5, 2.2, 1.8), new THREE.MeshStandardMaterial({color: 0x4b2c20}));
        const head = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.2, 1.2), new THREE.MeshStandardMaterial({color: 0x4b2c20}));
        head.position.set(2, 1, 0);
        const legGeo = new THREE.CylinderGeometry(0.2, 0.15, 1.5);
        for(let x of [-1, 1]) for(let z of [-0.5, 0.5]) {
            const leg = new THREE.Mesh(legGeo, new THREE.MeshStandardMaterial({color:0x222222}));
            leg.position.set(x*1.2, -1.5, z);
            body.add(leg);
        }
        cow.add(body, head);
        cow.position.set(25, -6, 0);
        scene.add(cow);

        // --- ROBOT STACKER ---
        const robot = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.8, 1.5), new THREE.MeshStandardMaterial({color: 0xf1c40f}));
        scene.add(robot);

        // Luces
        const light = new THREE.PointLight(0xffffff, 1.5); light.position.set(10, 20, 10);
        scene.add(light, new THREE.AmbientLight(0x404040));
        camera.position.set(28, 12, 28); camera.lookAt(0, 0, 0);

        function animate() {
            requestAnimationFrame(animate);
            // Cinemática Robot
            robot.position.y = ({{ dia }} * 1.6 - 6.6);
            robot.position.x = -4.5;
            robot.position.z = Math.sin(Date.now()*0.002) * 2.5;

            if ({{ dia }} == 7) {
                cow.position.x += (20 - cow.position.x) * 0.05;
                head.rotation.x = Math.sin(Date.now()*0.01) * 0.3;
            } else {
                scene.rotation.y += 0.001;
                cow.position.x = 25;
            }
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    control.update()
    return render_template_string(HTML_INSTR, dia=control.dia, s=control.sensores, c=control.campo, receta=control.receta)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)