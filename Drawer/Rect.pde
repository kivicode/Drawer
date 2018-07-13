class Rect { //<>//
  Polygon poly = new Polygon();
  int id = nodes.size();
  PVector corners[] = new PVector[4];
  ArrayList<PVector> points = new ArrayList<PVector>();
  ArrayList<Line> lines = new ArrayList<Line>();
  boolean draw = true;

  Rect(float x1, float y1, float w, float h) {
    corners[0] = new PVector(x1, y1);
    corners[1] = new PVector(x1+w, y1);
    corners[2] = new PVector(x1+w, y1+h);
    corners[3] = new PVector(x1, y1+h);
    init();
  }

  Rect(PVector cornerTL, PVector cornerBR) {
    PVector cornerTR = new PVector(cornerTL.x+(cornerBR.x-cornerTL.x), cornerTL.y);
    PVector cornerBL = new PVector(cornerTL.x, cornerTL.y+(cornerBR.y-cornerTL.y));
    corners[0] = cornerTL;
    corners[1] = cornerTR;
    corners[2] = cornerBR;
    corners[3] = cornerBL;
    init();
  }

  Rect(PVector corner, float w, float h) {
    corners[0] = corner;
    corners[1] = new PVector(corner.x+w, corner.y);
    corners[2] = new PVector(corner.x+w, corner.y+h);
    corners[3] = new PVector(corner.x, corner.y+h);
    init();
  }

  void init() {
    Line up = new Line(corners[0], corners[1]);
    Line right = new Line(corners[1].x, corners[1].y, corners[2].x, corners[2].y);
    Line down = new Line(corners[2], corners[3]);
    Line left = new Line(corners[3], corners[0]);
    lines.add(up);
    lines.add(down);
    lines.add(left);
    lines.add(right);
    addPoints(corners[0], corners[1]);
    addPoints(corners[1], corners[2]);
    addPoints(corners[2], corners[3]);
    addPoints(corners[3], corners[0]);
    points.addAll(up.points);
    points.addAll(right.points);
    points.addAll(down.points);
    points.addAll(left.points);
    draw();
    //nodes.add((Obj)this);
  }

  void draw() {
    if (draw) {
      pushStyle();
      for (Line l : lines) {
        l.draw();
      }
      popStyle();
    }
  }

  Info get() {
    return new Info(id, poly);
  }

  void addPoints(PVector from, PVector to) {
    int count = int(to.dist(from));
    float angle = atan2((to.y - from.y), (to.x - from.x));
    float lineLength = dist(from.x, from.y, to.x, to.y);
    float segmentLength = lineLength / count;

    for (int i = 1; i < count+1; i++) {                
      float distFromStart = segmentLength * i;
      float px = from.x + distFromStart * cos(angle);
      float py = from.y + distFromStart * sin(angle);
      poly.addPoint(int(px), int(py));
    }
  }
}
