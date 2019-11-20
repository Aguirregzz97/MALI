class Animal {
  attr {
    private char nombre;
    public int edad;
  }

  init(char n, int e) {
    nombre = n;
    edad = e;
  }

  public void PrintAnimal() {
    write nombre, ' ', edad, '$';
  }

  public char GetName() {
    return nombre;
  }
}

class Mamifero extends Animal {
  attr {
    private bool oviparo;
  }

  init(char n, int e, bool o) : Animal(n, e) {
    oviparo = o;
  }

  public void PrintMamifero() {
    write edad, oviparo;
  }
}

class Perro extends Mamifero {
  attr {
    private char raza;
    public char nombre;
  }

  init(char n, int e, bool o, char r) : Mamifero(n, e, o) {
    raza = r;
    #write r, ' ', raza, '$';
    nombre = 'L';
    edad = 0;
    #write oviparo, '$';
  }

  public void PrintPerro() {
    write edad, " ", raza, '$';
  }
}

main {
  var {
    Perro p;
  }

  p->init('s', 6, false, 'c');

  write "Debe ser: 6 c: ";
  p->PrintPerro();

  write "Debe ser: s L: ";
  write p->GetName(), ' ', p->nombre, '$';

  write "Debe ser: s 6: ";
  p->PrintAnimal();
}