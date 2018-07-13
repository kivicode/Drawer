public static class Circle {

  //Circle(){}
  static Polygon poly = new Polygon();
  static PVector center;
  static float radius;
  int id = 0;
  static PApplet pa;

  //public void set(PVector c, float r) {
  //  center = c;
  //  radius = r;
  //  init();
  //}

  public void set(float cX, float cY, float r) {
    center = new PVector(cX, cY);
    radius = r;
    init();
  }

  public void init() {
    getCirclePoints();
    id = nodes.size();
    //nodes.add(new Shape(poly));
  }

  public Shape get() {
    return nodes.get(id);
  }

  public static void draw() {
    pa.ellipse(center.x, center.y, radius, radius);
  }

  public ArrayList<PVector> getCirclePoints() {
    ArrayList<PVector> out = new ArrayList<PVector>();
    for (int i = 0; i < 360; i++) {
      float angle = radians(360-i);
      float x = center.x+cos(angle)*radius;
      float y = center.y+sin(angle)*radius;
      poly.addPoint(int(x), int(y));
    }
    return out;
  }
}
