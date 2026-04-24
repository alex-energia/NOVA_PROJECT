import random
from flask import Flask, render_template_string, request

app = Flask(__name__)

class ControladorNOVA:
    def __init__(self):
        self.reset()

    def reset(self):
        self.dia = 0
        self.batch_id = f"NOVA-B21-{random.randint(100,999)}"
        self.inv = {
            "ph": 5.9, "ce": 1.8, "co2": 450, "tanque": 100,
            "presion": 45.0, "peso": 12.0, "crecimiento": 0
        }
        self.pot = {"h2o_save": 0, "ch4": 0}
        self.receta = {"Maíz": "105kg", "Cebada": "15kg", "Avena": "10kg"}

    def update(self):
        if self.dia < 7:
            self.dia += 1
            self.inv["crecimiento"] = round(self.dia * 4.3, 1)
            self.inv["peso"] = round(12.0 + (self.dia * 9.5), 1)
            self.pot["h2o_save"] += 850
        else:
            self.reset()

ctrl = ControladorNOVA()

@app.route('/')
def index():
    if request.args.get('reset'): ctrl.reset()
    return render_template_string(HTML_V21, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

@app.route('/next')
def next_step():
    ctrl.update()
    return render_template_string(HTML_V21, d=ctrl.dia, inv=ctrl.inv, pot=ctrl.pot, rec=ctrl.receta, bid=ctrl.batch_id)

HTML_V21 = """
<!DOCTYPE html>
<html>
<head>
    <title>NOVA v21 | Glass & Autonomous Fodder</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root { --neon: #00ffcc; --bg: #030303; --glass-tinte: rgba(0, 255, 204, 0.1); }
        body { margin: 0; background: var(--bg); color: white; font-family: 'Inter', sans-serif; overflow: hidden; }
        .hud { position: absolute; background: rgba(5, 15, 15, 0.95); border: 2px solid var(--neon); padding: 20px; z-index: 100; backdrop-filter: blur(10px); }
        #ui-left { top: 20px; left: 20px; width: 340px; }
        #ui-right { top: 20px; right: 20px; width: 300px; }
        h2 { font-family: 'Orbitron'; font-size: 13px; color: var(--neon); letter-spacing: 2px; text-transform: uppercase; margin: 0 0 15px 0; border-bottom: 1px solid #333; }
        .stat { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 8px; }
        .val { font-weight: 700; color: #fff; }
        button { background: var(--neon); color: #000; border: none; padding: 16px; width: 100%; font-family: 'Orbitron'; font-weight: 900; cursor: pointer; margin-top: 10px; transition: 0.3s; }
        button:hover { background: #fff; box-shadow: 0 0 30px var(--neon); }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="ui-left" class="hud">
        <h2>CENTRAL CONTROL | {{ bid }}</h2>
        <div class="stat">CICLO: <span class="val">DÍA {{ d }} / 7</span></div>
        <div class="stat">PESO EN BANDEJA: <span class="val">{{ inv.peso }} KG</span></div>
        <button onclick="location.href='/next'">{{ "SIGUIENTE FASE" if d < 7 else "REINICIAR LOTE" }}</button>
        <button style="background:#111; color:#555; margin-top:5px;" onclick="location.href='/?reset=1'">RESET</button>
    </div>

    <div id="ui-right" class="hud">
        <h2>DATA STREAM</h2>
        <div class="stat">CRECIMIENTO: <span class="val">{{ inv.crecimiento }} CM</span></div>
        <div class="stat">TANQUE AGUA: <span class="val">{{ inv.tanque }}%</span></div>
        <div class="stat">H2O SAVE: <span class="val">{{ pot.h2o_save }} L</span></div>
    </div>

    <script>
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth/window.innerHeight, 0.1, 2000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // --- ILUMINACIÓN (MEJORADA PARA VISIBILIDAD) ---
        scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 0.6));
        const dirLight = new THREE.DirectionalLight(0xffffff, 1);
        dirLight.position.set(10, 20, 10);
        scene.add(dirLight);

        // --- ENTORNO ---
        const grid = new THREE.GridHelper(100, 50, 0x00ffcc, 0x111111);
        grid.position.y = -8;
        scene.add(grid);

        // --- TORRE SCADA (MATERIALES MEJORADOS) ---
        const towerGroup = new THREE.Group();
        const frameMat = new THREE.MeshStandardMaterial({color: 0x444444, metalness: 0.9, roughness: 0.1});
        const glassMat = new THREE.MeshPhysicalMaterial({
            color: 0x00ffcc, metalness: 0.2, roughness: 0.05, transmission: 0.95, transparent: true, opacity: 0.2
        });

        const floors = [];
        const doors = [];

        for(let i=0; i<10; i++){
            const h = i * 2.5 - 8;
            const floorGroup = new THREE.Group();
            
            // Estructura de Piso
            const floor = new THREE.Mesh(new THREE.BoxGeometry(6.5, 0.2, 6.5), frameMat);
            floor.position.y = h;
            floorGroup.add(floor);

            // Forraje
            const grassH = ({{ d }} * 0.3) + 0.1;
            const grassMat = new THREE.MeshStandardMaterial({color: ({{d}}==0 ? 0x3d2b1f : 0x00ff66)});
            const grass = new THREE.Mesh(new THREE.BoxGeometry(6, grassH, 6), grassMat);
            grass.position.y = h + grassH/2 + 0.1;
            floorGroup.add(grass);

            // PUERTAS DE CRISTAL (Dos hojas por nivel)
            const doorGroup = new THREE.Group();
            const doorGeo = new THREE.BoxGeometry(3.2, 2.3, 0.1);
            const doorL = new THREE.Mesh(doorGeo, glassMat);
            doorL.position.set(-1.6, h + 1.25, 3.2);
            const doorR = new THREE.Mesh(doorGeo, glassMat);
            doorR.position.set(1.6, h + 1.25, 3.2);
            doorGroup.add(doorL, doorR);
            scene.add(doorGroup);
            doors.push({group: doorGroup, left: doorL, right: doorR});

            towerGroup.add(floorGroup);
            floors.push(h);
        }
        
        // Vigas Maestro (Visibles)
        for(let x of [-3.2, 3.2]) {
            for(let z of [-3.2, 3.2]) {
                const beam = new THREE.Mesh(new THREE.BoxGeometry(0.3, 25, 0.3), frameMat);
                beam.position.set(x, 4.5, z);
                towerGroup.add(beam);
            }
        }
        scene.add(towerGroup);

        // --- ANIMAL AUTÓNOMO (MEJORADO) ---
        const animal = new THREE.Group();
        const cBody = new THREE.Mesh(new THREE.CapsuleGeometry(0.8, 2.2, 12, 24), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        cBody.rotation.z = Math.PI/2;
        const cHead = new THREE.Mesh(new THREE.SphereGeometry(0.6, 24, 24), new THREE.MeshStandardMaterial({color: 0x3d2b1f}));
        cHead.position.set(2, 0.8, 0);
        animal.add(cBody, cHead);
        animal.position.set(40, -7.2, 0); // Posición inicial lejana
        scene.add(animal);

        // --- LOGÍSTICA (BANDA Y COMEDERO) ---
        const conveyor = new THREE.Mesh(new THREE.BoxGeometry(30, 0.3, 4), new THREE.MeshStandardMaterial({color: 0x111111}));
        conveyor.position.set(18, -7.8, 0);
        scene.add(conveyor);

        const comedero = new THREE.Mesh(new THREE.BoxGeometry(5, 1, 4), new THREE.MeshStandardMaterial({color: 0x222222}));
        comedero.position.set(30, -7.5, 0);
        scene.add(comedero);

        const trayHarvest = new THREE.Mesh(new THREE.BoxGeometry(3, 0.2, 3), new THREE.MeshStandardMaterial({color: 0x00ff66}));
        trayHarvest.position.set(5, -7.6, 0);
        trayHarvest.visible = ({{ d }} == 7);
        scene.add(trayHarvest);

        camera.position.set(30, 15, 30);

        function animate() {
            requestAnimationFrame(animate);
            const time = Date.now() * 0.001;

            if ({{ d }} == 0) {
                // VISTA GLOBAL AL INICIO
                camera.position.lerp(new THREE.Vector3(45, 20, 45), 0.02);
                camera.lookAt(0, 0, 0);
                doors.forEach(d => {
                    d.left.position.lerp(new THREE.Vector3(-1.6, d.left.position.y, 3.2), 0.1);
                    d.right.position.lerp(new THREE.Vector3(1.6, d.right.position.y, 3.2), 0.1);
                });
            } else if ({{ d }} < 7) {
                // ZOOM A BANDEJA Y ABRIR PUERTA
                const ty = floors[{{ d }}];
                camera.position.lerp(new THREE.Vector3(-12, ty + 4, 12), 0.05);
                camera.lookAt(0, ty, 0);
                
                const activeDoor = doors[{{ d }}];
                activeDoor.left.position.lerp(new THREE.Vector3(-4.8, activeDoor.left.position.y, 3.2), 0.1);
                activeDoor.right.position.lerp(new THREE.Vector3(4.8, activeDoor.right.position.y, 3.2), 0.1);
                
                // Cerrar las otras
                doors.forEach((d, idx) => {
                    if(idx != {{ d }}){
                        d.left.position.lerp(new THREE.Vector3(-1.6, d.left.position.y, 3.2), 0.1);
                        d.right.position.lerp(new THREE.Vector3(1.6, d.right.position.y, 3.2), 0.1);
                    }
                });

            } else {
                // DÍA 7: LOGÍSTICA AUTÓNOMA
                camera.position.lerp(new THREE.Vector3(50, 10, 20), 0.02);
                camera.lookAt(25, -5, 0);

                // Bandeja viaja
                if(trayHarvest.position.x < 29) trayHarvest.position.x += 0.2;

                // Animal camina al comedero
                if(animal.position.x > 32) {
                    animal.position.x -= 0.12;
                    cBody.rotation.z = Math.PI/2 + Math.sin(time*10)*0.1; // Camina
                } else {
                    // Come
                    cHead.rotation.x = Math.sin(time*8)*0.2;
                }
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
