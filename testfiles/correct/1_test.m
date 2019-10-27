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

func void printAnimal(Animal a3) {
  var {
    int x1, y2;
  }

  #write a.nombre;
}

func void printAlgo() {

  write "Algo";
}

func int calculateA(int a){
  if (a < 5){
    return a * 5;
  } elif (a == 5) {
    return a + 5;
  };
}

main {
  var {
    Animal a;
    int x[5][10];
    int z,y,w,b,c;
  }

  #a = Perro;

  #a.init();

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

  while(cont < 5) {
    write '1', '2', '3';
    cont = cont + 1;
  };

  a = b + c;

  #a.Ladrar;
}
