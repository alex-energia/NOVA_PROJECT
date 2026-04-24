import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)

class MotorNova:
    def __init__(self):
        self.lote = "BATCH-PRO-3D"
        self.dia = 0
        self.altura = 0
        self.proteina = 0
        self.co2 = 0
        self.energia = 0

    def ciclo(self):
        self.dia = (self.dia + 1) if self.dia < 7 else 0
        self.altura = self.dia * 35.7
        self.proteina = 15 + (self.dia * 1.1)
        self.co2 = self.dia * 0.65
        self.energia += random.uniform(5, 8)

nova = MotorNova()

HTML_3D = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA 3D DIGITAL TWIN</title>
    <style>
        body { margin: 0; background: #050505; color: #00ff00; font-family: 'Courier New', Courier, monospace; overflow: hidden; }
        #ui { position: absolute; top: 20px; left: 20px; z-index: 100; background: rgba(0,0,0,0.8); padding: 15px; border: 1px solid #00ff00; }
        #canvas-container { width: 100vw; height: 100vh; }
        .alert { color: #ff0000; animation: blink 0.5s infinite; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui">
        <h1>🛰️ N.O.V.A. CORE 3D</h1>
        <p>Lote: {{ lote }}</p>
        <p>Día de Ciclo: {{ dia }} / 7</p>
        <p>Biomasa: {{ altura }} mm</p>
        <p>Proteína: {{ proteina }}%</p>
        <p>CO2 Mitigado: {{ co2 }} kg</p>
        <p>Energía Solar: {{ energia }} kWh</p>
        {% if dia == 4 %}<p class="alert">⚠️ BIO-INYECCIÓN NEEM/AJO ACTIVA</p>{% endif %}
        <button onclick="location.reload()">ACTUALIZAR SENSORES</button>
    </div>
    <div id="canvas-container"></div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('canvas-container').appendChild(renderer.domElement);

        // --- CONSTRUCCIÓN DEL INVERNADERO (10 PISOS) ---
        const geometry = new THREE.BoxGeometry(4, 0.2, 4);
        for(let i = 0; i < 10; i++) {
            const material = new THREE.MeshPhongMaterial({ 
                color: (i == {{ dia }} + 2) ? 0x00ff00 : 0x333333, 
                transparent: true, opacity: 0.8 
            });
            const shelf = new THREE.Mesh(geometry, material);
            shelf.position.y = i * 1.5 - 5;
            scene.add(shelf);
            
            // Simulación de Bandejas
            const trayGeo = new THREE.BoxGeometry(3.5, 0.1, 3.5);
            const trayMat = new THREE.MeshPhongMaterial({ color: 0x111111 });
            const tray = new THREE.Mesh(trayGeo, trayMat);
            tray.position.y = shelf.position.y + 0.2;
            scene.add(tray);
        }

        // --- PANELES SOLARES (TECHO) ---
        const solarGeo = new THREE.PlaneGeometry(5, 5);
        const solarMat = new THREE.MeshPhongMaterial({ color: 0x003366, side: THREE.DoubleSide });
        const solar = new THREE.Mesh(solarGeo, solarMat);
        solar.rotation.x = Math.PI / 2.5;
        solar.position.y = 10;
        scene.add(solar);

        // Iluminación
        const light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(10, 10, 10);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        camera.position.z = 15;
        camera.position.y = 2;

        function animate() {
            requestAnimationFrame(animate);
            scene.rotation.y += 0.005; // Rotación de cámara para ver todo el modelo
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
    return render_template_string(HTML_3D, 
                                 lote=nova.lote, 
                                 dia=nova.dia, 
                                 altura=round(nova.altura, 2), 
                                 proteina=round(nova.proteina, 2), 
                                 co2=round(nova.co2, 2), 
                                 energia=round(nova.energia, 2))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)