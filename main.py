import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-X-{random.randint(100,999)}"
        # Telemetría Invernadero
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "o2": 21, "par": 0,
            "hum_foliar": 82, "tanque": 95, "presion_neb": 45.2
        }
        # Telemetría Potrero
        self.pot = {
            "hum_suelo": 22.4, "temp_suelo": 21.8, "ndvi": 0.72, 
            "ch4_reducido": 12.5, "evapo": 4.2, "carbono": 142.5
        }
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg", "Biotec": "2kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["par"] = random.randint(300, 600)
            self.inv["co2"] -= random.randint(5, 10) # Consumo planta
            self.pot["ch4_reducido"] += 2.1
        else:
            self.reset() # Reinicia después del ciclo de comida

ctrl = ControladorNOVA()

@app.route('/')
def index():
    # Siempre que se abra la URL sin parámetros de avance, podrías resetearlo, 
    # pero para esta demo, el botón de 'Avanzar' manejará el estado.
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V14, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V14, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V14 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Deep Inspection System</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #050505; --glass: rgba(10, 10, 10, 0.9); }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: var(--glass); border: 1px solid rgba(0, 255, 204, 0.2); 
               padding: 20px; backdrop-filter: blur(15px); border-radius: 8px; z-index: 100; pointer-events: auto; }
        #panel-ui { top: 20px; left: 20px; width: 330px; }
        #sensor-ui { top: 20px; right: 20px; width: 300px; }
        h2 { font-size: 12px; color: var(--neon); letter-spacing: 2px; margin: 0 0 15px 0; border-bottom: 1px solid #333; }
        .data { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px; }
        .val { font-weight: 700; color: #fff; }
        button { background: var(--neon); color: #000; border: none; padding: 12px; width: 100%; border-radius: 4px; 
                 font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: 10px; }
        .alert { color: #f1c40f; font-size: 10px; font-weight: bold; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="panel-ui" class="hud">
        <h2>CENTRAL CONTROL | {{ bid }}</h2>
        <div class="data">CICLO: <span class="val">DÍA {{ d }} / 7</span></div>
        <hr style="opacity:0.1">
        {% if d == 0 %}
            <div class="alert">MODO: CARGA DE SEMILLAS</div>
            {% for k,v in rec.items() %}<div class="data">{{k}}: <span class="val">{{v}}</span>{% endfor %}
        {% elif d == 7 %}
            <div class="alert">MODO: DESPACHO LOGÍSTICO</div>
            <div class="data">DESTINO: <span class="val">POTRERO SECTOR A1</span></div>
        {% else %}
            <div class="alert">MODO: INSPECCIÓN DE BIOMASA</div>
            <div class="data">ESTADO: <span class="val">DESARROLLO FOLIAR</span></div>
        {% endif %}
        <button onclick="location.href='/next'">Avanzar Ciclo</button>
        <button style="background:#333; color:white; margin-top:5px;" onclick="location.href='/?reset=1'">Reiniciar</button>
    </div>

    <div id="sensor-ui" class="hud">
        <h2>GREENHOUSE TELEMETRY</h2>
        <div class="data">PH AGUA: <span class="val">{{ inv.ph }}</span></div>
        <div class="data">CO2: <span class="val">{{ inv.co2 }} ppm</span></div>
        <div class="data">PAR (LUZ): <span class="val">{{ inv.par }} umol</span></div>
        <div class="data">TANQUE H2O: <span class="val">{{ inv.tanque }}%</span></div>
        <div class="data">PRESION: <span class="val">{{ inv.presion_neb }} PSI</span></div>
        <hr style="opacity:0.1">
        <h2>FIELD-LINK DATA</h2>
        <div class="data">NDVI VIGOR: <span class="val">{{ pot.ndvi }}</span></div>
        <div class="data">RED. CH4: <span class="val">{{ pot.ch4_reducido }} kg</span></div>
        <div class="data">HUM. SUELO: <span class="val">{{ pot.hum_suelo|round(1) }}%</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x050505);
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- AMBIENTE ---
        const grid = new THREE.GridHelper(100, 50, 0x00ffcc, 0x111111);
        grid.position.y = -8;
        scene.add(grid);

        // --- TORRE DE INVERNADERO ---
        const tower = new THREE.Group();
        const floors = [];
        for(let i=0; i<10; i++){
            const floorGroup = new THREE.Group();
            const h = i * 2 - 8;
            
            // Piso con borde
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6, 0.1, 6), new THREE.MeshStandardMaterial({color:0x111111}));
            floor.position.y = h;
            floorGroup.add(floor);
            
            if(i == {{ d }}){
                const border = new THREE.Mesh(new THREE.BoxGeometry(6.2, 0.2, 6.2), new THREE.MeshBasicMaterial({color:0x00ffcc, wireframe:true}));
                border.position.y = h;
                floorGroup.add(border);
            }

            // Forraje Dinámico (Día 0: Semilla, Día 7: 30cm)
            const growthHeight = ({{ d }} * 0.2) + 0.05;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(5.5, growthHeight, 5.5), 
                         new THREE.MeshStandardMaterial({color: ({{d}} == 0 ? 0x554433 : 0x00ff44)}));
            grass.position.y = h + growthHeight/2;
            floorGroup.add(grass);
            
            tower.add(floorGroup);
            floors.push(floorGroup);
        }
        scene.add(tower);

        // --- ROBOT STACKER ---
        const robot = new THREE.Group();
        robot.add(new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.8, 1.5), new THREE.MeshStandardMaterial({color:0xf1c40f})));
        scene.add(robot);

        // --- BANDA Y COMEDERO ---
        const conveyor = new THREE.Mesh(new THREE.BoxGeometry(25, 0.2, 2), new THREE.MeshStandardMaterial({color:0x222222}));
        conveyor.position.set(15, -7.9, 0);
        scene.add(conveyor);

        // --- ANIMAL (MEJORADO) ---
        const animal = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.8, 2, 4, 12), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        body.rotation.z = Math.PI/2;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.6, 12, 12), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        head.position.set(1.8, 0.5, 0);
        animal.add(body, head);
        animal.position.set(32, -7, 0);
        scene.add(animal);

        // Bandeja de Cosecha
        const tray = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.1, 2.5), new THREE.MeshStandardMaterial({color:0x00ff44}));
        tray.position.set(5, -7.7, 0);
        tray.visible = ({{ d }} == 7);
        scene.add(tray);

        // Luces
        const light = new THREE.PointLight(0xffffff, 1.5); light.position.set(20, 30, 20);
        scene.add(light, new THREE.AmbientLight(0x404040, 1.5));

        // --- LÓGICA DE CÁMARA Y ANIMACIÓN ---
        function animate() {
            requestAnimationFrame(animate);
            const time = Date.now() * 0.001;

            if ({{ d }} < 7) {
                // ZOOM DE INSPECCIÓN A LA BANDEJA ACTIVA
                const targetY = ({{ d }} * 2 - 8);
                robot.position.y = targetY + 0.5;
                robot.position.x = -4.5;

                // Cámara se acerca a la bandeja
                const camTarget = new THREE.Vector3(-8, targetY + 2, 8);
                camera.position.lerp(camTarget, 0.05);
                camera.lookAt(-2, targetY, 0);
            } else {
                // DÍA 7: LOGÍSTICA Y DESPACHO
                const camFar = new THREE.Vector3(30, 10, 30);
                camera.position.lerp(camFar, 0.03);
                camera.lookAt(15, -5, 0);

                // Mover bandeja y animal
                if(tray.position.x < 30) tray.position.x += 0.2;
                if(animal.position.x > 31) animal.position.x -= 0.1;
                head.rotation.x = Math.sin(time * 5) * 0.2; // Animal comiendo
            }

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)