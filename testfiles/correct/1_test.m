class Animal {
  attr {
    public int edad;
  }

  init(int e) {
    var {
      int a;
    }
    edad = e;
  }

  public void Comer() {
    write "Que rico";
  }
}

class Perro extends Animal {
  attr {
    public char nombre, raza;
  }

  init(int e, char n, char r) : Animal(e) {
    nombre = n;
    raza = r;
  }

  public void Ladrar() {
    var {
      int z;
    }
    write "Woof Woof";
  }
}

var {
  int cont;
}

func void printAnimal(Animal a) {
  var {
    int x, y;
  }

  write a.nombre;
}

func void printAlgo() {

  write "Algo";
}

main {
  var {
    Animal a;
    int x[5][10];
    int z,y,w,b,c;
  }

  a = Perro(5);

  a = b;

  cont = 0;

  z = w * y + b * c + 100 * (7.8 + 'a');

  a.Ladrar;
}