class Page {
  attr {
    public int num;
  }

  init(int n) {
    num = n;
  }

  public void print(int n) {
    write n, '$';
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
}

var {
  int x, y, z;
}

main {
  var {
    Student student, student2;
    int n;
  }

  student.init(1, 500, 20);
  student2.init(2, 600, 30);

  write "Debe ser 1 500 20", '$';
  write student.id, ' ', student.book.cost, ' ', student.book.page.num, '$';

  write "Debe ser 2 600 30", '$';
  write student2.id, ' ', student2.book.cost, ' ', student2.book.page.num, '$';

  x = 5;
  y = 5;
  z = x + y;
  n = student2.get5();
  student2.book.page.print(z);
}