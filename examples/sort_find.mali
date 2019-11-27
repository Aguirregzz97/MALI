var {
  int arr[10], n;
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

func bool find(int x, int values[10]) {
  var {
    int i;
  }
  i = 0;
  while (i < 10) {
    if (values[i] == x) {
      return true;
    };
    i = i + 1;
  };
  return false;
}

main {
  var {
    int i;
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

  i = 0;
  while (i < n) {
    write arr[i], ' ';
    i = i + 1;
  };
  write '\n';

  if (find(5, arr)) {
    write "Found 5", '\n';
  };

  if (not find(15, arr)) {
    write "Did not find 15", '\n';
  };
}
