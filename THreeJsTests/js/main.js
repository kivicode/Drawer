var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 );

var renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );
camera.position.z = 5;



var line = line(2, 2, 2, 0, 0, 0, 1, 1, 1)
var cube = box(0, 0, 0, 1, 1, 1)

animate();