class Shape {
  Polygon data;
  Polygon subpoly;
  int id = nodes.size();
  boolean draw = true;

  Shape(Polygon points) {
    data = points;
  }

  void update() {
    nodes.add(this);
  }

  void AND(Polygon B) {
    Polygon A = data;
    Polygon out = new Polygon();
    ArrayList<PVector> points = new ArrayList<PVector>();
    for (int i = 0; i < A.npoints; i++) {
      PVector point = new PVector(A.xpoints[i], A.ypoints[i]);
      if (B.contains(point.x, point.y)) {
        points.add(new PVector(int(point.x), int(point.y)));
        //ellipse(point.x, point.y, 5, 5);
      }
    }
    for (int i = 0; i < B.npoints; i++) {
      PVector point = new PVector(B.xpoints[i], B.ypoints[i]);
      if (A.contains(point.x, point.y)) {
        points.add(new PVector(int(point.x), int(point.y)));
        //ellipse(point.x, point.y, 5, 5);
      }
    }
    points = sortPoints(points);
    for (PVector p : points) {
      out.addPoint(int(p.x), int(p.y));
    }
    out.addPoint(int(points.get(0).x), int(points.get(0).y));
    draw = false;
    subpoly = out;
  }

  Polygon get() {
    return data;
  }


  void draw() {
    pushStyle();
    noFill();
    beginShape();
    if (draw) {
      for (int i = 0; i < data.npoints; i++) {
        PVector p = new PVector(data.xpoints[i], data.ypoints[i]); 
        vertex(p.x, p.y);
      }
    } else {

      for (int i = 0; i < subpoly.npoints; i++) {
        PVector p = new PVector(subpoly.xpoints[i], subpoly.ypoints[i]); 
        vertex(p.x, p.y);
      }
    }
    endShape();

    popStyle();
  }
}
