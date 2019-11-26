func int factorial(int x) {
  if (x == 1) {
    return 1;
  };
  return x * factorial(x-1);
}

main {
  if (factorial(10) <> 3628800) {
    write "Error!", '\n';
  } else {
    write "Success!", '\n';
  };
}