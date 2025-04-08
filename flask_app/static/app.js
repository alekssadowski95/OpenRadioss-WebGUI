import * as THREE from './three.min.js'
import {STLLoader} from './STLLoader.js';
import {OrbitControls} from './OrbitControls.js';


const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera( 35, (window.innerWidth) / (window.innerHeight), 0.1, 1000 );
//scene.background = new THREE.Color().setHex( 0x222222 );


const renderer = new THREE.WebGLRenderer({ alpha: true } );
renderer.setSize( window.innerWidth, window.innerHeight );
var rendererElement = document.body.appendChild( renderer.domElement );

const controls = new OrbitControls( camera, renderer.domElement );
controls.enableZoom = true
controls.enablePan = true
controls.enableDamping = true
controls.dampingFactor = 0.6

/** 

// Load Light
var ambientLight = new THREE.AmbientLight(0xfff, 1);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1)
directionalLight.position.z = 100
scene.add(directionalLight)
*/

const loader = new THREE.FileLoader();

const gradient = [
	0x3c00f5,
	0x3a55f5,
	0x30b3f9,
	0x0cf9e6,
	0x00f994,
	0x00fb54,
	0x00fb49,
	0x81fb4b,
	0xe1fe53,
	0xfbbf44,
	0xfd7035,
	0xfd442e
]

//load a text file and output the result to the console
loader.load(
	// resource URL
	URL_OF_VTK_FILE,

	// onLoad callback
	function ( data ) {
		let points = [];
		let cells = [];
		let cellTypes = [];
		let mises = [];

		// output the text to the console
		const lines = data.split("\n");
		for (let i = 0; i < lines.length; i++) {
			if (lines[i].startsWith('DATASET')) {
				if (lines[i].includes('UNSTRUCTURED_GRID')) {
					console.log('Loaded file is an UNSTRUCTURED_GRID');
					continue;
				} else {
					console.error('Unsupported DATASET type:', lines[i]);
					break;
				}
			}

			let mode = null;
    
			for (let j = 0; j < lines.length; j++) {
				let line = lines[j].trim();
				if (line.startsWith('POINTS')) {
					mode = 'POINTS';
					continue;
				} else if (line.startsWith('CELLS')) {
					mode = 'CELLS';
					continue;
				} else if (line.startsWith('CELL_TYPES')) {
					mode = 'CELL_TYPES';
					continue;
				} else if (line == '') {
					mode = 'NONE'
					continue;
				} else if (line.startsWith('SCALARS 3DELEM_Von_Mises')) {
					mode = '3D_VON_MISES';
					j++;
					continue;
				} else if (line.startsWith('POINT_DATA') || line.startsWith('SCALARS') || line.startsWith('VECTORS')) {
					mode = 'NONE'
					continue;
				}
				
				if (mode === 'POINTS') {
					let coords = line.split(/\s+/).map(Number);
					points.push(coords);
				} else if (mode === 'CELLS') {
					let cellData = line.split(/\s+/).map(Number);
					cellData.shift(); // Remove first number (cell size)
					cells.push(cellData);
				} else if (mode === 'CELL_TYPES') {
					cellTypes.push(Number(line));
				} else if (mode === '3D_VON_MISES') {
					mises.push(Number(line));
				}
				else if (mode === 'NONE') {}
			}
			break;
		}
		// after loading to memory
		//console.log('Points:', points);
		//console.log('Cells:', cells);
		//console.log('Cell Types:', cellTypes);
		//console.log('3D Von Mises:', mises);
		console.log('Von Mises (max)', Math.max(...mises))
		console.log('Von Mises (min)', Math.min(...mises))

		let segments = gradient.length;
		let vertices = Array.from({ length: segments }, () => []);
		let indices = Array.from({ length: segments }, () => []);
		let newPointIds = new Array(segments).fill(0);
		let misesMax = Math.max(...mises);
		let misesMin = Math.min(...mises);

		//console.log('vertices:', vertices);
		//console.log('indices:', indices);
		//console.log('newPointIds:', newPointIds);

		let misesRange = misesMax - misesMin;
		let misesIntervall = misesRange / segments;
		
		// Looping over all cell types
		for (let i = 0; i < cells.length; i++) {
			// Cell - Tetrahedron
			if (cellTypes[i] == 10) {
				let cellMises = mises[i];

				let verticesTemp = [];
				let indicesTemp = [];
				let bracket = 0;

				for (let j = 0; j < segments; j++) {
					if (cellMises >= misesMin + misesIntervall * j) {
						bracket = j;
					}
				}

				// Triangle 1 (0, 1, 2)
				verticesTemp.push(points[cells[i][0]][0]);
				verticesTemp.push(points[cells[i][0]][1]);
				verticesTemp.push(points[cells[i][0]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][1]][0]);
				verticesTemp.push(points[cells[i][1]][1]);
				verticesTemp.push(points[cells[i][1]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][2]][0]);
				verticesTemp.push(points[cells[i][2]][1]);
				verticesTemp.push(points[cells[i][2]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				// Triangle 1 - reversed
				verticesTemp.push(points[cells[i][2]][0]);
				verticesTemp.push(points[cells[i][2]][1]);
				verticesTemp.push(points[cells[i][2]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][1]][0]);
				verticesTemp.push(points[cells[i][1]][1]);
				verticesTemp.push(points[cells[i][1]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][0]][0]);
				verticesTemp.push(points[cells[i][0]][1]);
				verticesTemp.push(points[cells[i][0]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;

				// Triangle 2 (0, 2, 3)
				verticesTemp.push(points[cells[i][0]][0]);
				verticesTemp.push(points[cells[i][0]][1]);
				verticesTemp.push(points[cells[i][0]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][2]][0]);
				verticesTemp.push(points[cells[i][2]][1]);
				verticesTemp.push(points[cells[i][2]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][3]][0]);
				verticesTemp.push(points[cells[i][3]][1]);
				verticesTemp.push(points[cells[i][3]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				// Triangle 2 - reversed
				verticesTemp.push(points[cells[i][3]][0]);
				verticesTemp.push(points[cells[i][3]][1]);
				verticesTemp.push(points[cells[i][3]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][2]][0]);
				verticesTemp.push(points[cells[i][2]][1]);
				verticesTemp.push(points[cells[i][2]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][0]][0]);
				verticesTemp.push(points[cells[i][0]][1]);
				verticesTemp.push(points[cells[i][0]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				
				// Triangle 3 (0, 1, 3)
				verticesTemp.push(points[cells[i][0]][0]);
				verticesTemp.push(points[cells[i][0]][1]);
				verticesTemp.push(points[cells[i][0]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][1]][0]);
				verticesTemp.push(points[cells[i][1]][1]);
				verticesTemp.push(points[cells[i][1]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][3]][0]);
				verticesTemp.push(points[cells[i][3]][1]);
				verticesTemp.push(points[cells[i][3]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				// Triangle 3 - reversed
				verticesTemp.push(points[cells[i][3]][0]);
				verticesTemp.push(points[cells[i][3]][1]);
				verticesTemp.push(points[cells[i][3]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][1]][0]);
				verticesTemp.push(points[cells[i][1]][1]);
				verticesTemp.push(points[cells[i][1]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][0]][0]);
				verticesTemp.push(points[cells[i][0]][1]);
				verticesTemp.push(points[cells[i][0]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;

				// Triangle 4 (1, 2, 3)
				verticesTemp.push(points[cells[i][1]][0]);
				verticesTemp.push(points[cells[i][1]][1]);
				verticesTemp.push(points[cells[i][1]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][2]][0]);
				verticesTemp.push(points[cells[i][2]][1]);
				verticesTemp.push(points[cells[i][2]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][3]][0]);
				verticesTemp.push(points[cells[i][3]][1]);
				verticesTemp.push(points[cells[i][3]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				// Triangle 4 - reversed
				verticesTemp.push(points[cells[i][3]][0]);
				verticesTemp.push(points[cells[i][3]][1]);
				verticesTemp.push(points[cells[i][3]][2]); // 1. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][2]][0]);
				verticesTemp.push(points[cells[i][2]][1]);
				verticesTemp.push(points[cells[i][2]][2]); // 2. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;
				verticesTemp.push(points[cells[i][1]][0]);
				verticesTemp.push(points[cells[i][1]][1]);
				verticesTemp.push(points[cells[i][1]][2]); // 3. Point (x, y, z)
				indicesTemp.push(newPointIds[bracket]);
				newPointIds[bracket] = newPointIds[bracket] + 1;

				for (let vert of verticesTemp) {
					vertices[bracket].push(vert)
				}

				for (let ind of indicesTemp) {
					indices[bracket].push(ind)
				}
			}
		}

		const meshGroup = new THREE.Group();

		for (let k = 0; k < segments; k++) {
			let geometry = new THREE.BufferGeometry();
			geometry.setIndex( indices[k] );
			geometry.setAttribute( 'position', new THREE.Float32BufferAttribute( vertices[k], 3 ) );
			geometry.computeVertexNormals();

			let material_wire = new THREE.MeshBasicMaterial( { color: 0x000000, wireframe: true, opacity: 0.04, transparent: true } );

			let material_fill = new THREE.MeshBasicMaterial( { color: gradient[k], polygonOffset: true, polygonOffsetFactor: 1, polygonOffsetUnits: 1 } );
			material_wire.polygonOffset = true;
			material_wire.depthTest = true;

			let mesh_wire = new THREE.Mesh( geometry, material_wire );
			let mesh_fill = new THREE.Mesh( geometry, material_fill );

			meshGroup.add(mesh_wire)
			meshGroup.add(mesh_fill)
			scene.add(meshGroup);
			

			// Compute bounding box
			const box3 = new THREE.Box3().setFromObject(meshGroup);
			const center = new THREE.Vector3();
			box3.getCenter(center);

			// Move group to center
			meshGroup.matrixAutoUpdate = false;
			meshGroup.position.sub(center);
			meshGroup.updateMatrix();
		}
		var viewerLegend = document.getElementById('viewer-legend');
		viewerLegend.style.display = "block";
		viewerLegend.innerHTML = "";
		var trTemp = viewerLegend.appendChild(document.createElement("tr"));
		trTemp.innerHTML = '<tr><td style="padding-bottom: 16px;" colspan="3">S, Mises</td></tr>';

		for (let k = segments; k > 0; k--) {
			var trTemp = viewerLegend.appendChild(document.createElement("tr"));
			if (k == segments){
				trTemp.innerHTML = `<td style="background-color: #${gradient[k-1].toString(16).padStart(6, '0')}; height: 20px; width: 30px; border-style: solid; border-width: 1px; border-color:#222222;"></td>
				<td style="width: 10px; border-top: 1px solid #000000; border-bottom: 1px solid #000000"></td>
				<td style="position: relative; padding-left: 6px; width: 120px;"><span style="position: absolute; top: -10px;">${misesMax.toPrecision(8)} Max</span></td>`;
			} else {
				trTemp.innerHTML = `<td style="background-color: #${gradient[k-1].toString(16).padStart(6, '0')}; height: 20px; width: 30px; border-style: solid; border-width: 1px; border-color:#222222;"></td>
				<td style="width: 10px; border-top: 1px solid #000000; border-bottom: 1px solid #000000"></td>
				<td style="position: relative; padding-left: 6px; width: 120px;"><span style="position: absolute; top: -10px;">${(k * misesIntervall + misesMin).toPrecision(8)}</span></td>`;
			}
		}
		var trMin = viewerLegend.appendChild(document.createElement("tr"));
		trMin.innerHTML = `<td style="height: 20px; width: 30px;"></td>
				<td style="width: 10px;"></td>
				<td style="position: relative; padding-left: 6px; width: 120px;"><span style="position: absolute; top: -10px;">${misesMin.toPrecision(8)} Min</span></td>`;
	},

	// onProgress callback
	function ( xhr ) {
		console.log( (xhr.loaded / xhr.total * 100) + '% loaded' );
	},

	// onError callback
	function ( err ) {
		console.error( 'An error happened' );
	}
);
camera.position.x = -getScaleVal();
camera.position.z = -getScaleVal();
camera.position.y = -getScaleVal();

function getScaleVal(){
	const windowWidth = window.innerWidth
	let scale = 0.8
	if(windowWidth > 400){
		scale = 0.5
	}
	if(windowWidth > 500){
		scale = 0.4
	}
	if(windowWidth > 600){
		scale = 0.3
	}
	if(windowWidth > 700){
		scale = 0.2
	}
	if(windowWidth > 1000){
		scale = 0.08
	}

	return -windowWidth*scale
}

function animate() {
	requestAnimationFrame( animate );
	renderer.render( scene, camera );
    controls.update()
}

function onWindowResize(){
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize( window.innerWidth, window.innerHeight );
}

animate();
window.addEventListener( 'resize', onWindowResize, false );