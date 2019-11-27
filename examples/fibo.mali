func int fib_it(int n) {
  var {
    int a, b, aux, cont;
  }
  a = 0;
  b = 1;
  cont = 0;
  while (cont < n) {
    aux = a;
    a = b;
    b = aux + b;
    cont = cont + 1;
  };
  return a;
}

func int fib_rec(int n) {
  if (n <= 1) {
    return n;
  };
  return fib_rec(n - 1) + fib_rec(n - 2);
}

main {
  write fib_it(10), '\n', fib_rec(10), '\n';
}