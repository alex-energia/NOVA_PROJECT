import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)

class MotorNova:
    def __init__(self):
        self.lote = "NOVA-ECO-3D"
        self.dia = 0
        self.altura = 0
        self.proteina = 0
        self.co2_invernadero = 0
        self.co2_potrero = 0
        self.status = "SISTEMA OPERATIVO"

    def ciclo(self):
        self.dia = (self.dia + 1) if self.dia < 7 else 0
        self.altura = self.dia * 36
        self.proteina = 14 + (self.dia * 1.2)
        self.co2_invernadero = self.dia * 0.8
        self.co2_potrero = self.dia * 2.5 # Captura masiva en suelo
        
        estados = ["DIA 0: CARGA", "DIA 1: GERMINACIÓN", "DIA 2: RAÍCES", "DIA 3: LED ON", 
                   "DIA 4: BIO-DEFENSA", "DIA 5: BIOMASA", "DIA 6: NUTRICIÓN", "DIA 7: DESPACHO"]
        self.status = estados[self.dia]

nova = MotorNova()

HTML_TOTAL = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA TOTAL ECOSYSTEM</title>
    <style>
        body { margin: 0; background: #000; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
        #ui { position: absolute; top: 20px; left: 20px; z-index: 100; background: rgba(0,20,0,0.9); 
              padding: 20px; border: 2px solid #00ff00; color: #0f0; border-radius: 10px; width: 300px; }
        .stat { display: flex; justify-content: space-between; margin: 5px 0; font-size: 14px; }
        .eco-label { color: #2ecc71; font-weight: bold; text-align: center; display: block; margin-top: 10px; }
        button { background: #00ff00; border: none; padding: 10px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui">
        <h2 style="margin:0">🛰️ N.O.V.A. ECO-SIM</h2>
        <div class="stat"><span>ESTADO:</span> <span>{{ status }}</span></div>
        <div class="stat"><span>DÍA:</span> <span>{{ dia }}/7</span></div>
        <div class="stat"><span>H<sub>2</sub>O NEBULIZADA:</span> <span>ACTIVA</span></div>
        <hr>
        <div class="stat"><span>CAPTURA INV:</span> <span>{{ co2_inv }} kg</span></div>
        <div class="stat"><span>CAPTURA SUELO:</span> <span>{{ co2_pot }} kg</span></div>
        <span class="eco-label">CARBONO NEGATIVO ✅</span>
        <button onclick="location.reload()">SIGUIENTE FASE</button>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- POTRERO (FIELD-LINK) ---
        const groundGeo = new THREE.PlaneGeometry(100, 100);
        const groundMat = new THREE.MeshPhongMaterial({ color: 0x0a2a0a });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.rotation.x = -Math.PI/2;
        ground.position.y = -7;
        scene.add(ground);

        // --- INVERNADERO (GREEN-CORE) ---
        const invGroup = new THREE.Group();
        const frameGeo = new THREE.BoxGeometry(8, 16, 8);
        const frameMat = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true, transparent: true, opacity: 0.2 });
        const frame = new THREE.Mesh(frameGeo, frameMat);
        invGroup.add(frame);

        // --- PISOS Y LLUVIA ---
        const rainParticles = [];
        for(let i=0; i<10; i++) {
            // Bandejas
            const bGeo = new THREE.BoxGeometry(6, 0.1, 6);
            const bMat = new THREE.MeshPhongMaterial({ color: 0x222222 });
            const bandeja = new THREE.Mesh(bGeo, bMat);
            bandeja.position.y = i * 1.5 - 7;
            invGroup.add(bandeja);

            // Gotas de lluvia (partículas)
            for(let j=0; j<20; j++) {
                const dropGeo = new THREE.SphereGeometry(0.02);
                const dropMat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
                const drop = new THREE.Mesh(dropGeo, dropMat);
                drop.position.set(Math.random()*5-2.5, bandeja.position.y + 1, Math.random()*5-2.5);
                scene.add(drop);
                rainParticles.push(drop);
            }
        }
        scene.add(invGroup);

        // --- ANIMALES (MIMIC) ---
        const cowGeo = new THREE.BoxGeometry(2, 1.5, 1);
        const cowMat = new THREE.MeshPhongMaterial({ color: 0x4b2c20 });
        const cow = new THREE.Mesh(cowGeo, cowMat);
        cow.position.set(15, -6.2, 10);
        scene.add(cow);

        // Luces
        const sun = new THREE.DirectionalLight(0xffffff, 1.2);
        sun.position.set(20, 30, 10);
        scene.add(sun);
        scene.add(new THREE.AmbientLight(0x404040));

        camera.position.set(25, 10, 25);
        camera.lookAt(0, 0, 0);

        function animate() {
            requestAnimationFrame(animate);
            
            // Animación Lluvia
            rainParticles.forEach(p => {
                p.position.y -= 0.05;
                if(p.position.y < -7) p.position.y = 8;
            });

            scene.rotation.y += 0.001;
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
    return render_template_string(HTML_TOTAL, lote=nova.lote, dia=nova.dia, status=nova.status,
                                 co2_inv=nova.co2_invernadero, co2_pot=nova.co2_potrero)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)