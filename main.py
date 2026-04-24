import datetime
import random
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

class SistemaCentralNOVA:
    def __init__(self):
        self.nodos = 25
        self.nodo_activo = 1
        self.dia_ciclo = 0
        self.presion_hidraulica = 45.5 # PSI
        self.flujo_nutrientes = 1.2 # L/min
        self.batch_id = "B-PRO-001"
        
    def procesar(self):
        self.dia_ciclo = (self.dia_ciclo + 1) if self.dia_ciclo < 7 else 0
        self.presion_hidraulica = round(random.uniform(42.0, 48.0), 1)
        self.flujo_nutrientes = round(random.uniform(1.0, 1.5), 2)

nova_system = SistemaCentralNOVA()

HTML_ENTERPRISE = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Enterprise Control</title>
    <style>
        :root { --main-color: #00ffcc; --bg-dark: #050505; }
        body { margin: 0; background: var(--bg-dark); color: var(--main-color); font-family: 'Inter', sans-serif; overflow: hidden; }
        #overlay-ui { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
        .panel { position: absolute; background: rgba(10, 10, 10, 0.85); border: 1px solid var(--main-color); 
                  backdrop-filter: blur(15px); padding: 20px; pointer-events: auto; }
        #left-panel { top: 20px; left: 20px; width: 320px; }
        #bottom-panel { bottom: 20px; left: 50%; transform: translateX(-50%); width: 80%; height: 60px; display: flex; align-items: center; justify-content: space-around; }
        .node-dot { width: 10px; height: 10px; border-radius: 50%; background: #222; }
        .node-active { background: var(--main-color); box-shadow: 0 0 10px var(--main-color); }
        h2 { font-size: 14px; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 15px 0; opacity: 0.8; }
        .value { color: white; font-weight: bold; float: right; }
        button { background: var(--main-color); color: black; border: none; padding: 10px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; transition: 0.3s; }
        button:hover { background: white; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="overlay-ui">
        <div id="left-panel" class="panel">
            <h2>N.O.V.A. Mission Control</h2>
            <div>BATCH: <span class="value">{{ batch }}</span></div>
            <div>DÍA DE PROCESO: <span class="value">{{ dia }}/7</span></div>
            <div>PRESIÓN SISTEMA: <span class="value">{{ presion }} PSI</span></div>
            <div>FLUJO NUTRIENTES: <span class="value">{{ flujo }} L/m</span></div>
            <hr style="border: 0.5px solid #222; margin: 15px 0;">
            <div style="font-size: 11px; color: #f1c40f;">BIOTECH STATUS: {{ "INYECCIÓN SISTÉMICA ACTIVA" if dia == 4 else "MONITOREO DE BIOMASA" }}</div>
            <button onclick="location.reload()">FORZAR CICLO TELEMETRÍA</button>
        </div>
        
        <div id="bottom-panel" class="panel">
            {% for i in range(1, 26) %}
                <div class="node-dot {{ 'node-active' if i == 1 else '' }}"></div>
            {% endfor %}
            <span style="font-size: 10px; opacity: 0.5;">MULTI-NODE FLEET MANAGEMENT (25 UNITS)</span>
        </div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        document.body.appendChild(renderer.domElement);

        // --- ILUMINACIÓN CINEMATOGRÁFICA ---
        const ambLight = new THREE.AmbientLight(0x404040, 0.5);
        scene.add(ambLight);
        const pointLight = new THREE.PointLight(0x00ffcc, 1.5);
        pointLight.position.set(10, 10, 10);
        scene.add(pointLight);

        // --- CONSTRUCCIÓN DEL CORE INDUSTRIAL ---
        const greenhouse = new THREE.Group();
        
        // Estructura de Columnas (Ingeniería)
        const colGeo = new THREE.CylinderGeometry(0.05, 0.05, 18);
        const colMat = new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 1 });
        for(let x of [-3.5, 3.5]) {
            for(let z of [-3.5, 3.5]) {
                const col = new THREE.Mesh(colGeo, colMat);
                col.position.set(x, 0, z);
                greenhouse.add(col);
            }
        }

        // Pisos de Rejilla Metálica
        for(let i=0; i<10; i++) {
            const fGeo = new THREE.BoxGeometry(7, 0.1, 7);
            const fMat = new THREE.MeshStandardMaterial({ 
                color: (i == {{ dia }}) ? 0x00ffcc : 0x111111,
                transparent: true, opacity: 0.9, metalness: 0.8
            });
            const floor = new THREE.Mesh(fGeo, fMat);
            floor.position.y = i * 1.8 - 8;
            greenhouse.add(floor);
        }
        scene.add(greenhouse);

        // --- ROBOT STACKER ARTICULADO ---
        const robot = new THREE.Group();
        const chassis = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.8, 2), new THREE.MeshStandardMaterial({color: 0x111111, metalness: 1}));
        const laser = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 10), new THREE.MeshBasicMaterial({color: 0xff0000, transparent: true, opacity: 0.3}));
        laser.rotation.z = Math.PI/2;
        laser.position.x = 5;
        robot.add(chassis, laser);
        scene.add(robot);

        camera.position.set(22, 10, 22);
        camera.lookAt(0, 0, 0);

        function animate() {
            requestAnimationFrame(animate);
            const targetY = ({{ dia }} * 1.8 - 8);
            robot.position.y += (targetY - robot.position.y) * 0.05;
            robot.position.x = -5;
            
            greenhouse.rotation.y += 0.002;
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    nova_system.procesar()
    return render_template_string(HTML_ENTERPRISE, 
                                 batch=nova_system.batch_id, 
                                 dia=nova_system.dia_cycle, 
                                 presion=nova_system.presion_hidraulica, 
                                 flujo=nova_system.flujo_nutrientes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
