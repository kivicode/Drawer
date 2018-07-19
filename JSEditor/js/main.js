
var prevmesh = null
var tryit = codemirror.getInputField();
var timeout = null;
var viewer = new Viewer(new CSG(), window.innerWidth, 480, 10);
// viewer.setDepth(5);
var dep = 5;
addViewer(viewer);
function rebuild() {
  var error = document.getElementById('error');
  // console.error(codemirror.getValue().split("Poly{")[1].split("}")[0])
  try {
    // setScale(10)
    var solid = new Function(codemirror.getValue())();
    error.innerHTML = '';
    var m = eval(solid).toMesh()
    saveGCode(m)
    viewer.mesh = m;
    viewer.gl.ondraw();
  } catch (e) {
    error.innerHTML = 'Error: <code>' + e.toString().replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</code>';
  }
}

function stringifyVertex(vec){
  try{
    return "vertex X"+vec[0]+" Y"+vec[1]+" Z"+vec[2]+" \n";
  } catch (e) {
    return ""
  }
}

// Use FileSaver.js 'saveAs' function to save the string
function saveGCode(geometry){  
  var trias = geometry.triangles
  var verts = geometry.vertices
  var stlOut = ""
  verts.forEach(function(v){
    stlOut += "v " + toTextS(v, 3, 100)
  })

  trias.forEach(function(f){
    stlOut += "f " + toTextS(f, 0)
  })
  // var polys = geometry.polygons;
  // var stlOut = "M3 F100\nG10 L1 P1 R0.5\nT1\nG40\nG1 B0\n";
  // // console.log(polys)
  // polys.forEach(function(poly){
  //   var verts = poly.vertices;
  //   var normal = verts[1].normal
  //   stlOut += "G0 X" + toTextG(verts[0].pos)
  //   verts.forEach(function(vert){
  //     var pos = vert.pos;
  //     stlOut += "G1 X" + toTextG(pos)
  //   })
  // })
  // stlOut += "M30"
  console.log(stlOut)
}

function saveSTL(geometry){  
  var polys = geometry.toPolygons()//.polygons;
  // console.log(polys)
  var stlOut = "solid Ball\n";
  polys.forEach(function(p){
    var normal = p.plane.normal
    var verts = p.vertices
    stlOut += "facet normal " + toTextS(normal) + "outer loop\n"
    verts.forEach(function(pp){
      stlOut += "vertex " + toTextS(pp.pos)
    })
    stlOut += "endloop\nendfacet\n\n"
    console.log(stlOut)
    console.log(stlOut + "endsolid Ball")
  })
  // var stlOut = "solid Ball\n";
  // // console.log(polys)
  // polys.forEach(function(poly){
  //   var verts = poly.vertices;
  //   var normal = verts[1].normal
  //   stlOut += "facet normal " + toTextS(normal) + "outer loop\n"
  //   verts.forEach(function(vert){
  //     var pos = vert.pos;
  //     stlOut += "vertex " + toTextS(pos)
  //   })
  //   stlOut += "endloop\nendfacet\n\n"
  // })
  // console.log(stlOut + "endsolid Ball")
}

function toTextG(v){
  return (v.x.toFixed(3)*10+50) + " Y" + (v.y.toFixed(3)*10+50) + " Z" + (v.z.toFixed(3)*10+10) + "\n";
}

function toTextS(v, fix=3, mult=1){
  return (v[0].toFixed(fix)*mult) + " " + (v[1].toFixed(fix)*mult) + " " + (v[2].toFixed(fix)*mult) + "\n";
}

function toSTL(){
  // var geom = viewer.mesh.computeWireframe().vertices
  // var e = Cube(1);
  // for(var i = 0; i < geom.length-1; i+=2){
  //   var v = geom[i], v2 = geom[i+1];
  //   e=e.add(Cylinder([(v[0]*100).toFixed(0), (v[1]*100).toFixed(0), (v[2]*100).toFixed(0)], [(v2[0]*100).toFixed(0), (v2[1]*100).toFixed(0), (v2[2]*100).toFixed(0)], 10))
  // }

  // // return Sphere(0).add(Cylinder([0, 100, 0], [35, 92, 15], 10).add(Cylinder([38, 92, 0], [65, 71, 27], 10).add(Cylinder([71, 71, 0], [85, 38, 35], 10).add(Cylinder([92, 38, 0], [92, 0, 38], 10).add(Cylinder([100, 0, 0], [85, -38, 35], 10).add(Cylinder([92, -38, 0], [65, -71, 27], 10).add(Cylinder([71, -71, 0], [35, -92, 15], 10).add(Cylinder([38, -92, 0], [0, -100, 0], 10).add(Cylinder([27, 92, 27], [50, 71, 50], 10).add(Cylinder([65, 38, 65], [71, 0, 71], 10).add(Cylinder([65, -38, 65], [50, -71, 50], 10).add(Cylinder([27, -92, 27], [0, -100, 0], 10).add(Cylinder([15, 92, 35], [27, 71, 65], 10).add(Cylinder([35, 38, 85], [38, 0, 92], 10).add(Cylinder([35, -38, 85], [27, -71, 65], 10).add(Cylinder([15, -92, 35], [0, -100, 0], 10).add(Cylinder([0, 92, 38], [0, 71, 71], 10).add(Cylinder([0, 38, 92], [0, 0, 100], 10).add(Cylinder([0, -38, 92], [0, -71, 71], 10).add(Cylinder([0, -92, 38], [0, -100, 0], 10).add(Cylinder([-15, 92, 35], [-27, 71, 65], 10).add(Cylinder([-35, 38, 85], [-38, 0, 92], 10).add(Cylinder([-35, -38, 85], [-27, -71, 65], 10).add(Cylinder([-15, -92, 35], [0, -100, 0], 10).add(Cylinder([-27, 92, 27], [-50, 71, 50], 10).add(Cylinder([-65, 38, 65], [-71, 0, 71], 10).add(Cylinder([-65, -38, 65], [-50, -71, 50], 10).add(Cylinder([-27, -92, 27], [-0, -100, 0], 10).add(Cylinder([-35, 92, 15], [-65, 71, 27], 10).add(Cylinder([-85, 38, 35], [-92, 0, 38], 10).add(Cylinder([-85, -38, 35], [-65, -71, 27], 10).add(Cylinder([-35, -92, 15], [-0, -100, 0], 10).add(Cylinder([-38, 92, 0], [-71, 71, 0], 10).add(Cylinder([-92, 38, 0], [-100, 0, 0], 10).add(Cylinder([-92, -38, 0], [-71, -71, 0], 10).add(Cylinder([-38, -92, 0], [-0, -100, 0], 10).add(Cylinder([-35, 92, -15], [-65, 71, -27], 10).add(Cylinder([-85, 38, -35], [-92, 0, -38], 10).add(Cylinder([-85, -38, -35], [-65, -71, -27], 10).add(Cylinder([-35, -92, -15], [-0, -100, 0], 10).add(Cylinder([-27, 92, -27], [-50, 71, -50], 10).add(Cylinder([-65, 38, -65], [-71, 0, -71], 10).add(Cylinder([-65, -38, -65], [-50, -71, -50], 10).add(Cylinder([-27, -92, -27], [-0, -100, -0], 10).add(Cylinder([-15, 92, -35], [-27, 71, -65], 10).add(Cylinder([-35, 38, -85], [-38, 0, -92], 10).add(Cylinder([-35, -38, -85], [-27, -71, -65], 10).add(Cylinder([-15, -92, -35], [-0, -100, -0], 10).add(Cylinder([-0, 92, -38], [-0, 71, -71], 10).add(Cylinder([-0, 38, -92], [-0, 0, -100], 10).add(Cylinder([-0, -38, -92], [-0, -71, -71], 10).add(Cylinder([-0, -92, -38], [-0, -100, -0], 10).add(Cylinder([15, 92, -35], [27, 71, -65], 10).add(Cylinder([35, 38, -85], [38, 0, -92], 10).add(Cylinder([35, -38, -85], [27, -71, -65], 10).add(Cylinder([15, -92, -35], [-0, -100, -0], 10).add(Cylinder([27, 92, -27], [50, 71, -50], 10).add(Cylinder([65, 38, -65], [71, 0, -71], 10).add(Cylinder([65, -38, -65], [50, -71, -50], 10).add(Cylinder([27, -92, -27], [0, -100, -0], 10).add(Cylinder([35, 92, -15], [65, 71, -27], 10).add(Cylinder([85, 38, -35], [92, 0, -38], 10).add(Cylinder([85, -38, -35], [65, -71, -27], 10).add(Cylinder([35, -92, -15], [0, -100, -0], 10).add(Cylinder([38, 92, -0], [71, 71, -0], 10).add(Cylinder([92, 38, -0], [100, 0, -0], 10).add(Cylinder([92, -38, -0], [71, -71, -0], 10).add(Cylinder([38, -92, -0], [0, -100, -0], 10)
  // try{
  //   console.log(e)
  // viewer.mesh = e.toMesh();
  // viewer.gl.ondraw();
  // } catch (e) {
  //   error.innerHTML = 'Error: <code>' + e.toString().replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</code>';
  // }
}

var canvas = document.getElementsByTagName("canvas")[0]
var ctx = canvas.getContext("2d");
// document.body.addEventListener("wheel", alert(""));
Number.prototype.map = function (in_min, in_max, out_min, out_max) {
  return (this - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function keyDownTextField(e) {
var keyCode = e.keyCode;
  if([17, 91, 93].includes(keyCode)) {
    if (timeout) clearTimeout(timeout);
      timeout = setTimeout(rebuild, 0);
    }
}

function setScale(sc){
viewer.gl.translate(0,0,10)
}
rebuild();
rebuild();

document.addEventListener("keydown", keyDownTextField);
var del = 100;


function Cylinder(start=[-1, 0, 0], end=[1, 0, 0], radius){
  return CSG.cylinder({
    radius: radius/del,
    start: start,
    end: end
  });
}

function SphereC(center, radius){
  return CSG.sphere({
    center: [center[0]/del, center[1]/del, center[2]/del],
    radius: (radius/del)
  });
}

function Sphere(radius){
  return CSG.sphere({
    slices: 16,
    stacks: 8,
    center: [0, 0, 0],
    radius: (radius/del)
  });
}

function Cube(center, radius){
  return CSG.cube({
    center: center,
    radius: (radius/del)
  });
}

function Cube(radius){
  return CSG.cube({
    center: [0, 0, 0],
    radius: (radius/del)
  });
}

function Plane(w, h){
  return CSG.plane({
    center: [0, 0, 0],
    w: w/100,
    h: h/100
    // radius: (radius/del)
  });
}