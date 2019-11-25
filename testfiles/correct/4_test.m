class Page {
  attr {
    public int num;
  }

  init(int n) {
    num = n;
  }

  public void print(int n, int m) {
    write n, ' ', m, '\n';
  }
}

class Book {
  attr {
    public int cost;
    public Page page;
  }

  init(int c, int n) {
    cost = c;
    page.init(n);
  }
}

class Student {
  attr {
    public int id;
    public Book book;
  }

  init(int i, int c, int n) {
    id = i;
    book.init(c, n);
  }

  public int get5() {
    return 5;
  }

  public int getN(int n) {
    return n;
  }
}

var {
  int x, y, z;
}

func int get10() {
  return 10;
}

func void doesNothing() {
  write "";
}

main {
  var {
    Student student, student2;
    int n, m, o, p, q, r;
    float f;
  }

  student.init(1, 500, 20);
  student2.init(2, 600, 30);

  write "Debe ser 1 500 20", '\n';
  write student.id, ' ', student.book.cost, ' ', student.book.page.num, '\n';

  write "Debe ser 2 600 30", '\n';
  write student2.id, ' ', student2.book.cost, ' ', student2.book.page.num, '\n';

  x = 5;
  y = 5;
  z = x + y;
  n = student2.get5();
  m = student2.get5();
  o = student2.get5();
  r = m + o;

  write "Debe ser 25 5", '\n';
  student2.book.page.print(m + z + student.get5() + student2.get5(), student.get5());

  write "Debe ser 10 10", '\n';
  student2.book.page.print(z, get10());

  n = 555;

  student2.book.cost = read;
  student.book.cost = student2.book.cost;

  write student.book.cost, ' ', student2.book.cost, '\n';
}