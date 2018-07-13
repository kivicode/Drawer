import java.awt.*;

static ArrayList<Shape> nodes = new ArrayList<Shape>();

PVector from = new PVector(100, 100);
PVector to = new PVector(150, 150);

String scriptName = "Drawer";

CodeEditor ce;
void setup() {

  String[] args = {"Code Editor"};
  ce = new CodeEditor();
  PApplet.runSketch(args, ce);
  surface.setSize(640, 480);
  ellipseMode(RADIUS);


  //evalP5(js, // calls P5's canvas API from JS.
  //  "say();");
  evalFile("main");

}

void draw() {
  background(255);
  stroke(0);
  nodes.clear();
  //Shape c1 = new Circle(from, 100).get();
  //Shape c2 = new Circle(to, PVector.dist(to, new PVector(mouseX, mouseY))).get();
  //c1.AND(c2.get());
  //c1.draw();
}

void say() {
  //for (String d : i) {
  println("Fuck ");
  //}
}
String getText() {
  return ce.text();
}
