var {
  int arr[10], n;
}

func void print() {
  var {
    int i, j;
  }
  i = 0;
  while (i < n) {
    write arr[i], '\n';
    i = i + 1;
  };
}

func bool validate_sort() {
  var {
    int i;
  }

  i = 0;
  while (i < n-1) {
    if (arr[i] > arr[i+1]) {
      return false;
    };
    i = i + 1;
  };
  return true;
}

func void sort() {
  var {
    int i, j, aux;
  }

  i = 0;
  while (i < n-1) {
    j = 0;
    while (j < n-1-i) {
      if (arr[j] > arr[j+1]) {
        aux = arr[j];
        arr[j] = arr[j+1];
        arr[j+1] = aux;
      };
      j = j + 1;
    };
    i = i + 1;
  };
}

func bool find(int x) {
  var {
    int i;
  }

  i = 0;
  while (i < n) {
    if (i == x) {
      return true;
    };
    i = i + 1;
  };
  return false;
}

main {
  var {
    bool error;
  }

  error = false;

  n = 10;
  arr[0] = 10;
  arr[1] = 9;
  arr[2] = 8;
  arr[3] = 7;
  arr[4] = 6;
  arr[5] = 5;
  arr[6] = 4;
  arr[7] = 3;
  arr[8] = 2;
  arr[9] = 1;

  sort();

  #print();

  if (not validate_sort()) {
    write "Error on sort!";
    error = true;
  };

  if (not find(5)) {
    write "Error on find when it exists!";
    error = true;
  };

  if (find(15)) {
    write "Error on find when it does not exists!";
    error = true;
  };

  if (not error) {
    write "Success!", '\n';
  };
}