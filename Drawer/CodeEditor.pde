public class CodeEditor extends PApplet {
  static final int NUM = 2;
  final TextBox[] tboxes = new TextBox[NUM];
  int idx;
  String startText = "var c1 = c(90,90,90)h;";

  
  public void settings() {
    size(640, 480);
    smooth(4);
  }

  void setup() {
    surface.setResizable(true);
    frameRate(20);
    rectMode(CORNER);
    textAlign(LEFT);
    strokeWeight(1.5);

    instantiateBoxes();
    tboxes[idx = 0].isFocused = true;
  }
  String text(){
    return tboxes[0].txt;
  }

  void draw() {
    background(#778C85);
    tboxes[0].display();
  }

  
  void keyTyped() {
    final char k = key;
    if (k == CODED | idx < 0)  return;

    final TextBox tbox = tboxes[idx];
    final int len = tbox.txt.length();

    if (k == BACKSPACE)  tbox.txt = tbox.txt.substring(0, max(0, len-1));
    else if (len >= tbox.lim)  return;
    else if (k == ENTER | k == RETURN)     tbox.txt += "\n";
    else if (k == TAB & len < tbox.lim-3)  tbox.txt += "    ";
    else if (k == DELETE)  tbox.txt = "";
    else if (k >= ' ')     tbox.txt += str(k);
  }

  void keyPressed() {
    if (key != CODED | idx < 0)  return;
    final int k = keyCode;

    final TextBox tbox = tboxes[idx];
    final int len = tbox.txt.length();

    if (k == LEFT)  tbox.txt = tbox.txt.substring(0, max(0, len-1));
    else if (k == RIGHT & len < tbox.lim-3)  tbox.txt += "    ";
  }

  void instantiateBoxes() {
    tboxes[0] = new TextBox(
      2, 2, // x, y
      width-5, height-5, // w, h
      640, // lim
      0300 << 030, color(-1, 040), // textC, baseC
      color(-1, 0100), color(#FFFF00, 0200)); // bordC, slctC
  }

  class TextBox { // demands rectMode(CORNER)
    final color textC, baseC, bordC, slctC;
    final short x, y, w, h, xw, yh, lim;

    boolean isFocused;
    String txt = startText;

    TextBox(int xx, int yy, int ww, int hh, int li, 
      color te, color ba, color bo, color se) {
      x = (short) xx;
      y = (short) yy;
      w = (short) ww;
      h = (short) hh;

      lim = (short) li;

      xw = (short) (xx + ww);
      yh = (short) (yy + hh);

      textC = te;
      baseC = ba;
      bordC = bo;
      slctC = se;
    }

    void display() {
      stroke(isFocused? slctC : bordC);
      fill(baseC);
      rect(x, y, w, h);

      fill(textC);
      text(txt + blinkChar(), x+2, y+2, w, h);
    }

    String blinkChar() {
      return isFocused && (frameCount>>2 & 1) == 0 ? "_" : "";
    }

    boolean checkFocus() {
      return isFocused = mouseX > x & mouseX < xw & mouseY > y & mouseY < yh;
    }
  }
}
