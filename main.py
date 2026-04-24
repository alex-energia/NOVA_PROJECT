import random
from flask import Flask, render_template_string

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.dia = 0
        self.lote = "NOVA-PREMIUM-X"
        self.sensores = {
            "caudal": 1.25, "ph": 5.9, "ce": 1.85, "co2": 480, "temp": 22.4
        }
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Micro": "2.5kg"}

    def update(self):
        self.dia = (self.dia + 1) if self.dia < 8 else 0
        self.sensores["caudal"] = round(random.uniform(1.2, 1.4), 2)
        self.sensores["temp"] = round(random.uniform(21.5, 23.5), 1)

ctrl = ControladorNOVA()

HTML_PRO_VISUAL = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Industrial Digital Twin</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --glass: rgba(15, 15, 15, 0.85); }
        body { margin: 0; background: #0a0a0a; color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        
        .hud { position: absolute; background: var(--glass); border: 1px solid rgba(0, 255, 204, 0.3); 
               padding: 25px; backdrop-filter: blur(12px); border-radius: 12px; z-index: 100; }
        #panel-left { top: 30px; left: 30px; width: 320px; }
        #panel-right { top: 30px; right: 30px; width: 280px; }
        
        h1 { font-size: 14px; font-weight: 900; letter-spacing: 2px; color: var(--neon); margin: 0 0 20px 0; border-bottom: 1px solid #333; padding-bottom: 10px; }
        .data-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; font-weight: 300; }
        .value { color: var(--neon); font-weight: 600; }
        
        .btn-advance { background: var(--neon); color: black; border: none; padding: 15px; width: 100%; 
                       border-radius: 6px; font-weight: 900; cursor: pointer; text-transform: uppercase; transition: 0.3s; }
        .btn-advance:hover { box-shadow: 0 0 20px var(--neon); transform: translateY(-2px); }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="panel-left" class="hud">
        <h1>COMMAND CENTER</h1>
        <div class="data-row">ID LOTE: <span class="value">{{ lote }}</span></div>
        <div class="data-row">ESTADO: <span class="value">{{ "DESPACHO" if dia == 7 else "PRODUCCIÓN" }}</span></div>
        <div class="data-row">DÍA DE CICLO: <span class="value">{{ dia }} / 7</span></div>
        <hr style="opacity:0.1">
        {% if dia == 0 %}
            <h1 style="color:#f1c40f">LOGÍSTICA CARGA</h1>
            {% for k,v in receta.items() %}<div class="data-row">{{k}}: <span class="value">{{v}}</span></div>{% endfor %}
        {% else %}
            <h1>BIOTECH MONITOR</h1>
            <div class="data-row">SUPLEMENTO: <span class="value">{{ "NEEM/AJO" if dia >= 4 else "NPK BASE" }}</span></div>
        {% endif %}
        <button class="btn-advance" onclick="location.href='/'">Avanzar Ciclo Temporal</button>
    </div>

    <div id="panel-right" class="hud">
        <h1>INSTRUMENTACIÓN</h1>
        <div class="data-row">PH: <span class="value">{{ s.ph }}</span></div>
        <div class="data-row">CE: <span class="value">{{ s.ce }} mS</span></div>
        <div class="data-row">TEMP: <span class="value">{{ s.temp }} °C</span></div>
        <div class="data-row">CAUDAL: <span class="value">{{ s.caudal }} L/min</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x0a0a0a);
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- SUELO TRIDIMENSIONAL ---
        const grid = new THREE.GridHelper(100, 40, 0x00ffcc, 0x1a1a1a);
        grid.position.y = -8;
        scene.add(grid);

        // --- INVERNADERO (TORRE) ---
        const tower = new THREE.Group();
        for(let i=0; i<10; i++) {
            const h = i * 1.8 - 7;
            const isActive = (i == {{ dia }});
            
            // Suelo del piso
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), new THREE.MeshStandardMaterial({color: 0x111111, metalness: 0.8}));
            floor.position.y = h;
            tower.add(floor);

            // Resaltado de borde neón si es el piso activo
            if(isActive) {
                const borderGeo = new THREE.BoxGeometry(6.2, 0.15, 6.2);
                const borderMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true});
                const border = new THREE.Mesh(borderGeo, borderMat);
                border.position.y = h;
                tower.add(border);
            }
        }
        scene.add(tower);

        // --- BANDA TRANSPORTADORA ---
        const conveyor = new THREE.Mesh(new THREE.BoxGeometry(20, 0.3, 2), new THREE.MeshStandardMaterial({color:0x222222, metalness:0.9}));
        conveyor.position.set(10, -7.8, 0);
        scene.add(conveyor);

        // --- ANIMAL (ORGANICO) ---
        const animal = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CapsuleGeometry(1, 2, 8, 16), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        body.rotation.z = Math.PI/2;
        animal.add(body);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.7, 16, 16), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        head.position.set(1.8, 0.5, 0);
        animal.add(head);
        animal.position.set(25, -6.5, 0);
        scene.add(animal);

        // Bandeja de entrega
        const tray = new THREE.Mesh(new THREE.BoxGeometry(2, 0.2, 2), new THREE.MeshPhongMaterial({color:0x00ff00}));
        tray.position.set(4, -7.6, 0);
        tray.visible = ({{ dia }} == 7);
        scene.add(tray);

        // --- ROBOT ---
        const robot = new THREE.Group();
        robot.add(new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.8, 1.2), new THREE.MeshStandardMaterial({color:0xf1c40f})));
        scene.add(robot);

        // Luces
        const light = new THREE.DirectionalLight(0xffffff, 1.2);
        light.position.set(10, 20, 10);
        scene.add(light, new THREE.AmbientLight(0x404040, 1));
        camera.position.set(28, 10, 28); camera.lookAt(5, -2, 0);

        function animate() {
            requestAnimationFrame(animate);
            robot.position.y = ({{ dia }} * 1.8 - 6.6);
            robot.position.x = -4.2;
            robot.rotation.y += 0.01;

            if({{ dia }} == 7) {
                // Mover bandeja por la banda
                if(tray.position.x < 22) tray.position.x += 0.15;
                // Mover animal al comedero
                if(animal.position.x > 23) animal.position.x -= 0.08;
                head.rotation.x = Math.sin(Date.now()*0.01)*0.2;
            } else {
                scene.rotation.y += 0.001;
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
    ctrl.update()
    return render_template_string(HTML_PRO_VISUAL, dia=ctrl.dia, s=ctrl.sensores, receta=ctrl.receta, lote=ctrl.lote)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
