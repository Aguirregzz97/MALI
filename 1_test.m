class Animal {
  public int edad;

  init Animal(int e) {
    edad = e;
  }

  public void Comer() {
    write "Que rico";
  }
}

class Perro extends Animal {
  public char nombre, raza;

  init Perro(int e) : Animal(e) {

  }

  public void Ladrar() {
    write "Woof Woof"
  }
}

int cont;

func void printAnimal(Animal a) {
  write a.nombre;
}

main {
  cont = 0;

  Animal a;

  a = Perro(5);

  a.Ladrar;
}
