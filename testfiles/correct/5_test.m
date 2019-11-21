func int fib(int n) {
  #write n, '$';
  if (n <= 1) {
    return n;
  };
  return fib(n - 1) + fib(n - 2);
}

main {
  if (fib(10) == 55) {
    write "Finished without errors!", '\n';
  } else {
    write "Error calculating fib", '\n';
  };
}