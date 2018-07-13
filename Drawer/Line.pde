class Line {
  Polygon poly = new Polygon();
  int id = nodes.size();
  PVector from;
  PVector to;
  ArrayList<PVector> points;
  boolean draw = true;

  Line(float fx, float fy, float tx, float ty) {
    from = new PVector(fx, fy);
    to = new PVector(tx, ty);
    init();
  }

  Line(PVector f, PVector t) {
    from = f;
    to = t;
    init();
  }

  void init() {
    points = getPoints(from, to);
    points.add(to);
    draw();
    //nodes.add((Obj)this);
  }

  void draw() {
    if (draw) {
      pushStyle();
      noFill();
      beginShape();
      vertex(points.get(0).x, points.get(0).y);
      vertex(points.get(points.size()-1).x, points.get(points.size()-1).y);
      endShape();
      popStyle();
    }
  }

  Info get() {
    return new Info(id, poly);
  }


  ArrayList<PVector> getPoints(PVector from, PVector to) {
    ArrayList<PVector> points = new ArrayList<PVector>();
    int count = int(to.dist(from));
    float angle = atan2((to.y - from.y), (to.x - from.x));
    float lineLength = dist(from.x, from.y, to.x, to.y);
    float segmentLength = lineLength / count;

    for (int i = 1; i < count+1; i++) {                
      float distFromStart = segmentLength * i;
      float px = from.x + distFromStart * cos(angle);
      float py = from.y + distFromStart * sin(angle);
      poly.addPoint(int(px), int(py));
      points.add(new PVector(px, py));
    }
    return points;
  }
}
