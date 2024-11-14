# OEIS Sequence submissions

This repository is for the purpose of supporting sequence submissions to [OEIS](https://oeis.org/) when proofs are offered by way of program.

## A377941

T(n,k) = number of free polyominoes with n cells, where the maximum number of cells in any row or column is k.

```text
Collinearity considered for any line in the plane across tile centres
   |  k
n  |        1       2       3       4       5       6       7       8
---------------------------------------------------------------------
 1 |        1
 2 |        0       1
 3 |        0       1       1
 4 |        0       2       2       1
 5 |        0       0       9       2       1
 6 |        0       0      18      13       3       1
 7 |        0       0      37      48      19       3       1
 8 |        0       0      62     200      77      25       4       1
```

## A377942

T(n,k) = number of free polyominoes with n cells, where the maximum number of collinear tile centers on any line in the plane is k.

```text
Collinearity only considered along rows or columns
   |  k
n  |        1       2       3       4       5       6       7       8
---------------------------------------------------------------------
 1 |        1
 2 |        0       1
 3 |        0       1       1
 4 |        0       2       2       1
 5 |        0       1       8       2       1
 6 |        0       1      17      13       3       1
 7 |        0       1      39      45      19       3       1
 8 |        0       1      79     182      77      25       4       1
```

## A378014

T(n,k) = number of free hexagon polyominoes with n cells, where the maximum number of cells on any lattice line is k.The term "lattice line" meaning a line running through the cell centres that is perpendicular to the hexagon cell sides.

```text

   |  k
 n |       1      2      3      4      5      6      7      8      9     10       Total
---------------------------------------------------------------------------------------
 1 |       1                                                                          1
 2 |       0      1                                                                   1
 3 |       0      2      1                                                            3
 4 |       0      4      2      1                                                     7
 5 |       0      3     15      3      1                                             22
 6 |       0      5     50     23      3      1                                      82
 7 |       0      1    171    126     30      4      1                              333
 8 |       0      1    506    710    187     39      4      1                      1448
 9 |       0      1   1459   3520   1268    270     48      5      1               6572
10 |       0      1   3792  16617   7703   1948    364     59      5      1       30490

The T(4,2)=4 hexagon polyominoes are:
#         #        #   #      # #
 # #       # #      # #      # #
    #     #

```

## A378015

T(n,k) = number of free hexagon polyominoes with n cells, where the maximum number of collinear cell centers on any line in the plane is k.

```text

   |  k

 n |       1      2      3      4      5      6      7      8      9     10       Total
---------------------------------------------------------------------------------------
 1 |       1                                                                          1
 2 |       0      1                                                                   1
 3 |       0      2      1                                                            3
 4 |       0      4      2      1                                                     7
 5 |       0      2     16      3      1                                             22
 6 |       0      3     52     23      3      1                                      82
 7 |       0      0    169    129     30      4      1                              333
 8 |       0      0    477    740    187     39      4      1                      1448
 9 |       0      0   1245   3729   1274    270     48      5      1               6572
10 |       0      0   2750  17578   7785   1948    364     59      5      1       30490

The T(5,2)=2 hexagon polyominoes are:
 #          #   #
#   #        # #
 # #        #
```
