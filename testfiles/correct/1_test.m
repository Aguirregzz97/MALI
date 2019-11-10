class Animal {
  attr {
    public int edad;
    private int anios_captivo;
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
  init(int i, char n, char r) : Animal(i) {
    nombre = n;
    raza = r;
  }

  public void Ladrar() {
    var {
      int z;
    }
    write "Woof Woof", '$';
    write edad, '$';
  }

  public int calculateB(int a){
    if (a < 5){
      return a * 5;
    } elif (a == 5) {
      return a + 5;
    };
  }
}

var {
  int cont;
  Perro perro;
}

func void printAnimal(Animal a) {
  var {
    int x1, y2;
  }

  write a.edad;
  #write a.anios_captivo;
}

func void printAlgo() {

  write "Algo", '$';
}

func int calculateA(int b){
  if (b < 5){
    return b * 5;
  } elif (b == 5) {
    return b + 5;
  };
}

main {
  var {
    Perro a;
    int x[5][10];
    int z,y,w,b,c;
  }

  cont = 5;

  w = 5;
  write w, '$';

  z = 0;
  y = 0;
  w = 0;
  b = 0;
  c = 0;

  z = w * y + b * c + 100 * (7.8 + 2);

  write z, '$';

  if (y > b) {
    write "True", '$';
  } elif (y < b) {
    write "False", '$';
  } elif (c < b) {
    write "False2", '$';
  } else {
    write "Neither", '$';
  };

  while(cont < 10) {
    write "CICLO", '$';
    cont = cont + 1;
  };

  y = b + c;

  y = 535;

  a.init(5, 's', 'c');
  y = a.edad;
  a.Ladrar();

  y = a.calculateB(5);
  printAlgo();
  y = calculateA(5);

  printAlgo();

  perro.init(6, 'l', 'c');
  perro.Ladrar();


}
