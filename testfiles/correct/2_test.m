class Rectangle {
  attr {
    private int altura;
    private int anchura;
  }

  init(int a, int b) {
    altura = a;
    anchura = b;
  }

  public int Area() {
    return altura * anchura;
  }

  public int Perimetro() {
    return 2 * altura + 2 * anchura;
  }
}

class Square extends Rectangle {
  init(int a) : Rectangle(a, a) {

  }
}

main {
  var {
    Square s, r;
  }

  s->init(5);

  r->init(6);

  write "Debe imprimir 25: ", s->Area(), '$';
  write "Debe imprimir 20: ", s->Perimetro(), '$';

  write "Debe imprimir 36: ", r->Area(), '$';
  write "Debe imprimir 24: ", r->Perimetro(), '$';
}