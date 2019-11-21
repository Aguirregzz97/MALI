main {
  var {
    int i;
    float f;
    char c;
    bool b, error;
  }

  error = false;

  i = 5 + 5 - 5 * 2 / 5;
  if (i <> 8) {
    write "Error on expression: 5 + 5 - 5 * 2 / 5 = ", i, '\n';
    error = true;
  };

  i = 2 + 'a' * 2.5 - true / 1;
  if (i <> 243) {
    write "Error on expression: 2 + 'a' * 2.5 - true / 1 = ", i, '\n';
    error = true;
  };

  f = 1.5 + 2 - 3.14 * 5.2 / 6.4;
  if (f < 0.9 or f > 0.99) {
    write "Error on expression: 1.5 + 2 - 3.14 * 5.2 / 6.4 = ", f, '\n';
    error = true;
  };

  f = 1 + 1.5 - true * 'a' / 2;
  if (f <> -45.5) {
    write "Error on expression: 1 + 1.5 - true * 'a' / 2 = ", f, '\n';
    error = true;
  };

  c = 'A' + 2;
  if (c <> 'C') {
    write "Error on expression: 'A' + 2 = ", c, '\n';
    error = true;
  };

  b = 1 < 2 and 4 > 3 and 5 >= 5 and 6 <= 6 and 7 == 7 and 8 <> 9;
  if (not b) {
    write "Error on expression: 1 < 2 and 4 > 3 and 5 >= 5 and 6 <= 6 and 7 == 7 and 8 <> 9 = ", b, '\n';
    error = true;
  };

  b = 1 < 2 or 4 > 3;
  if (not b) {
    write "Error on expression: 1 < 2 or 4 > 3 = ", b, '\n';
    error = true;
  };

  i = - (2 + 4) * 3;
  if (i <> -18) {
    write "Error on expression: (2 + 4) * 3 = ", i, '\n';
    error = true;
  };

  if (not error) {
    write "Finished without errors!", '\n';
  };
}