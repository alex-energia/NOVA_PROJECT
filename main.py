import datetime
import random
from flask import Flask, render_template_string

app = Flask(__name__)

class SistemaCentralNOVA:
    def __init__(self):
        self.batch_id = "B-PRO-001"
        self.dia_ciclo = 0
        self.presion_hidraulica = 45.0
        self.nutrientes_ph = 6.0
        self.nutrientes_ce = 1.8
        # Trazabilidad de ingredientes (Día 0)
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Alfalfa": "5kg", "Quelatos": "2kg"}
        # Mediciones Potrero
        self.humedad_suelo = 22.5
        self.temp_suelo = 24.0
        self.carbono_suelo_ton = 142.5

    def procesar(self):
        self.dia_ciclo = (self.dia_ciclo + 1) if self.dia_ciclo < 8 else 0
        self.presion_hidraulica = round(random.uniform(44.0, 46.0), 1)
        self.nutrientes_ph = round(random.uniform(5.8, 6.2), 2)
        self.nutrientes_ce = round(random.uniform(1.7, 1.9), 2)
        self.humedad_suelo += random.uniform(-0.3, 0.3)

nova_system = SistemaCentralNOVA()

HTML_CINEMATIC = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Cinematic Engineering</title>
    <style>
        :root { --main: #00ffcc; --industrial: #1a1a1a; --tech-yellow: #f1c40f; }
        body { margin: 0; background: #010101; color: var(--main); font-family: 'Orbitron', sans-serif; overflow: hidden; }
        .hud-panel { position: absolute; background: rgba(0,0,0,0.85); border: 2px solid var(--main); padding: 20px; backdrop-filter: blur(15px); z-index: 10; width: 320px; }
        #left-ui { top: 20px; left: 20px; }
        #right-ui { top: 20px; right: 20px; }
        h1 { font-size: 16px; margin: 0 0 15px 0; letter-spacing: 2px; border-bottom: 1px solid var(--main); }
        .data-stream { display: flex; justify-content: space-between; font-size: 12px; margin: 5px 0; }
        .ingredient { font-size: 11px; color: #888; }
        .event-alert { color: var(--tech-yellow); animation: blink 1s infinite; font-weight: bold; font-size: 11px; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.2; } 100% { opacity: 1; } }
        button { background: var(--main); color: black; border: none; padding: 12px; width: 100%; font-weight: 900; cursor: pointer; margin-top: 15px; font-family: 'Orbitron', sans-serif; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
</head>
<body>
    <div id="left-ui" class="hud-panel">
        <h1>UNIT: {{ batch }}</h1>
        <div class="data-stream"><span>DÍA DE PROCESO:</span> <span style="color:white">{{ dia }}/7</span></div>
        <div class="data-stream"><span>PRESION AGUA:</span> <span style="color:white">{{ presion }} PSI</span></div>
        <div class="data-stream"><span>SISTEMA PH:</span> <span style="color:white">{{ ph }}</span></div>
        <div class="data-stream"><span>SISTEMA CE:</span> <span style="color:white">{{ ce }} mS/cm</span></div>
        <hr style="border:0.1px solid #333">
        {% if dia == 0 %}
            <h2>📦 CARGA DE INGREDIENTES</h2>
            {% for ing, cant in receta.items() %}
            <div class="ingredient">{{ ing }}: <span style="color:white">{{ cant }}</span></div>
            {% endfor %}
        {% else %}
            <h2>📊 MONITOREO BIOMASA</h2>
            <div class="event-alert">
                {% if dia == 4 %}
                    >> BIO-DEFENSA NEEM/AJO ACTIVA
                {% elif dia == 7 %}
                    >> COSECHA Y DESPACHO EN CURSO
                {% else %}
                    CRECIMIENTO NOMINAL
                {% endif %}
            </div>
        {% endif %}
        <button onclick="location.reload()">AVANZAR CICLO DE TIEMPO (24H)</button>
    </div>

    <div id="right-ui" class="hud-panel">
        <h1>POTRERO | FIELD-LINK</h1>
        <div class="data-stream"><span>HUMEDAD SUELO:</span> <span style="color:white">{{ humedad }}%</span></div>
        <div class="data-stream"><span>TEMP SUELO:</span> <span style="color:white">{{ t_suelo }} °C</span></div>
        <div class="data-stream"><span>C-ORGÁNICO:</span> <span style="color:white">{{ carbono }} TON/HA</span></div>
        <div class="event-alert" style="margin-top:10px;">{{ "HATO PROTEGIDO SISTÉMICAMENTE" if dia >= 4 else "HATO EN MONITOREO" }}</div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ENTORNO ---
        const ground = new THREE.Mesh(new THREE.PlaneGeometry(100, 100), new THREE.MeshStandardMaterial({color: 0x050505}));
        ground.rotation.x = -Math.PI/2; ground.position.y = -8;
        scene.add(ground);

        // --- INVERNADERO INDUSTRIAL ---
        const greenCore = new THREE.Group();
        const frame = new THREE.BoxGeometry(7, 16, 7);
        const frameMat = new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.1 });
        greenCore.add(new THREE.Mesh(frame, frameMat));
        
        for(let i=0; i<10; i++) {
            const h = i * 1.6 - 7;
            // Pisos Metálicos
            const piso = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), new THREE.MeshStandardMaterial({color: (i == {{ dia }}) ? 0x00ffcc : 0x1a1a1a, metalness: 1}));
            piso.position.y = h;
            greenCore.add(piso);
            
            // Forraje Dinámico
            const grasGeo = new THREE.BoxGeometry(5.5, ({{ dia }} * 0.1) + 0.1, 5.5);
            const grass = new THREE.Mesh(grasGeo, new THREE.MeshPhongMaterial({color: 0x00aa00}));
            grass.position.y = h + (({{ dia }} * 0.1) + 0.1)/2;
            greenCore.add(grass);

            // SISTEMA DE AGUA: Tuberías de Riego (Visibles)
            const pipeGeo = new THREE.CylinderGeometry(0.05, 0.05, 6);
            const pipeMat = new THREE.MeshStandardMaterial({ color: 0xdddddd, metalness: 1 });
            const pipe = new THREE.Mesh(pipeGeo, pipeMat);
            pipe.rotation.z = Math.PI/2;
            pipe.position.set(0, h + 1.2, -2.8);
            greenCore.add(pipe);
        }
        scene.add(greenCore);

        // --- PANELES SOLARES (TECHO) ---
        const solar = new THREE.Mesh(new THREE.BoxGeometry(8, 0.1, 8), new THREE.MeshStandardMaterial({color: 0x001133, metalness: 1}));
        solar.position.y = 8.5;
        scene.add(solar);

        // --- ROBOT STACKER (CINEMÁTICA REALISTA) ---
        const robot = new THREE.Group();
        robot.add(new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.8, 1.5), new THREE.MeshStandardMaterial({color: 0xf1c40f})));
        robot.add(new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 3), new THREE.MeshStandardMaterial({color: 0x444444})));
        scene.add(robot);

        // --- LOGÍSTICA DE CAMPO (DÍA 7) ---
        const beltMat = new THREE.MeshStandardMaterial({color: 0x333333, metalness: 1});
        const conveyor = new THREE.Mesh(new THREE.BoxGeometry(20, 0.2, 2), beltMat);
        conveyor.position.set(13, -7.8, 0);
        scene.add(conveyor);

        const trough = new THREE.Mesh(new THREE.BoxGeometry(3, 1, 3), new THREE.MeshStandardMaterial({color: 0x444444}));
        trough.position.set(23, -7.5, 0);
        scene.add(trough);

        // Animal Vacuno (Modelo Industrial)
        const animal = new THREE.Group();
        animal.add(new THREE.Mesh(new THREE.BoxGeometry(3, 2, 1.5), new THREE.MeshStandardMaterial({color: 0x4b2c20}))); // Cuerpo
        animal.add(new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 1.5), new THREE.MeshStandardMaterial({color: 0x4b2c20}))); // Cuello
        animal.position.set(30, -7, 0); // Posición inicial lejana
        scene.add(animal);

        // Bandeja de Cosecha
        const trayHarvest = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.2, 2.5), new THREE.MeshPhongMaterial({color: 0x00ff00}));
        trayHarvest.position.set(4, -7.6, 0); trayHarvest.visible = false;
        scene.add(trayHarvest);

        // --- ILUMINACIÓN ---
        const light = new THREE.PointLight(0xffffff, 1.5); light.position.set(10, 20, 10);
        scene.add(light, new THREE.AmbientLight(0x404040, 1));

        camera.position.set(25, 10, 25); camera.lookAt(0, 0, 0);

        function animate() {
            requestAnimationFrame(animate);
            
            // Cinemática Robot Stacker (Subida e Inserción)
            const currentFloorH = ({{ dia }} * 1.6 - 7);
            robot.position.y += (currentFloorH + 0.4 - robot.position.y) * 0.05;
            robot.position.x = -4.5;
            // Simulación de movimiento de brazo (extensión en Z)
            robot.position.z = Math.sin(Date.now() * 0.005) * 2;

            // --- ANIMACIÓN DE COSECHA (DÍA 7) ---
            if ({{ dia }} == 7) {
                // 1. Zoom al potrero
                camera.position.lerp(new THREE.Vector3(35, 5, 20), 0.02);
                camera.lookAt(20, -5, 0);

                // 2. Mover bandeja
                trayHarvest.visible = true;
                if(trayHarvest.position.x < 22) trayHarvest.position.x += 0.1;

                // 3. Animal se acerca y come
                if(animal.position.x > 25) {
                    animal.position.x -= 0.05;
                } else {
                    // Animación de ingesta
                    animal.rotation.x = Math.sin(Date.now() * 0.01) * 0.1;
                    trayHarvest.scale.lerp(new THREE.Vector3(0,0,0), 0.005); // Pasto desaparece
                }
            } else {
                scene.rotation.y += 0.001; // Rotación lenta normal
            }

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
    return render_template_string(HTML_CINEMATIC, 
                                 batch=nova_system.batch_id, 
                                 dia=nova_system.dia_ciclo,
                                 ph=nova_system.nutrientes_ph,
                                 ce=nova_system.nutrientes_ce,
                                 presion=nova_system.presion_hidraulica,
                                 receta=nova_system.receta,
                                 humedad=round(nova_system.humedad_suelo, 1),
                                 t_suelo=round(nova_system.temp_suelo, 1),
                                 carbono=nova_system.carbono_suelo_ton)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
