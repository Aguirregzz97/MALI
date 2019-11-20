func int fib(int n) {
  #write n, '$';
  if (n <= 1) {
    return n;
  };
  return fib(n - 1) + fib(n - 2);
}

main {
  var {
    int n;
  }
  n = 10;
  write fib(n), '\n';
}