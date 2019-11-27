class Polygon {
  attr {
    protected float length, width, area;
  }

  init (float l, float w) {
    length = l;
    width = w;
  }

  public float get_area() {
    return area;
  }
}

class Rectangle extends Polygon {
  init (float l, float w) : Polygon(l, w) {

  }

  public void calculate_area() {
    area =  length * width;
  }
}

class Square extends Rectangle {
  init (float l) : Rectangle(l, l) {

  }
}

class Triangle extends Polygon {
  init (float l, float w) : Polygon(l, w) {

  }

  public void calculate_area() {
    area = length * width / 2;
  }
}

class Trapezoid extends Polygon {
  attr {
    private Triangle triangle;
    private Rectangle rectangle;
  }

  init (float big_b, float small_b, float h) {
    rectangle.init(small_b, h);
    triangle.init(big_b - small_b, h);
  }

  public void calculate_area() {
    rectangle.calculate_area();
    triangle.calculate_area();
    area = rectangle.get_area() + triangle.get_area();
  }
}

main {
  var {
    Rectangle rectangle;
    Square square;
    Triangle triangle;
    Trapezoid trapezoid;
  }

  rectangle.init(5, 6);
  rectangle.calculate_area();
  write rectangle.get_area(), '\n';

  square.init(5);
  square.calculate_area();
  write square.get_area(), '\n';

  triangle.init(5, 6);
  triangle.calculate_area();
  write triangle.get_area(), '\n';

  trapezoid.init(5, 6, 7);
  trapezoid.calculate_area();
  write trapezoid.get_area(), '\n';
}