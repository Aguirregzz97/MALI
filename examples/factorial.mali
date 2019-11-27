func int factorial_rec(int x) {
  if (x == 1) {
    return 1;
  };
  return x * factorial_rec(x-1);
}

func int factorial_it(int x) {
  var {
    int res;
  }
  res = 1;
  while (x > 1) {
    res = res * x;
    x = x - 1;
  };
  return res;
}

main {
  write factorial_rec(10), '\n', factorial_it(10), '\n';
}