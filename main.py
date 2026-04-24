import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)

class MotorNova:
    def __init__(self):
        self.lote = "BATCH-ULTRA-3D"
        self.dia = 0
        self.altura = 0
        self.proteina = 0
        self.co2 = 0
        self.energia = 0
        self.status = "SISTEMA OPERATIVO"

    def ciclo(self):
        self.dia = (self.dia + 1) if self.dia < 7 else 0
        self.altura = self.dia * 35.7
        self.proteina = 15 + (self.dia * 1.2)
        self.co2 = self.dia * 0.72
        self.energia += random.uniform(5, 10)
        
        estados = [
            "DIA 0: ACTIVACIÓN MINERAL", "DIA 1: GERMINACIÓN", "DIA 2: ANCLAJE RADICULAR",
            "DIA 3: FOTOSÍNTESIS LED", "DIA 4: BIO-INYECCIÓN NEEM/AJO", 
            "DIA 5: CRECIMIENTO ACELERADO", "DIA 6: MADURACIÓN", "DIA 7: COSECHA ROBOTIZADA"
        ]
        self.status = estados[self.dia]

nova = MotorNova()

HTML_BRUTAL = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA INDUSTRIAL SIMULATOR</title>
    <style>
        body { margin: 0; background: #000; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        #overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;
                   border: 20px solid rgba(0, 255, 0, 0.1); box-sizing: border-box; }
        #ui-panel { position: absolute; top: 30px; left: 30px; z-index: 10; background: rgba(0, 20, 0, 0.85); 
                    padding: 25px; border: 2px solid #00ff00; border-radius: 5px; color: #0f0; width: 320px; }
        .data-line { display: flex; justify-content: space-between; margin: 8px 0; border-bottom: 1px solid #004400; }
        .biotech-glow { color: #f1c40f; text-shadow: 0 0 10px #f1c40f; font-weight: bold; }
        button { pointer-events: auto; background: #00ff00; color: #000; border: none; padding: 10px; cursor: pointer; width: 100%; font-weight: bold; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="overlay"></div>
    <div id="ui-panel">
        <h2 style="margin-top:0">🛰️ N.O.V.A. CORE v7.0</h2>
        <div class="data-line"><span>LOTE ID:</span> <span>{{ lote }}</span></div>
        <div class="data-line"><span>ESTADO:</span> <span class="biotech-glow">{{ status }}</span></div>
        <div class="data-line"><span>DÍA DE CICLO:</span> <span>{{ dia }} / 7</span></div>
        <div class="data-line"><span>ALTURA FORRAJE:</span> <span>{{ altura }} mm</span></div>
        <div class="data-line"><span>PROTEÍNA BRUTA:</span> <span>{{ proteina }}%</span></div>
        <div class="data-line"><span>CAPTURA CO2:</span> <span>{{ co2 }} kg</span></div>
        <div class="data-line"><span>ENERGÍA SOLAR:</span> <span>{{ energia }} kWh</span></div>
        <br>
        <button onclick="location.reload()">AVANZAR CICLO DE TIEMPO</button>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ESTRUCTURA DEL INVERNADERO (FRAME) ---
        const frameGeo = new THREE.BoxGeometry(6, 15, 6);
        const frameMat = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true, transparent: true, opacity: 0.1 });
        const warehouse = new THREE.Mesh(frameGeo, frameMat);
        scene.add(warehouse);

        // --- PISOS Y BANDEJAS ---
        const floors = [];
        for(let i = 0; i < 10; i++) {
            const floorGroup = new THREE.Group();
            
            // Piso metálico
            const pGeo = new THREE.BoxGeometry(5, 0.1, 5);
            const pMat = new THREE.MeshPhongMaterial({ color: 0x222222, shininess: 100 });
            const floor = new THREE.Mesh(pGeo, pMat);
            floor.position.y = i * 1.4 - 6.5;
            floorGroup.add(floor);

            // Luces LED (Día 3 en adelante)
            if ({{ dia }} >= 3) {
                const ledGeo = new THREE.PlaneGeometry(4.8, 0.2);
                const ledMat = new THREE.MeshBasicMaterial({ color: 0xff00ff, side: THREE.DoubleSide });
                const led = new THREE.Mesh(ledGeo, ledMat);
                led.position.y = floor.position.y + 1.2;
                led.rotation.x = Math.PI / 2;
                floorGroup.add(led);
            }

            // Forraje (Crecimiento Dinámico)
            if (i <= {{ dia }} + 2) {
                const grassGeo = new THREE.BoxGeometry(4.5, ({{ dia }} * 0.1) + 0.1, 4.5);
                const grassMat = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
                const grass = new THREE.Mesh(grassGeo, grassMat);
                grass.position.y = floor.position.y + 0.1;
                floorGroup.add(grass);
            }

            scene.add(floorGroup);
            floors.push(floorGroup);
        }

        // --- ROBOT STACKER (MOVIMIENTO) ---
        const robotGeo = new THREE.BoxGeometry(1, 0.5, 2);
        const robotMat = new THREE.MeshPhongMaterial({ color: 0xf1c40f });
        const robot = new THREE.Mesh(robotGeo, robotMat);
        robot.position.set(-2.5, ({{ dia }} * 1.4 - 6.5), 0);
        scene.add(robot);

        // --- PANELES SOLARES ---
        const solarGeo = new THREE.BoxGeometry(7, 0.2, 7);
        const solarMat = new THREE.MeshPhongMaterial({ color: 0x001133 });
        const solar = new THREE.Mesh(solarGeo, solarMat);
        solar.position.y = 8;
        scene.add(solar);

        // --- LUZ ---
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(5, 10, 7.5);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        camera.position.set(12, 5, 12);
        camera.lookAt(0, 0, 0);

        function animate() {
            requestAnimationFrame(animate);
            scene.rotation.y += 0.002; // Rotación lenta para inspección
            robot.position.y = Math.sin(Date.now() * 0.001) * 7; // El robot "escanea" los pisos
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    nova.ciclo()
    return render_template_string(HTML_BRUTAL, 
                                 lote=nova.lote, 
                                 dia=nova.dia, 
                                 status=nova.status,
                                 altura=round(nova.altura, 2), 
                                 proteina=round(nova.proteina, 2), 
                                 co2=round(nova.co2, 2), 
                                 energia=round(nova.energia, 2))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)