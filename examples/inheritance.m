class Polygon {
  attr {
    protected float length, width, area;
  }

  init (float l, float w) {
    length = l;
    width = w;
  }

  public void calculate_area() {
    area =  length * width;
  }

  public float get_area() {
    return area;
  }
}

class Rectangle extends Polygon {
  init (float l, float w) : Polygon(l, w) {

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
    bool error;
  }

  error = false;

  rectangle.init(5, 6);
  rectangle.calculate_area();
  if (rectangle.get_area() <> 30) {
    write "Error calculating rectangle area", '\n';
    error = true;
  };

  square.init(5);
  square.calculate_area();
  if (square.get_area() <> 25) {
    write "Error calculating square area", '\n';
    error = true;
  };

  triangle.init(5, 6);
  triangle.calculate_area();
  if (triangle.get_area() <> 15) {
    write "Error calculating triangle area", '\n';
    error = true;
  };

  trapezoid.init(5, 6, 7);
  trapezoid.calculate_area();
  if (trapezoid.get_area() <> 38.5) {
    write "Error calculating trapezoid area", '\n';
    error = true;
  };

  if (not error) {
    write "Success!", '\n';
  };
}