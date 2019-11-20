func int fib(int n) {
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

main {
  write fib(10), '\n';
}