import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Clase de Control con lógica de estado sólido
class ControladorNOVA:
    def __init__(self):
        self.inicializar_datos()

    def inicializar_datos(self):
        self.dia = 0
        self.batch_id = f"NOVA-B-PRO-{random.randint(1000,9999)}"
        # Instrumentación Invernadero (Sensores Reales)
        self.inv = {
            "ph": 5.8, "ce": 1.75, "co2": 450, "o2": 21, "par": 0,
            "hum_foliar": 80, "tanque": 100, "presion_neb": 45.0,
            "luz_uv": "OFF", "temp_amb": 22.5
        }
        # Instrumentación Potrero y Sostenibilidad
        self.pot = {
            "hum_suelo": 22.0, "temp_suelo": 21.0, "ndvi": 0.65, 
            "ch4_reducido": 0.0, "evapo": 4.0, "carbono": 142.0,
            "ahorro_h2o": 0 # Litros ahorrados vs tradicional
        }
        self.receta = {
            "Maíz Amarillo": "105kg", 
            "Cebada Forrajera": "15kg", 
            "Avena": "10kg", 
            "Complejo Bio-Activo": "2.5kg"
        }

    def avanzar(self):
        if self.dia < 7:
            self.dia += 1
            # Simulación de crecimiento y consumo de recursos
            self.inv["par"] = random.randint(400, 700)
            self.inv["tanque"] -= 5
            self.inv["ph"] = round(random.uniform(5.7, 6.1), 1)
            self.pot["ch4_reducido"] = round(self.dia * 2.8, 1)
            self.pot["ahorro_h2o"] += 850 # Litros por día
            self.inv["luz_uv"] = "ON" if self.dia > 2 else "OFF"
        else:
            # Al llegar al día 7 y dar click, reiniciamos para el siguiente lote
            self.inicializar_datos()

# Instancia global
ctrl = ControladorNOVA()

@app.route('/')
def index():
    # Si viene el parámetro reset, forzamos la limpieza
    if request.args.get('reset'):
        ctrl.inicializar_datos()
    return render_template_string(HTML_V15, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.avanzar()
    return render_template_string(HTML_V15, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V15 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA | Enterprise Digital Twin v15</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --alert: #f1c40f; --bg: #030303; --panel: rgba(15, 15, 15, 0.95); }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        
        /* UI Estilo SCADA */
        .hud { position: absolute; background: var(--panel); border: 1px solid rgba(0, 255, 204, 0.3); 
               padding: 20px; backdrop-filter: blur(20px); border-radius: 10px; z-index: 100; box-shadow: 0 0 30px rgba(0,0,0,0.5); }
        
        #main-monitor { top: 20px; left: 20px; width: 350px; }
        #telemetry-grid { top: 20px; right: 20px; width: 320px; }
        #metrics-bottom { bottom: 20px; left: 50%; transform: translateX(-50%); width: 60%; display: flex; justify-content: space-around; }

        h2 { font-size: 13px; font-weight: 900; color: var(--neon); text-transform: uppercase; letter-spacing: 2px; 
             margin: 0 0 15px 0; border-bottom: 1px solid #333; padding-bottom: 8px; }
        
        .stat-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 12px; }
        .label { color: #888; text-transform: uppercase; font-size: 10px; }
        .value { font-weight: 700; color: #fff; }
        
        .btn { border: none; padding: 14px; width: 100%; border-radius: 5px; font-weight: 900; cursor: pointer; 
               text-transform: uppercase; transition: all 0.3s; font-family: 'Inter'; margin-top: 10px; }
        .btn-next { background: var(--neon); color: #000; }
        .btn-next:hover { background: #fff; box-shadow: 0 0 20px var(--neon); }
        .btn-reset { background: #222; color: #888; margin-top: 5px; font-size: 10px; }

        .badge { background: rgba(0,255,204,0.1); color: var(--neon); padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 900; }
        .metric-card { text-align: center; }
        .metric-val { font-size: 20px; font-weight: 900; color: var(--neon); display: block; }
        .metric-lab { font-size: 9px; color: #888; text-transform: uppercase; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

    <div id="main-monitor" class="hud">
        <h2>SISTEMA NOVA | {{ bid }}</h2>
        <div class="stat-row">
            <span class="label">Ciclo de Crecimiento</span>
            <span class="value">DÍA {{ d }} / 7</span>
        </div>
        <div class="stat-row">
            <span class="label">Estado Motor</span>
            <span class="badge">{{ "LOGÍSTICA DESPACHO" if d == 7 else "AUTOMATIZADO" }}</span>
        </div>
        
        <hr style="opacity:0.1; margin: 15px 0;">
        
        {% if d == 0 %}
            <h2>📦 CARGA INICIAL (RECETA)</h2>
            {% for k,v in rec.items() %}
                <div class="stat-row"><span class="label">{{ k }}</span><span class="value">{{ v }}</span></div>
            {% endfor %}
        {% elif d == 7 %}
            <h2 style="color:var(--alert)">🚀 ACTIVACIÓN DE COSECHA</h2>
            <p style="font-size: 11px; color: #aaa;">Robot Stacker transfiriendo bandeja a banda transportadora sector Alpha.</p>
        {% else %}
            <h2>🌱 ANÁLISIS DE BIOMASA</h2>
            <div class="stat-row"><span class="label">Altura Estimada</span><span class="value">{{ (d * 4.2)|round(1) }} cm</span></div>
            <div class="stat-row"><span class="label">Densidad Foliar</span><span class="value">{{ (d * 12)|round(0) }}%</span></div>
        {% endif %}

        <button class="btn btn-next" onclick="location.href='/next'">{{ "INICIAR NUEVO LOTE" if d == 7 else "AVANZAR 24 HORAS" }}</button>
        <button class="btn btn-reset" onclick="location.href='/?reset=1'">FORZAR RESET TOTAL</button>
    </div>

    <div id="telemetry-grid" class="hud">
        <h2>INVERNADERO (SENSÓRICA)</h2>
        <div class="stat-row"><span class="label">PH Nutrientes</span><span class="value">{{ inv.ph }}</span></div>
        <div class="stat-row"><span class="label">CO2 Atmosférico</span><span class="value">{{ inv.co2 }} ppm</span></div>
        <div class="stat-row"><span class="label">Rad. PAR</span><span class="value">{{ inv.par }} µmol</span></div>
        <div class="stat-row"><span class="label">Tanque Reserva</span><span class="value">{{ inv.tanque }}%</span></div>
        <div class="stat-row"><span class="label">Nebulización</span><span class="value">{{ inv.presion_neb }} PSI</span></div>
        <div class="stat-row"><span class="label">Luz UV-C</span><span class="value">{{ inv.luz_uv }}</span></div>
        
        <hr style="opacity:0.1; margin: 15px 0;">
        <h2>FIELD-LINK (POTRERO)</h2>
        <div class="stat-row"><span class="label">NDVI (Vigor)</span><span class="value">{{ pot.ndvi }}</span></div>
        <div class="stat-row"><span class="label">Hum. Suelo</span><span class="value">{{ pot.hum_suelo|round(1) }}%</span></div>
        <div class="stat-row"><span class="label">Temp. Suelo</span><span class="value">{{ pot.temp_suelo }} °C</span></div>
    </div>

    <div id="metrics-bottom" class="hud">
        <div class="metric-card">
            <span class="metric-val">{{ pot.ahorro_h2o }} L</span>
            <span class="metric-lab">Agua Ahorrada</span>
        </div>
        <div class="metric-card">
            <span class="metric-val">{{ pot.ch4_reducido }} kg</span>
            <span class="metric-lab">CO2 eq. Evitado</span>
        </div>
        <div class="metric-card">
            <span class="metric-val">{{ pot.carbono }} T</span>
            <span class="metric-lab">Carbono en Suelo</span>
        </div>
    </div>

    <script>
        // --- CONFIGURACIÓN DE ESCENA ---
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x020202);
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ILUMINACIÓN ---
        const light = new THREE.DirectionalLight(0xffffff, 1.5);
        light.position.set(10, 20, 10);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040, 2));

        // --- ENTORNO ---
        const ground = new THREE.GridHelper(100, 40, 0x00ffcc, 0x111111);
        ground.position.y = -8;
        scene.add(ground);

        // --- TORRE DE PRODUCCIÓN ---
        const towerGroup = new THREE.Group();
        const trays = [];
        for(let i=0; i<10; i++){
            const floorH = i * 2.2 - 8;
            const isTarget = (i == {{ d }});
            
            // Estructura de Piso
            const floor = new THREE.Mesh(
                new THREE.BoxGeometry(6, 0.15, 6), 
                new THREE.MeshStandardMaterial({color: 0x1a1a1a, metalness: 1})
            );
            floor.position.y = floorH;
            towerGroup.add(floor);

            // Resaltado de borde
            if(isTarget){
                const glow = new THREE.Mesh(
                    new THREE.BoxGeometry(6.3, 0.2, 6.3),
                    new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true})
                );
                glow.position.y = floorH;
                towerGroup.add(glow);
            }

            // FORRAJE (CRECIMIENTO DINÁMICO)
            const growth = ({{ d }} * 0.22) + 0.05;
            const forraje = new THREE.Mesh(
                new THREE.BoxGeometry(5.6, growth, 5.6),
                new THREE.MeshStandardMaterial({
                    color: ({{d}} == 0 ? 0x443322 : 0x00ff66),
                    roughness: 0.8
                })
            );
            forraje.position.y = floorH + growth/2;
            towerGroup.add(forraje);
            trays.push({mesh: forraje, h: floorH});
        }
        scene.add(towerGroup);

        // --- ROBOT STACKER ---
        const robot = new THREE.Group();
        const robBody = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1, 2), new THREE.MeshStandardMaterial({color:0xf1c40f}));
        robot.add(robBody);
        scene.add(robot);

        // --- BANDA TRANSPORTADORA ---
        const belt = new THREE.Mesh(new THREE.BoxGeometry(25, 0.3, 2.5), new THREE.MeshStandardMaterial({color:0x222222}));
        belt.position.set(15, -7.8, 0);
        scene.add(belt);

        // --- BANDEJA LOGÍSTICA (PARA EL DÍA 7) ---
        const logTray = new THREE.Mesh(new THREE.BoxGeometry(3, 0.2, 3), new THREE.MeshStandardMaterial({color: 0x00ff66}));
        logTray.position.set(5, -7.6, 0);
        logTray.visible = ({{ d }} == 7);
        scene.add(logTray);

        // --- ANIMAL (ORGANICO MEJORADO) ---
        const animal = new THREE.Group();
        const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.8, 2, 4, 12), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        body.rotation.z = Math.PI/2;
        const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.5, 1), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        neck.position.set(1.5, 0.5, 0);
        neck.rotation.z = -Math.PI/4;
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.6, 16, 16), new THREE.MeshStandardMaterial({color:0x4b2c20}));
        head.position.set(2.2, 0.8, 0);
        animal.add(body, neck, head);
        animal.position.set(35, -6.8, 0);
        scene.add(animal);

        // --- LÓGICA DE CÁMARA Y ANIMACIÓN ---
        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now() * 0.001;

            if ({{ d }} < 7) {
                // MODO INSPECCIÓN: ZOOM A BANDEJA
                const targetY = ({{ d }} * 2.2 - 8);
                robot.position.y = targetY + 0.6;
                robot.position.x = -4.5;
                robot.position.z = Math.sin(t) * 1.5; // Movimiento de escaneo

                const camPos = new THREE.Vector3(-10, targetY + 3, 10);
                camera.position.lerp(camPos, 0.05);
                camera.lookAt(0, targetY, 0);
            } else {
                // MODO COSECHA: VISTA GLOBAL
                camera.position.lerp(new THREE.Vector3(35, 15, 35), 0.03);
                camera.lookAt(15, -5, 0);

                // Movimiento de bandeja en banda
                if(logTray.position.x < 33) logTray.position.x += 0.25;
                
                // Animal se acerca al comedero
                if(animal.position.x > 34) animal.position.x -= 0.1;
                
                // Animación de cabeza del animal
                head.rotation.x = Math.sin(t * 6) * 0.2;
            }

            renderer.render(scene, camera);
        }
        animate();

        // Responsive
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