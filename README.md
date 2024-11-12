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

## In the Pipeline

Having learnt the ropes a little bit more on the submission process, I think my initial submission A377756 should be cancelled.

I will submit the equivalent sequences for hexagon polyominoes if these (A377941/A377941) become accepted.
