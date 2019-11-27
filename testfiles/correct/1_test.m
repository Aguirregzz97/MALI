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
    private int ye[5];
  }

  # El e dentro de Animal es una expresion que se agrega a los cuadruplos pero que no se
  # saca porque aun no programamos la llamada a funcion
  init(int e, char n, char r[10], char s) : Animal(e) {
    nombre = n;
    raza = r[0];
    #edad = e;
    ye[1] = 2;
  }

  public void Ladrar() {
    var {
      int z;
    }
    write "Woof Woof", '\n';
    write "Woof soy un ", raza, '\n';
    write edad, '\n';
    write ye[1], '\n';
    ye[1] = ye[1] * 5;
    write ye[1], '\n';
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

func void printCubo2x2x2(char cubo[2][2][2]){
  var {
    int i, j, k;
  }
  write "Imprimiendo cubo", '\n';
  i = 0;
  while(i < 2){
    j = 0;
    while(j < 2){
      k = 0;
      while (k < 2){
        write cubo[i][j][k];
        k = k + 1;
      };
      j = j + 1;
    };
    i = i + 1;
  };
  write " TKM", '\n';
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
    char d[10], e[2][2][2];
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

  if (1 > 1) {
    write "True", '\n';
  } elif (2 < 2) {
    write "False", '\n';
  } elif (2 < 2) {
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
  d[0] = 'x';
  write "Passing", '\n';
  a.init(5, 's', d, 's');

  a.Ladrar();
  a.Ladrar();

  y = a.edad;

  a.Comer();

  y = a.calculateB(5);

  printAlgo();

  y = calculateA(5);

  printAlgo();

  perro.init(6, 'l', d, 's');

  perro.Ladrar();

  write "Calculo del arreglo x[2][", x[1][2], "] = ", x[2][x[1][2]], '\n';

  write "Setteando cubo", '\n';
  e[0][0][0] = 'M';
  e[0][0][1] = 'A';
  e[0][1][0] = 'U';
  e[0][1][1] = 'G';
  e[1][0][0] = 'U';
  e[1][0][1] = 'A';
  e[1][1][0] = 'M';
  e[1][1][1] = 'A';
  printCubo2x2x2(e);
}
