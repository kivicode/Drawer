ScriptEngineManager factory = new ScriptEngineManager();
ScriptEngine js = factory.getEngineByName("nashorn");

import javax.script.*;
import javax.script.Invocable;
import javax.script.Compilable;
import javax.script.CompiledScript;

void addClass(String name) {
  try {
    js.eval("var " + name + " = Java.type(\"" + scriptName + "." + name + "\");");
  }
  catch (final ScriptException se) { 
    se.printStackTrace();
  }
}
void initJS() {
  addClass("Circle");
  addClass("Test");
}

boolean isHighIndex(char in) {
  return int(in) >= 65  && int(in) <= 90;
}

String[] normalizeCode(String[] br) {
  String[] newStrings = new String[br.length];
  for (int i = 0; i < br.length; i++) {
    String line = br[i];
    int index = line.indexOf("new ");
    if (index != -1 && isHighIndex(line.charAt(index+4))) {
      String className = split(split(line, "new ")[1], "(")[0];
      String params = join(split(split(split(line, className + "(")[1], ")")[0].trim(), ","), ",");
      String init = split(line, "new " + className + "(")[0];
      String n = split(split(init, "var")[1], "=")[0].trim();
      String out = init + "new " + className + "();"+n+".set("+params+");";
      newStrings[i] = out;
    } else {
      newStrings[i] = line;
    }
  }
  return newStrings;
}

void evalFile(String name) {
  initJS();
  try {
    String[] lines = loadStrings("code/" + name+".js");
    lines = normalizeCode(lines);
    println(join(lines, "\n"));
    js.eval(join(lines, "\n"));
  } 
  catch (final ScriptException se) { 
    se.printStackTrace();
  }
}

boolean partOfPoly(ArrayList<PVector> in, PVector test) {
  PVector points[] = in.toArray(new PVector[0]);
  int i;
  int j;
  boolean result = false;
  for (i = 0, j = points.length - 1; i < points.length; j = i++) {
    if ((points[i].y > test.y) != (points[j].y > test.y) &&
      (test.x < (points[j].x - points[i].x) * (test.y - points[i].y) / (points[j].y-points[i].y) + points[i].x)) {
      result = !result;
    }
  }
  return result;
}

static ArrayList sortPoints(ArrayList<PVector> in) {
  ArrayList<PVector> orderedList = new ArrayList<PVector>();
  orderedList.add(in.remove(0)); //Arbitrary starting point

  while (in.size() > 0) {
    //Find the index of the closest point (using another method)
    int nearestIndex=findNearestIndex(orderedList.get(orderedList.size()-1), in);

    //Remove from the unorderedList and add to the ordered one
    orderedList.add(in.remove(nearestIndex));
  }
  return orderedList;
}
static int findNearestIndex (PVector thisPoint, ArrayList<PVector> listToSearch) {
  double nearestDistSquared=Double.POSITIVE_INFINITY;
  int nearestIndex = 0;
  for (int i=0; i< listToSearch.size(); i++) {
    PVector point2=listToSearch.get(i);
    float distsq = (thisPoint.x - point2.x)*(thisPoint.x - point2.x) 
      + (thisPoint.y - point2.y)*(thisPoint.y - point2.y);
    if (distsq < nearestDistSquared) {
      nearestDistSquared = distsq;
      nearestIndex=i;
    }
  }
  return nearestIndex;
}


public static class Test {
  String m = "";
  

  public void set(String msg) {
    m = msg;
  }

  public void pr() {
    System.out.println("printMsg : "+m);
  }
  public void printMsg(String msg) {
    System.out.println("printMsg : "+msg);
  }
}
