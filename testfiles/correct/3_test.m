class Animal {
  attr {
    private char nombre;
    public int edad;
  }

  init(char n, int e) {
    nombre = n;
    edad = e;
  }

  public void PrintNombre() {
    write nombre, edad;
  }
}

class Mamifero extends Animal {
  attr {
    private bool oviparo;
  }

  init (char n, int e, bool o) : Animal(n, e) {
    oviparo = o;
  }

  public void PrintMamifero() {
    write edad, oviparo;
  }
}

class Perro extends Mamifero {
  attr {
    private char raza;
  }

  init (char n, int e, bool o, char r) : Mamifero(n, e, o) {
    raza = r;
  }

  public void PrintPerro() {
    write edad, " ", raza, '$';
  }
}

main {
  var {
    Perro p;
  }

  p.init('s', 6, 0, 'c');

  p.PrintPerro();
}