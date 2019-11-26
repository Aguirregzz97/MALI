func int fib(int n) {
  if (n <= 1) {
    return n;
  };
  return fib(n - 1) + fib(n - 2);
}

main {
  var {
    int n, fib;
  }
  n = 10;
  fib = fib(n);
  if (fib == 55) {
    write "Success! fib(", n, ") = ", fib, '\n';
  } else {
    write "Error! fib(", n, ") = ", fib, '\n';
  };
}