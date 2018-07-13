function box(x, y, z, a, b, c, color=0xffffff){
	var geometry = new THREE.BoxGeometry( 1, 1, 1 );
	var material = new THREE.MeshBasicMaterial( { color: color } );
	var cube = new THREE.Mesh( geometry, material );
	cube.position.x = x
	cube.position.y = y
	cube.position.z = z
	scene.add(cube);
	return cube
}

function line(ax, ay, az, bx, by, bz, cx, cy, cz, color=0xffffff){
	var geometry = new THREE.Geometry();
	var material = new THREE.LineBasicMaterial( { color: color } );
	geometry.vertices.push(new THREE.Vector3( ax, ay, az) );
	geometry.vertices.push(new THREE.Vector3( bx, by, bz ) );
	geometry.vertices.push(new THREE.Vector3( cx, cy, cz) );
	var line = new THREE.Line( geometry, material );
	scene.add(line)
	return line
}
var animate = function () {
	requestAnimationFrame( animate );

	cube.rotation.x += 0.01;
	cube.rotation.y += 0.01;

	renderer.render( scene, camera );
};