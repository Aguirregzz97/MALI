var {
  int mat1[3][3], mat2[3][3], res[3][3];
  int ren, col;
}

func void multiply() {
  var {
    int r, c, k;
  }

  r = 0;
  while (r < ren) {
    c = 0;
    while (c < col) {
      res[r][c] = 0;
      k = 0;
      while (k < col) {
        res[r][c] = res[r][c] + mat1[r][k] * mat2[k][c];
        k = k + 1;
      };
      c = c + 1;
    };
    r = r + 1;
  };

  r = 0;
  while (r < ren) {
    c = 0;
    while (c < col) {
      write res[r][c], ' ';
      c = c + 1;
    };
    r = r + 1;
    write '\n';
  };
}

main {
  var {
    int r, c;
  }
  ren = 3;
  col = 3;

  # mat 1
  # 1 2 1
  # 0 1 0
  # 2 3 4
  mat1[0][0] = 1;
  mat1[0][1] = 2;
  mat1[0][2] = 1;
  mat1[1][0] = 0;
  mat1[1][1] = 1;
  mat1[1][2] = 0;
  mat1[2][0] = 2;
  mat1[2][1] = 3;
  mat1[2][2] = 4;

  # mat 2
  # 1 0 0
  # 0 1 0
  # 0 0 1
  mat2[0][0] = 1;
  mat2[0][1] = 0;
  mat2[0][2] = 0;
  mat2[1][0] = 0;
  mat2[1][1] = 1;
  mat2[1][2] = 0;
  mat2[2][0] = 0;
  mat2[2][1] = 0;
  mat2[2][2] = 1;

  multiply();
}