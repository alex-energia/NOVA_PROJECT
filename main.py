import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-X-{random.randint(100,999)}"
        # Instrumentación Invernadero (Ampliada)
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "par": 0, "tanque": 100,
            "presion": 45.2, "mg": 15, "k": 20, "ca": 12, "hum_foliar": 85,
            "peso_bandeja": 12.5  # Peso inicial en kg (semilla + bandeja)
        }
        # Telemetría Potrero
        self.pot = {
            "hum": 22.4, "ndvi": 0.65, "ch4": 0, "h2o_save": 0, 
            "carbono": 142.5, "evapo": 4.1, "nitrogeno": 18.2
        }
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg", "Bio": "2kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["par"] = random.randint(350, 650)
            self.pot["h2o_save"] += 850
            self.pot["ch4"] += 2.8
            self.inv["tanque"] -= 4
            # Incremento de peso por biomasa (crecimiento)
            self.inv["peso_bandeja"] = round(12.5 + (self.dia * 8.4), 2)
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V17, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V17, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V17 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v17 | Engineering Mode</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;600;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #020202; --panel: rgba(8, 8, 8, 0.98); --alert: #ff3333; }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        
        .hud { position: absolute; background: var(--panel); border: 1px solid rgba(0, 255, 204, 0.4); 
               padding: 22px; backdrop-filter: blur(20px); border-radius: 4px; z-index: 100; box-shadow: 0 0 25px rgba(0,0,0,0.8); }
        
        #ui-left { top: 20px; left: 20px; width: 350px; }
        #ui-right { top: 20px; right: 20px; width: 310px; }
        
        h2 { font-size: 11px; color: var(--neon); letter-spacing: 3px; text-transform: uppercase; margin: 0 0 15px 0; border-left: 3px solid var(--neon); padding-left: 10px; }
        .stat { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 10px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }
        .val { font-weight: 700; color: #fff; text-shadow: 0 0 5px var(--neon); }
        
        button { background: var(--neon); color: #000; border: none; padding: 15px; width: 100%; border-radius: 2px; 
                 font-weight: 900; cursor: pointer; text-transform: uppercase; margin-top: 10px; transition: 0.2s; letter-spacing: 1px; }
        button:hover { background: #fff; box-shadow: 0 0 30px var(--neon); }
        
        .alert-box { border: 1px solid var(--alert); color: var(--alert); padding: 8px; font-size: 10px; font-weight: 900; text-align: center; margin-top: 10px; border-radius: 4px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>NOVA CORE UNIT | {{ bid }}</h2>
        <div class="stat">ESTADO DEL CICLO: <span class="val">DÍA {{ d }} / 7</span></div>
        <div class="stat">PESO EN BANDEJA: <span class="val">{{ inv.peso_bandeja }} KG</span></div>
        
        <hr style="opacity:0.1; margin: 15px 0;">
        
        {% if d == 0 %}
            <div style="color: #f1c40f; font-size: 11px; margin-bottom:10px;">RECETA DE CARGA ACTIVA</div>
            {% for k,v in rec.items() %}<div class="stat">{{k}}: <span class="val">{{v}}</span></div>{% endfor %}
        {% else %}
            <div style="color: var(--neon); font-size: 11px; margin-bottom:10px;">PROYECCIÓN DE CRECIMIENTO</div>
            <div class="stat">BIOMASA ESTIMADA: <span class="val">{{ (d * 11.5)|round(1) }} KG</span></div>
            <div class="stat">ALTURA FOLIAR: <span class="val">{{ (d * 4.3)|round(1) }} CM</span></div>
        {% endif %}

        <button onclick="location.href='/next'">{{ "INICIAR COSECHA" if d == 6 else "AVANZAR DÍA" if d < 7 else "REINICIAR PROCESO" }}</button>
        <button style="background:#1a1a1a; color:#555; font-size:9px;" onclick="location.href='/?reset=1'">HARD RESET</button>
        
        {% if inv.ph > 6.0 %}<div class="alert-box">ALERTA: PH FUERA DE RANGO</div>{% endif %}
    </div>

    <div id="ui-right" class="hud">
        <h2>INSTRUMENTACIÓN IV</h2>
        <div class="stat">HUM. FOLIAR: <span class="val">{{ inv.hum_foliar }}%</span></div>
        <div class="stat">NIVEL TANQUE: <span class="val">{{ inv.tanque }}%</span></div>
        <div class="stat">PRESIÓN NEB.: <span class="val">{{ inv.presion }} PSI</span></div>
        <div class="stat">LUZ PAR: <span class="val">{{ inv.par }} µmol</span></div>
        <hr style="opacity:0.1">
        <h2>FIELD-LINK (POTRERO)</h2>
        <div class="stat">AHORRO H2O: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">METANO RED.: <span class="val">{{ pot.ch4 }} KG</span></div>
        <div class="stat">NDVI VIGOR: <span class="val">{{ pot.ndvi }}</span></div>
        <div class="stat">NITRÓGENO: <span class="val">{{ pot.nitrogeno }} mg/kg</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x010101);
        const camera = new THREE.PerspectiveCamera(40, window.innerWidth/window.innerHeight, 0.1, 2000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, logarithmicDepthBuffer: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ILUMINACIÓN INDUSTRIAL ---
        const amb = new THREE.AmbientLight(0xffffff, 0.5);
        scene.add(amb);
        const point = new THREE.PointLight(0x00ffcc, 1, 100);
        point.position.set(10, 20, 10);
        scene.add(point);

        // --- PISO TECNOLÓGICO ---
        const grid = new THREE.GridHelper(200, 80, 0x00ffcc, 0x111111);
        grid.position.y = -10;
        scene.add(grid);

        // --- CONSTRUCCIÓN DE TORRE (REFUERZO VISUAL) ---
        const towerGroup = new THREE.Group();
        const frameMat = new THREE.MeshStandardMaterial({color: 0x444444, metalness: 1, roughness: 0.1});
        
        // Vigas de Acero Inoxidable (Visibles)
        for(let x of [-4, 4]) {
            for(let z of [-4, 4]) {
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.4, 25, 0.4), frameMat);
                beam.position.set(x, 2, z);
                towerGroup.add(beam);
            }
        }

        // Pisos, Sensores de Carga y Forraje
        for(let i=0; i<10; i++){
            const h = i * 2.5 - 8;
            const active = (i == {{ d }});
            
            // Placa del Piso
            const floor = new THREE.Mesh(new THREE.BoxGeometry(7, 0.2, 7), new THREE.MeshStandardMaterial({color: 0x222222}));
            floor.position.y = h;
            towerGroup.add(floor);

            // Célula de Carga (Load Cell) - Pequeño cilindro rojo bajo la bandeja
            const loadCell = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.3), new THREE.MeshBasicMaterial({color: 0xff3333}));
            loadCell.position.set(0, h + 0.2, 0);
            towerGroup.add(loadCell);

            // Forraje Dinámico (Se vuelve verde y alto)
            const gH = ({{ d }} * 0.3) + 0.1;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(6.5, gH, 6.5), 
                          new THREE.MeshStandardMaterial({
                              color: ({{d}} == 0 ? 0x3d2b1f : 0x00ff66),
                              emissive: (active ? 0x00ff66 : 0x000000),
                              emissiveIntensity: 0.2
                          }));
            grass.position.y = h + gH/2 + 0.3;
            towerGroup.add(grass);
            
            if(active){
                const ring = new THREE.Mesh(new THREE.TorusGeometry(5, 0.05, 16, 100), new THREE.MeshBasicMaterial({color: 0x00ffcc}));
                ring.rotation.x = Math.PI/2;
                ring.position.y = h;
                towerGroup.add(ring);
            }
        }
        scene.add(towerGroup);

        // --- ANIMAL (MEJORADO ORGANICAMENTE) ---
        const cow = new THREE.Group();
        const cBody = new THREE.Mesh(new THREE.CapsuleGeometry(0.9, 2.2, 12, 24), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        cBody.rotation.z = Math.PI/2;
        const cNeck = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.6, 1.2), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        cNeck.position.set(1.8, 0.6, 0); cNeck.rotation.z = -Math.PI/4;
        const cHead = new THREE.Mesh(new THREE.SphereGeometry(0.7, 24, 24), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        cHead.position.set(2.5, 1, 0);
        cow.add(cBody, cNeck, cHead);
        cow.position.set(40, -8.5, 0);
        scene.add(cow);

        // --- BANDA TRANSPORTADORA ---
        const belt = new THREE.Mesh(new THREE.BoxGeometry(35, 0.4, 4), new THREE.MeshStandardMaterial({color: 0x111111, metalness: 1}));
        belt.position.set(20, -9.8, 0);
        scene.add(belt);

        const trayHarvest = new THREE.Mesh(new THREE.BoxGeometry(3, 0.2, 3), new THREE.MeshStandardMaterial({color: 0x00ff66}));
        trayHarvest.position.set(5, -9.5, 0);
        trayHarvest.visible = ({{ d }} == 7);
        scene.add(trayHarvest);

        camera.position.set(30, 15, 30);

        function animate() {
            requestAnimationFrame(animate);
            const time = Date.now() * 0.001;

            if ({{ d }} < 7) {
                const targetY = ({{ d }} * 2.5 - 8);
                // Zoom dinámico de inspección (Más cerca y angulado)
                camera.position.lerp(new THREE.Vector3(-14, targetY + 4, 14), 0.04);
                camera.lookAt(0, targetY, 0);
            } else {
                // Día 7: Despacho Global
                camera.position.lerp(new THREE.Vector3(45, 18, 45), 0.02);
                camera.lookAt(20, -5, 0);
                if(trayHarvest.position.x < 38) trayHarvest.position.x += 0.25;
                if(cow.position.x > 39) cow.position.x -= 0.1;
                cHead.rotation.x = Math.sin(time * 7) * 0.2;
            }
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)