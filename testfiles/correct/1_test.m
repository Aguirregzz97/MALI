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
    anios_captivo = e;
  }

  public void Comer() {
    write "Que rico", anios_captivo, '\n';
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
    #edad = e;
  }

  public void Ladrar() {
    var {
      int z;
    }
    write "Woof Woof", '\n';
    write edad, '\n';
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

  write "Algo", '\n';
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
    bool flag;
  }

  cont = 5;

  w = 5;
  write w, '\n';
  write "Xs", '\n';
  x[1][2] = 2;
  write x[1][2], '\n';
  x[2][x[1][2]] = 3;

  z = -1;
  y = +2;
  flag = not true;

  write z, ' ', y, ' ', flag, '\n';

  w = 0;
  b = 0;
  c = 0;

  z = w * y + b * c + 100 * (7.8 + 2);

  write z, '\n';

  if (y > b) {
    write "True", '\n';
  } elif (y < b) {
    write "False", '\n';
  } elif (c < b) {
    write "False2", '\n';
  } else {
    write "Neither", '\n';
  };


  #if ('\0') {
  #  write "True";
  #} else {
  #  write "False";
  #};

  while(cont < 10) {
    write "CICLO", '\n';
    cont = cont + 1;
  };

  y = b + c;

  y = 535;

  write "1", '\n';

  a.init(5, 's', 'c');

  write "2", '\n';

  y = a.edad;

  write "3", '\n';

  a.Ladrar();

  a.Comer();

  write "4", '\n';

  y = a.calculateB(5);

  write "5", '\n';

  printAlgo();

  write "6", '\n';

  y = calculateA(5);

  write "7", '\n';

  printAlgo();

  write "8", '\n';

  perro.init(6, 'l', 'c');

  write "9", '\n';

  perro.Ladrar();

  write "10", '\n';

  write "Calculo del arreglo x[2][", x[1][2], "] = ", x[2][x[1][2]], '\n';
}
