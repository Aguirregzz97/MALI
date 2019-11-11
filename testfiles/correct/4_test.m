class Page {
  attr {
    public int num;
  }

  init(int n) {
    num = n;
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
}

main {
  var {
    Student student, student2;
  }

  student.init(1, 500, 20);
  student2.init(2, 600, 30);

  write student.book.page.num, '$';
  write student2.book.page.num, '$';
}