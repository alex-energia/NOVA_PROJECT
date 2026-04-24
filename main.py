import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-B22-{random.randint(100,999)}"
        # Sensores Invernadero
        self.inv = {
            "ph": 5.8, "ce": 1.6, "vpd": 1.2, "etc": 3.4, "peso": 12.0, 
            "tanque": 100, "co2": 450, "crecimiento": 0, "lixiviados": 5.2
        }
        # Sensores Potrero
        self.pot = {
            "h2o_save": 0, "ch4": 0, "hum_10cm": 22.1, "hum_30cm": 18.5, 
            "temp_suelo": 14.2, "rad_global": 650, "ndvi": 0.72
        }

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["crecimiento"] = round(self.dia * 4.6, 1)
            self.inv["peso"] = round(12.0 + (self.dia * 10.2), 1)
            self.pot["h2o_save"] += 850
            self.pot["ch4"] += 2.6
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V22, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V22, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, bid=ctrl.batch_id)

HTML_V22 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v22 | Final Logistics & Sensors</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --alert: #ff0055; --bg: #000; }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: rgba(0, 15, 15, 0.9); border: 2px solid var(--neon); padding: 15px; z-index: 100; box-shadow: 0 0 15px var(--neon); }
        #ui-left { top: 10px; left: 10px; width: 320px; }
        #ui-right { top: 10px; right: 10px; width: 280px; }
        h2 { font-family: 'Orbitron'; font-size: 11px; color: var(--neon); text-transform: uppercase; margin: 0 0 10px 0; border-bottom: 1px solid #222; }
        .stat { display: flex; justify-content: space-between; font-size: 10px; margin-bottom: 5px; }
        .val { font-weight: 900; color: #fff; }
        button { background: var(--neon); color: #000; border: none; padding: 12px; width: 100%; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; margin-top: 5px; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>SCADA UNIT | {{ bid }}</h2>
        <div class="stat">DÍA: <span class="val">{{ d }} / 7</span></div>
        <div class="stat">VPD / ETc: <span class="val">{{ inv.vpd }} / {{ inv.etc }}</span></div>
        <div class="stat">BIOMASA: <span class="val">{{ inv.crecimiento }} CM</span></div>
        <div class="stat">PESO: <span class="val">{{ inv.peso }} KG</span></div>
        <div class="stat">LIXIVIADOS: <span class="val">{{ inv.lixiviados }}%</span></div>
        <button onclick="location.href='/next'">{{ "INICIAR DESPACHO" if d == 6 else "SIGUIENTE" if d < 7 else "REINICIAR" }}</button>
    </div>

    <div id="ui-right" class="hud">
        <h2>POTRERO (FIELD-SENSORS)</h2>
        <div class="stat">H2O SAVE: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">HUM (10/30/60): <span class="val">{{ pot.hum_10cm }}/{{ pot.hum_30cm }}/12%</span></div>
        <div class="stat">TEMP. SUELO: <span class="val">{{ pot.temp_suelo }} °C</span></div>
        <div class="stat">RAD. GLOBAL: <span class="val">{{ pot.rad_global }} W/m²</span></div>
        <div class="stat">NDVI: <span class="val">{{ pot.ndvi }}</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 1, 3000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- TORRE DE LUZ (VISIBILIDAD RADICAL) ---
        const towerGroup = new THREE.Group();
        const frameMat = new THREE.MeshBasicMaterial({color: 0x00ffcc, wireframe: true});
        const glassMat = new THREE.MeshBasicMaterial({color: 0x00ffff, transparent: true, opacity: 0.1});

        const floors = [];
        const doors = [];

        for(let i=0; i<10; i++){
            const h = i * 4 - 15;
            const floor = new THREE.Mesh(new THREE.BoxGeometry(8, 0.2, 8), frameMat);
            floor.position.y = h;
            
            // Forraje
            const gH = ({{ d }} * 0.5) + 0.2;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(7, gH, 7), new THREE.MeshBasicMaterial({color: ({{d}}==0?0x332211:0x00ff44)}));
            grass.position.y = h + gH/2;
            
            // Puertas
            const dL = new THREE.Mesh(new THREE.BoxGeometry(4, 3.5, 0.1), glassMat);
            dL.position.set(-2, h+1.8, 4);
            const dR = new THREE.Mesh(new THREE.BoxGeometry(4, 3.5, 0.1), glassMat);
            dR.position.set(2, h+1.8, 4);
            
            towerGroup.add(floor, grass, dL, dR);
            floors.push(h);
            doors.push({L: dL, R: dR});
        }
        scene.add(towerGroup);

        // --- ROBOT (BRAZO) ---
        const robot = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 5), new THREE.MeshBasicMaterial({color:0xff00ff}));
        scene.add(robot);

        // --- BANDA Y ANIMAL ---
        const belt = new THREE.Mesh(new THREE.BoxGeometry(50, 0.4, 6), new THREE.MeshBasicMaterial({color:0x222222}));
        belt.position.set(30, -18, 0);
        scene.add(belt);

        const animal = new THREE.Group();
        animal.add(new THREE.Mesh(new THREE.BoxGeometry(3, 2, 1.5), new THREE.MeshBasicMaterial({color: 0x442200})));
        animal.position.set(60, -17, 0);
        scene.add(animal);

        const trayH = new THREE.Mesh(new THREE.BoxGeometry(4, 0.2, 4), new THREE.MeshBasicMaterial({color: 0x00ff44}));
        trayH.position.set(5, -17.5, 0);
        trayH.visible = ({{ d }} == 7);
        scene.add(trayH);

        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now() * 0.001;

            if ({{ d }} == 0) {
                camera.position.lerp(new THREE.Vector3(60, 30, 60), 0.05);
                camera.lookAt(0, 0, 0);
            } else if ({{ d }} < 7) {
                const ty = floors[{{ d }}];
                camera.position.lerp(new THREE.Vector3(-15, ty + 5, 15), 0.05);
                camera.lookAt(0, ty, 0);
                // Abrir puertas
                doors[{{ d }}].L.position.x = -6;
                doors[{{ d }}].R.position.x = 6;
                robot.position.set(-5, ty+2, Math.sin(t)*3);
            } else {
                // LOGÍSTICA FINAL
                camera.position.lerp(new THREE.Vector3(70, 10, 30), 0.03);
                camera.lookAt(40, -10, 0);
                if(trayH.position.x < 55) trayH.position.x += 0.3;
                if(animal.position.x > 56) animal.position.x -= 0.15; // Camina al comedero
            }
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>