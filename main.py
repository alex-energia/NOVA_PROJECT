import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-SYS-{random.randint(100,999)}"
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "tanque": 100,
            "presion": 45.2, "peso": 12.5, "hum": 85, "crecimiento": 0
        }
        self.pot = {"h2o_save": 0, "ch4": 0}
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["crecimiento"] = round(self.dia * 4.28, 1)
            self.inv["peso"] = round(12.5 + (self.dia * 9.5), 1)
            self.pot["h2o_save"] += 850
            self.pot["ch4"] += 2.8
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V19, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V19, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V19 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v19 | Industrial SCADA</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #000; --glass: rgba(0, 20, 20, 0.9); }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: var(--glass); border: 2px solid var(--neon); padding: 20px; z-index: 100; }
        #ui-left { top: 20px; left: 20px; width: 320px; }
        #ui-right { top: 20px; right: 20px; width: 280px; cursor: pointer; }
        h2 { font-family: 'Orbitron'; font-size: 12px; color: var(--neon); letter-spacing: 2px; }
        .stat { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 6px; border-bottom: 1px solid rgba(0,255,204,0.1); }
        .val { font-weight: 700; color: #fff; }
        button { background: var(--neon); color: #000; border: none; padding: 15px; width: 100%; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; margin-top: 10px; }
        #graph-panel { display: none; position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; background: #050505; border: 2px solid #fff; padding: 20px; z-index: 1000; }
        .bar { background: var(--neon); width: 25px; margin-right: 5px; transition: height 0.5s; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>CENTRAL CORE | {{ bid }}</h2>
        <div class="stat">DÍA: <span class="val">{{ d }} / 7</span></div>
        <div class="stat">BIOMASA: <span class="val">{{ inv.crecimiento }} CM</span></div>
        <div class="stat">PESO: <span class="val">{{ inv.peso }} KG</span></div>
        <button onclick="playBeep(); location.href='/next'">AVANZAR CICLO</button>
        <button style="background:#222; color:#666; margin-top:5px;" onclick="location.href='/?reset=1'">RESET</button>
    </div>

    <div id="ui-right" class="hud" onclick="document.getElementById('graph-panel').style.display='block'">
        <h2>TELEMETRÍA (CLICK)</h2>
        <div class="stat">H2O SAVE: <span class="val">{{ pot.h2o_save }} L</span></div>
        <div class="stat">CO2 REDUCIDO: <span class="val">{{ pot.ch4 }} KG</span></div>
        <div class="stat">HUMEDAD: <span class="val">{{ inv.hum }}%</span></div>
    </div>

    <div id="graph-panel" onclick="this.style.display='none'">
        <h2>AHORRO HÍDRICO (LITROS)</h2>
        <div style="display:flex; align-items:flex-end; height:150px;">
            {% for i in range(d + 1) %}<div class="bar" style="height:{{ i * 20 + 10 }}px;"></div>{% endfor %}
        </div>
        <p style="font-size:10px; margin-top:10px;">Total: {{ pot.h2o_save }} L. Click para cerrar.</p>
    </div>

    <script>
        // --- AUDIO ENGINE ---
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playPumpSound() {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'sawtooth'; osc.frequency.setValueAtTime(40, audioCtx.currentTime);
            gain.gain.setValueAtTime(0.02, audioCtx.currentTime);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }
        function playBeep() {
            const osc = audioCtx.createOscillator();
            osc.type = 'sine'; osc.frequency.setValueAtTime(880, audioCtx.currentTime);
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
            osc.stop(audioCtx.currentTime + 0.2);
        }

        // --- THREE.JS SCENE ---
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // TORRE CON EXOESQUELETO NEÓN
        const tower = new THREE.Group();
        const beamMat = new THREE.MeshStandardMaterial({color: 0x111111, metalness: 1});
        const neonMat = new THREE.MeshBasicMaterial({color: 0x00ffcc});
        for(let x of [-3.5, 3.5]) {
            for(let z of [-3.5, 3.5]) {
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.3, 25, 0.3), beamMat);
                beam.position.set(x, 4, z); tower.add(beam);
                const glow = new THREE.Mesh(new THREE.BoxGeometry(0.05, 25.1, 0.05), neonMat);
                glow.position.set(x, 4, z); tower.add(glow);
            }
        }
        
        const floors = [];
        for(let i=0; i<10; i++){
            const h = i * 2.5 - 8;
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.1, 6.5), beamMat);
            floor.position.y = h;
            const grassH = ({{ d }} * 0.3) + 0.1;
            const grass = new THREE.Mesh(new THREE.BoxGeometry(6, grassH, 6), new THREE.MeshStandardMaterial({color: ({{d}}==0?0x3d2b1f:0x00ff44)}));
            grass.position.y = h + grassH/2;
            tower.add(floor, grass);
            floors.push(h);
        }
        scene.add(tower);

        // BRAZO ROBÓTICO (IK SIM)
        const robot = new THREE.Group();
        const base = new THREE.Mesh(new THREE.BoxGeometry(1, 0.5, 1), beamMat);
        const arm1 = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 2), neonMat);
        arm1.position.y = 1; arm1.rotation.z = Math.PI/4;
        robot.add(base, arm1);
        scene.add(robot);

        // GOTEO
        const drips = new THREE.Group();
        for(let i=0; i<20; i++) {
            const d = new THREE.Mesh(new THREE.SphereGeometry(0.03), new THREE.MeshBasicMaterial({color:0x00ffff}));
            drips.add(d);
        }
        scene.add(drips);

        scene.add(new THREE.AmbientLight(0xffffff, 0.5));
        const pLight = new THREE.PointLight(0x00ffcc, 1, 50); pLight.position.set(5,10,5); scene.add(pLight);

        function animate() {
            requestAnimationFrame(animate);
            const t = Date.now() * 0.001;
            if ({{ d }} < 7) {
                const ty = floors[{{ d }}];
                camera.position.lerp(new THREE.Vector3(-12, ty + 4, 12), 0.05);
                camera.lookAt(0, ty, 0);
                robot.position.set(-4.5, ty + 1, Math.sin(t)*2);
                arm1.rotation.y = Math.sin(t*2);
                drips.children.forEach((d, i) => {
                    d.position.set(Math.sin(i)*2.5, ty + 2 - ((t+i*0.2)%1)*2, Math.cos(i)*2.5);
                });
                if(Math.random() > 0.95) playPumpSound();
            } else {
                camera.position.lerp(new THREE.Vector3(40, 15, 40), 0.02);
                camera.lookAt(15, -5, 0);
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