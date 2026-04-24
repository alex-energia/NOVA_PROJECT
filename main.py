import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-X-{random.randint(100,999)}"
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "par": 0, "tanque": 100,
            "presion": 45.2, "peso": 12.5, "hum_foliar": 85
        }
        self.pot = {
            "h2o_save": 0, "ch4": 0, "ndvi": 0.65
        }
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["peso"] = round(12.5 + (self.dia * 9.2), 1)
            self.pot["h2o_save"] += 850
            self.pot["ch4"] += 2.8
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V18, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V18, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V18 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v18 | SCADA Digital Twin</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --alert: #ff0055; --bg: #000; }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        
        /* Estilo SCADA */
        .hud { position: absolute; background: rgba(5, 10, 10, 0.9); border: 2px solid var(--neon); 
               padding: 20px; backdrop-filter: blur(10px); border-radius: 4px; z-index: 100; box-shadow: 0 0 20px rgba(0,255,204,0.2); }
        #ui-left { top: 20px; left: 20px; width: 340px; }
        #ui-right { top: 20px; right: 20px; width: 300px; cursor: pointer; }
        
        h1, h2 { font-family: 'Orbitron', sans-serif; font-size: 12px; color: var(--neon); letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; }
        .stat { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; border-bottom: 1px solid rgba(0,255,204,0.1); }
        .val { font-weight: 700; color: #fff; }
        
        /* Gráfica Flotante */
        #water-graph { display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                       width: 400px; height: 250px; background: rgba(0,20,20,0.95); border: 2px solid #fff; z-index: 1000; padding: 20px; }

        button { background: var(--neon); color: #000; border: none; padding: 15px; width: 100%; border-radius: 2px; 
                 font-family: 'Orbitron'; font-weight: 900; cursor: pointer; margin-top: 10px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 30px var(--neon); }

        /* Etiquetas 3D */
        .tag { position: absolute; background: rgba(0,0,0,0.8); border: 1px solid var(--neon); padding: 5px; font-size: 10px; color: var(--neon); pointer-events: none; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h1>UNIT CONTROL | {{ bid }}</h1>
        <div class="stat">MODO: <span class="val">{{ "COSECHA" if d == 7 else "GROWTH_SCADA" }}</span></div>
        <div class="stat">DÍA: <span class="val">{{ d }} / 7</span></div>
        <button onclick="location.href='/next'">EJECUTAR AVANCE CICLO</button>
        <button style="background:#222; color:#555; font-size:10px;" onclick="location.href='/?reset=1'">RESET COLD BOOT</button>
    </div>

    <div id="ui-right" class="hud" onclick="document.getElementById('water-graph').style.display='block'">
        <h2>TELEMETRÍA (CLICK PARA GRÁFICA H2O)</h2>
        <div class="stat">H2O SAVE: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">PESO: <span class="val">{{ inv.peso }} kg</span></div>
        <div class="stat">CO2: <span class="val">{{ inv.co2 }} ppm</span></div>
        <div class="stat">HUM. FOLIAR: <span class="val">{{ inv.hum_foliar }}%</span></div>
    </div>

    <div id="water-graph" onclick="this.style.display='none'">
        <h2>AHORRO HÍDRICO ACUMULADO (L)</h2>
        <div style="display: flex; align-items: flex-end; height: 150px; gap: 10px;">
            {% for i in range(d + 1) %}
            <div style="background: var(--neon); width: 30px; height: {{ i * 20 + 10 }}px;"></div>
            {% endfor %}
        </div>
        <p style="font-size: 10px; margin-top: 20px;">Total: {{ pot.h2o_save }} Litros ahorrados vs agricultura tradicional.</p>
        <p style="font-size: 9px; color: #888;">[ CLICK PARA CERRAR ]</p>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x000000);
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- TORRE SCADA BRUTAL ---
        const tower = new THREE.Group();
        const metalMat = new THREE.MeshStandardMaterial({color: 0x222222, metalness: 1, roughness: 0.1});
        const neonMat = new THREE.MeshBasicMaterial({color: 0x00ffcc});

        // Vigas Maestro (Exoesqueleto Brillante)
        for(let x of [-3.5, 3.5]) {
            for(let z of [-3.5, 3.5]) {
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.3, 24, 0.3), metalMat);
                beam.position.set(x, 4, z);
                tower.add(beam);
                
                const edge = new THREE.Mesh(new THREE.BoxGeometry(0.05, 24.1, 0.05), neonMat);
                edge.position.set(x, 4, z);
                tower.add(edge);
            }
        }

        // Pisos y Elementos SCADA
        const floors = [];
        for(let i=0; i<10; i++){
            const h = i * 2.4 - 8;
            const floorGroup = new THREE.Group();
            
            // Bandeja
            const tray = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.2, 6.5), metalMat);
            tray.position.y = h;
            floorGroup.add(tray);

            // Forraje (Crecimiento)
            const hG = ({{ d }} * 0.28) + 0.1;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(6, hG, 6), 
                          new THREE.MeshStandardMaterial({color: ({{d}}==0?0x332211:0x00ff44)}));
            grass.position.y = h + hG/2;
            floorGroup.add(grass);

            tower.add(floorGroup);
            floors.push({group: floorGroup, y: h});
        }
        scene.add(tower);

        // --- SISTEMA DE GOTEO (PARTÍCULAS) ---
        const dripCount = 50;
        const drips = new THREE.Group();
        for(let i=0; i<dripCount; i++){
            const drip = new THREE.Mesh(new THREE.SphereGeometry(0.02), new THREE.MeshBasicMaterial({color:0x00ffff}));
            drips.add(drip);
        }
        scene.add(drips);

        // --- ANIMAL ---
        const animal = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.8, 2, 4, 16), new THREE.MeshStandardMaterial({color: 0x331a00}));
        body.rotation.z = Math.PI/2;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.6), new THREE.MeshStandardMaterial({color: 0x331a00}));
        head.position.set(1.8, 0.6, 0);
        animal.add(body, head);
        animal.position.set(35, -8, 0);
        scene.add(animal);

        // Iluminación
        const l1 = new THREE.PointLight(0x00ffcc, 2, 50); l1.position.set(10, 10, 10);
        scene.add(l1, new THREE.AmbientLight(0xffffff, 0.3));

        function animate() {
            requestAnimationFrame(animate);
            const time = Date.now() * 0.001;

            if ({{ d }} < 7) {
                const ty = floors[{{ d }}].y;
                // ZOOM INTRUSIVO
                camera.position.lerp(new THREE.Vector3(-14, ty + 4, 14), 0.05);
                camera.lookAt(0, ty, 0);

                // Animación de Goteo
                drips.children.forEach((d, i) => {
                    d.position.y = ty + 2 - ( (time + i*0.1) % 1 ) * 2;
                    d.position.x = Math.sin(i) * 2;
                    d.position.z = Math.cos(i) * 2;
                    d.visible = true;
                });
            } else {
                // DESPACHO
                camera.position.lerp(new THREE.Vector3(45, 15, 45), 0.03);
                camera.lookAt(20, -5, 0);
                drips.children.forEach(d => d.visible = false);
                if(animal.position.x > 32) animal.position.x -= 0.1;
                head.rotation.x = Math.sin(time*8)*0.2;
            }

            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>