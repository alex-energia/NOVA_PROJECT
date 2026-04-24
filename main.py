import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)

class MotorNova:
    def __init__(self):
        self.lote = "NOVA-CORE-V8"
        self.dia = 0
        self.altura = 0
        self.status = "SISTEMA OPERATIVO"
        self.energia_acumulada = 0

    def ciclo(self):
        self.dia = (self.dia + 1) if self.dia < 7 else 0
        self.altura = self.dia * 35.7
        self.energia_acumulada += random.uniform(8.5, 12.0)
        
        estados = [
            "DÍA 0: ACTIVACIÓN", "DÍA 1: GERMINACIÓN", "DÍA 2: RAÍZ",
            "DÍA 3: FOTOSÍNTESIS", "DÍA 4: BIO-DEFENSA", "DÍA 5: BIOMASA",
            "DÍA 6: MADURACIÓN", "DÍA 7: DESPACHO"
        ]
        self.status = estados[self.dia]

nova = MotorNova()

HTML_V8 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA INSTRUMENTACIÓN 3D</title>
    <style>
        body { margin: 0; background: #000; overflow: hidden; font-family: 'Courier New', monospace; }
        #ui-layer { position: absolute; top: 20px; left: 20px; z-index: 100; background: rgba(0,25,0,0.9); 
                    padding: 20px; border: 1px solid #00ff00; color: #00ff00; width: 350px; }
        .sensor-read { display: flex; justify-content: space-between; font-size: 13px; margin: 4px 0; }
        .solar-tag { color: #f1c40f; font-weight: bold; }
        button { background: #00ff00; color: #000; border: none; padding: 12px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 15px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-layer">
        <h2 style="margin:0">🛰️ N.O.V.A. CORE v8.0</h2>
        <div class="sensor-read"><span>ESTADO ACTUAL:</span> <span style="color:white">{{ status }}</span></div>
        <div class="sensor-read"><span>DÍA DE CICLO:</span> <span>{{ dia }}/7</span></div>
        <div class="sensor-read"><span>ALTURA FORRAJE:</span> <span>{{ altura }} mm</span></div>
        <hr>
        <div class="sensor-read"><span class="solar-tag">PANEL SOLAR:</span> <span class="solar-tag">{{ energia }} kWh</span></div>
        <div class="sensor-read"><span>ROBOT STACKER:</span> <span id="robot-status">OPERANDO</span></div>
        <button onclick="location.reload()">SIGUIENTE FASE (SIMULAR DÍA)</button>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- PANELES SOLARES (TECHO) ---
        const solarGroup = new THREE.Group();
        const sGeo = new THREE.BoxGeometry(7, 0.2, 7);
        const sMat = new THREE.MeshPhongMaterial({ color: 0x001133, specular: 0x0099ff });
        const solarPanel = new THREE.Mesh(sGeo, sMat);
        solarPanel.position.y = 8.5;
        solarGroup.add(solarPanel);
        scene.add(solarGroup);

        // --- INVERNADERO Y PISOS COLOREADOS ---
        const floors = [];
        const floorColors = [0x222222, 0x111111, 0x003300, 0x006600, 0x00aa00, 0x00ff00, 0x55ff55, 0xaaffaa];
        
        for(let i=0; i<10; i++) {
            const floorLevel = new THREE.Group();
            
            // Estructura de Piso
            const pGeo = new THREE.BoxGeometry(6, 0.1, 6);
            const pMat = new THREE.MeshPhongMaterial({ 
                color: (i == {{ dia }}) ? floorColors[{{ dia }}] : 0x222222,
                emissive: (i == {{ dia }}) ? 0x002200 : 0x000000
            });
            const floor = new THREE.Mesh(pGeo, pMat);
            floor.position.y = i * 1.5 - 7;
            floorLevel.add(floor);

            // Bandejas con Forraje
            const bGeo = new THREE.BoxGeometry(5, ({{ dia }} * 0.05) + 0.1, 5);
            const bMat = new THREE.MeshPhongMaterial({ color: 0x00aa00 });
            const bandeja = new THREE.Mesh(bGeo, bMat);
            bandeja.position.y = floor.position.y + 0.1;
            floorLevel.add(bandeja);

            scene.add(floorLevel);
            floors.push(floorLevel);
        }

        // --- ROBOT STACKER (CINEMÁTICA) ---
        const robotGroup = new THREE.Group();
        const bodyGeo = new THREE.BoxGeometry(1.2, 0.6, 1.2);
        const bodyMat = new THREE.MeshPhongMaterial({ color: 0xf1c40f });
        const robotBody = new THREE.Mesh(bodyGeo, bodyMat);
        
        const armGeo = new THREE.BoxGeometry(2, 0.2, 0.2);
        const robotArm = new THREE.Mesh(armGeo, bodyMat);
        robotArm.position.x = 1.2;
        
        robotGroup.add(robotBody);
        robotGroup.add(robotArm);
        scene.add(robotGroup);

        // --- ILUMINACIÓN ---
        const light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(10, 10, 10);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        camera.position.set(15, 8, 15);
        camera.lookAt(0, 0, 0);

        function animate() {
            requestAnimationFrame(animate);
            
            // Movimiento del Robot entre niveles
            const targetY = ({{ dia }} * 1.5 - 6.8);
            robotGroup.position.y += (targetY - robotGroup.position.y) * 0.05;
            robotGroup.position.x = -3.5;
            robotGroup.rotation.y += 0.01;

            scene.rotation.y += 0.002;
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
    return render_template_string(HTML_V8, lote=nova.lote, dia=nova.dia, 
                                 status=nova.status, altura=round(nova.altura, 2), 
                                 energia=round(nova.energia_acumulada, 2))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
