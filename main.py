import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)

class SistemaCentralNOVA:
    def __init__(self):
        self.batch_id = "B-PRO-001"
        self.dia_ciclo = 0
        self.presion_hidraulica = 45.5
        self.nutrientes_L_min = 1.2
        # Trazabilidad de ingredientes (Día 0)
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Alfalfa": "5kg", "Minerales": "2.5kg"}
        # Mediciones Potrero
        self.humedad_suelo = 22.0
        self.carbono_suelo_ton = 142.5

    def procesar(self):
        self.dia_ciclo = (self.dia_ciclo + 1) if self.dia_ciclo < 7 else 0
        self.presion_hidraulica = round(random.uniform(43.0, 47.0), 1)
        self.humedad_suelo += random.uniform(-0.5, 0.5)

nova_system = SistemaCentralNOVA()

HTML_FINAL = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Full Ecosystem Control</title>
    <style>
        :root { --main: #00ffcc; --industrial-gray: #1a1a1a; }
        body { margin: 0; background: #020202; color: var(--main); font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud-panel { position: absolute; background: rgba(0,0,0,0.8); border: 1px solid var(--main); padding: 15px; backdrop-filter: blur(10px); z-index: 10; }
        #left-ui { top: 20px; left: 20px; width: 300px; }
        #right-ui { top: 20px; right: 20px; width: 280px; }
        .ingredient { font-size: 11px; color: #aaa; }
        button { background: var(--main); border: none; padding: 10px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 10px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="left-ui" class="hud-panel">
        <h2 style="margin:0; font-size:14px;">📦 LOGÍSTICA DE CARGA (DÍA 0)</h2>
        <div style="margin:10px 0;">
            {% for ing, cant in receta.items() %}
            <div class="ingredient">{{ ing }}: <span style="color:white">{{ cant }}</span></div>
            {% endfor %}
        </div>
        <hr style="border:0.1px solid #333">
        <div style="font-size:12px;">ESTADO: <span style="color:white">{{ "DESPACHANDO AL COMEDERO" if dia == 7 else "EN CRECIMIENTO" }}</span></div>
        <button onclick="location.reload()">AVANZAR LOGÍSTICA</button>
    </div>

    <div id="right-ui" class="hud-panel">
        <h2 style="margin:0; font-size:14px;">🌱 FIELD-LINK: POTRERO</h2>
        <div style="font-size:12px; margin-top:10px;">HUMEDAD SUELO: <span style="color:white">{{ humedad }}%</span></div>
        <div style="font-size:12px;">C-ORGÁNICO: <span style="color:white">{{ carbono }} TON/HA</span></div>
        <div style="font-size:12px;">ESTADO HATO: <span style="color:#f1c40f;">PROTEGIDO (NEEM/AJO)</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- INVERNADERO ---
        const structure = new THREE.GridHelper(20, 20, 0x00ffcc, 0x002211);
        structure.position.y = -5;
        scene.add(structure);

        for(let i=0; i<10; i++) {
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), new THREE.MeshStandardMaterial({color: (i == {{ dia }}) ? 0x00ffcc : 0x111111}));
            floor.position.y = i * 1.5 - 5;
            scene.add(floor);
        }

        // --- BANDA TRANSPORTADORA AL COMEDERO ---
        const beltGeo = new THREE.BoxGeometry(15, 0.2, 2);
        const beltMat = new THREE.MeshStandardMaterial({color: 0x333333});
        const conveyor = new THREE.Mesh(beltGeo, beltMat);
        conveyor.position.set(10, -4.8, 0);
        scene.add(conveyor);

        // --- COMEDERO Y ANIMAL (POTRERO) ---
        const trough = new THREE.Mesh(new THREE.BoxGeometry(3, 1, 3), new THREE.MeshStandardMaterial({color: 0x444444}));
        trough.position.set(18, -4.5, 0);
        scene.add(trough);

        // Robot Stacker
        const robot = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({color: 0xf1c40f}));
        scene.add(robot);

        camera.position.set(25, 15, 25);
        camera.lookAt(0, 0, 0);

        const light = new THREE.PointLight(0xffffff, 1);
        light.position.set(10, 20, 10);
        scene.add(light, new THREE.AmbientLight(0x404040));

        function animate() {
            requestAnimationFrame(animate);
            robot.position.y = ({{ dia }} * 1.5 - 4.5);
            robot.position.x = -4;
            
            // Simular movimiento de banda en día 7
            if ({{ dia }} == 7) {
                conveyor.material.color.setHex(0x00ff00);
            }
            
            scene.rotation.y += 0.002;
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

@app.route('/')
def inicio():
    nova_system.procesar()
    return render_template_string(HTML_FINAL, 
                                 dia=nova_system.dia_ciclo,
                                 receta=nova_system.receta,
                                 humedad=round(nova_system.humedad_suelo, 1),
                                 carbono=nova_system.carbono_suelo_ton)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)