import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-B24-{random.randint(100,999)}"
        # Sensores e Indicadores
        self.inv = {"ph": 5.8, "vpd": 1.2, "etc": 3.4, "peso": 12.0, "co2": 450, "h_semilla": 0.5}
        # La Joya: Captura y medición de CO2 en potrero
        self.pot = {"h2o_save": 0, "co2_captura": 15.2, "co2_suelo": 850, "hum_10": 22.1, "rad": 650}
        self.mezcla = "Maíz (80%) + Cebada (15%) + Avena (5%)"

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["h_semilla"] = round(0.5 + (self.dia * 4.5), 1)
            self.inv["peso"] = round(12.0 + (self.dia * 10.5), 1)
            self.pot["h2o_save"] += 850
            self.pot["co2_captura"] += 5.4 # Incremento de captura por biomasa
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V24, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V24, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id, mez=ctrl.mezcla)

HTML_V24 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v24 | CO2 Capture SCADA</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --gold: #ffd700; --bg: #000; }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: rgba(0, 10, 10, 0.95); border: 2px solid var(--neon); padding: 15px; z-index: 100; box-shadow: 0 0 15px var(--neon); }
        #ui-left { top: 10px; left: 10px; width: 330px; }
        #ui-right { top: 10px; right: 10px; width: 280px; }
        h2 { font-family: 'Orbitron'; font-size: 11px; color: var(--neon); text-transform: uppercase; margin: 0 0 10px 0; border-bottom: 1px solid #222; }
        .stat { display: flex; justify-content: space-between; font-size: 10px; margin-bottom: 5px; }
        .val { font-weight: 900; color: #fff; }
        .jewel { color: var(--gold) !important; font-weight: 900; }
        button { background: var(--neon); color: #000; border: none; padding: 14px; width: 100%; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; margin-top: 5px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>INVERNADERO | {{ bid }}</h2>
        <div class="stat">CICLO: <span class="val">DÍA {{ d }} / 7</span></div>
        {% if d == 0 %}
        <div class="stat" style="color:var(--gold)">MEZCLA: <span class="val">{{ mez }}</span></div>
        {% endif %}
        <div class="stat">VPD / ETc: <span class="val">{{ inv.vpd }} / {{ inv.etc }}</span></div>
        <div class="stat">ALTURA FORRAJE: <span class="val">{{ inv.h_semilla }} CM</span></div>
        <button onclick="location.href='/next'">{{ "INICIAR COSECHA" if d == 6 else "AVANZAR" if d < 7 else "REINICIAR" }}</button>
    </div>

    <div id="ui-right" class="hud">
        <h2>POTRERO (LA JOYA: CO2)</h2>
        <div class="stat jewel">CO2 CAPTURADO: <span class="val">{{ pot.co2_captura }} KG</span></div>
        <div class="stat">CO2 EN SUELO: <span class="val">{{ pot.co2_suelo }} PPM</span></div>
        <div class="stat">RAD. GLOBAL: <span class="val">{{ pot.rad }} W/m²</span></div>
        <div class="stat">HUMEDAD 10CM: <span class="val">{{ pot.hum_10 }}%</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 3000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ILUMINACIÓN ---
        scene.add(new THREE.AmbientLight(0xffffff, 0.4));
        const point = new THREE.PointLight(0x00ffcc, 1, 100);
        scene.add(point);

        // --- ESTRUCTURA TORRE ---
        const towerGroup = new THREE.Group();
        const floors = []; const doors = [];
        const frameMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true});
        const glassMat = new THREE.MeshPhysicalMaterial({color: 0x00ffff, transparent: true, opacity: 0.3, transmission: 0.8});

        for(let i=0; i<10; i++){
            const h = i * 4.5 - 15;
            const floor = new THREE.Mesh(new THREE.BoxGeometry(9, 0.2, 9), frameMat);
            floor.position.y = h;
            
            // BANDEJA CON BORDE NEÓN
            const tray = new THREE.Mesh(new THREE.BoxGeometry(8, 0.3, 8), new THREE.MeshStandardMaterial({color: 0x111111}));
            tray.position.y = h + 0.2;
            
            // SEMILLA / FORRAJE
            const gH = ({{ d }} * 0.6) + 0.1;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(7.5, gH, 7.5), 
                        new THREE.MeshStandardMaterial({color: ({{d}}==0?0x5c4033:0x00ff44), emissive: 0x000000}));
            grass.position.y = h + 0.2 + gH/2;
            
            // PUERTAS
            const dL = new THREE.Mesh(new THREE.BoxGeometry(4.2, 4, 0.1), glassMat); dL.position.set(-2.1, h+2.2, 4.5);
            const dR = new THREE.Mesh(new THREE.BoxGeometry(4.2, 4, 0.1), glassMat); dR.position.set(2.1, h+2.2, 4.5);
            
            towerGroup.add(floor, tray, grass, dL, dR);
            floors.push(h); doors.push({L: dL, R: dR, tray: tray});
        }
        scene.add(towerGroup);

        // --- GOTEO ---
        const drips = new THREE.Group();
        for(let j=0; j<15; j++){
            const d = new THREE.Mesh(new THREE.SphereGeometry(0.05), new THREE.MeshBasicMaterial({color: 0x00ffff}));
            drips.add(d);
        }
        scene.add(drips);

        // --- ANIMAL (MEJORADO) ---
        const animal = new THREE.Group();
        const body = new THREE.Mesh(new THREE.SphereGeometry(1.2, 32, 32), new THREE.MeshStandardMaterial({color: 0x442200}));
        body.scale.set(1.5, 1, 1);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.7, 32, 32), new THREE.MeshStandardMaterial({color: 0x442200}));
        head.position.set(1.8, 0.5, 0);
        animal.add(body, head);
        animal.position.set(60, -18, 0);
        scene.add(animal);

        // --- ROBOT Y BANDA ---
        const robot = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 4), new THREE.MeshBasicMaterial({color: 0xff00ff}));
        scene.add(robot); robot.visible = false;
        const belt = new THREE.Mesh(new THREE.BoxGeometry(60, 0.5, 6), new THREE.MeshStandardMaterial({color: 0x222222}));
        belt.position.set(30, -19.5, 0); scene.add(belt);

        const trayH = new THREE.Mesh(new THREE.BoxGeometry(4, 0.2, 4), new THREE.MeshBasicMaterial({color: 0x00ff44}));
        trayH.position.set(5, -19, 0); trayH.visible = ({{ d }} == 7); scene.add(trayH);

        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now() * 0.001;

            if ({{ d }} == 0) {
                camera.position.lerp(new THREE.Vector3(75, 35, 75), 0.05);
                camera.lookAt(0, 0, 0);
            } else if ({{ d }} < 7) {
                const ty = floors[{{ d }}];
                camera.position.lerp(new THREE.Vector3(-18, ty + 6, 18), 0.05);
                camera.lookAt(0, ty, 0);
                // Puertas abren
                doors[{{ d }}].L.position.x = -6.5; doors[{{ d }}].R.position.x = 6.5;
                // Goteo
                drips.children.forEach((d, i) => {
                    d.position.set(Math.sin(i)*3, ty + 4 - ((t+i*0.2)%1)*4, Math.cos(i)*3);
                    d.visible = true;
                });
            } else {
                // DIA 7: ROBÓTICA Y DESPACHO
                camera.position.lerp(new THREE.Vector3(80, 20, 50), 0.02); // ZOOM OUT NATURAL
                camera.lookAt(40, -10, 0);
                robot.visible = true;
                robot.position.set(5, -15 + Math.sin(t)*2, 0); // Robot trabajando
                if(trayH.position.x < 55) trayH.position.x += 0.3;
                if(animal.position.x > 57) animal.position.x -= 0.15;
            }
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>