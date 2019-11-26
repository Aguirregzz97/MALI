main {
  var {
    int arr[5], cont, n;
  }

  cont = 0;
  while (cont < 5) {
    arr[cont] = cont;
    cont = cont + 1;
  };

  cont = 0;
  while (cont < 5) {
    write arr[arr[cont]], '\n';
    cont = cont + 1;
  };

}