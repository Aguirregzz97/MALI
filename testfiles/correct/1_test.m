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

  # El e dentro de Animal es una expresion que se agrega a los cuadruplos pero que no se
  # saca porque aun no programamos la llamada a funcion
  init(int e, char n, char r) : Animal(e) {
    nombre = n;
    raza = r;
  }

  public void Ladrar() {
    var {
      int z;
    }
    write "Woof Woof";
    write edad;
  }
}

var {
  int cont;
}

func void printAnimal(Animal a) {
  var {
    int x, y;
  }

  #write a.nombre;
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

  w = read;

  z = w * y + b * c + 100 * (7.8 + 'a');

  if (y > b) {
    write "True";
  } elif (y < b) {
    write "False";
  } elif (c < b) {
    write "False2";
  } else {
    write "Neither";
  };

  a = b + c;

  #a.Ladrar;
}