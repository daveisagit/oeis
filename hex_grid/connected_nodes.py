"""Code for finding connected planer graphs with nodes that 
lie on a hex/triangular lattice.
With a particular interest on restricting the collinearity
This is to support contribution on OEIS for sequence A377756
"""

from functools import lru_cache
from itertools import combinations
from operator import add, sub
from sys import setrecursionlimit
from numpy.linalg import matrix_rank


setrecursionlimit(3000)

# Using Cube coordinates where x+y+z=0 is the plane
# slicing the infinite cube through its centre
# Here is a good description of them
# https://www.redblobgames.com/grids/hexagons/#neighbors

origin = (0, 0, 0)

cube_vectors = [
    (1, 0, -1),
    (1, -1, 0),
    (0, -1, 1),
    (-1, 0, 1),
    (-1, 1, 0),
    (0, 1, -1),
]


def cube_to_doubled(h):
    """Convert Cube to Double"""
    return h[1], h[0] - h[2]


def scalar_multiply(v, s):
    return tuple(x * s for x in v)


def draw_pattern(points):
    """Visualise a pattern of nodes"""
    doubled = [cube_to_doubled(p) for p in points]
    min_r = min(p[0] for p in doubled)
    min_c = min(p[1] for p in doubled)
    max_r = max(p[0] for p in doubled)
    max_c = max(p[1] for p in doubled)

    for r in range(min_r, max_r + 1):
        row = ""
        for c in range(min_c, max_c + 1):
            p = r, c
            c = " "
            if p in doubled:
                c = "#"
            row += c
        print(row)


def collinear(points):
    """Return True if points are collinear
    As identified when the rank of matrix = 1
    https://en.wikipedia.org/wiki/Collinearity
    """
    point_list = list(points)
    vectors = [list(map(sub, p, point_list[0])) for p in point_list[1:]]
    r = matrix_rank(vectors)
    return r == 1


def collinear_along_lattice_lines(points):
    """Return True if points are collinear along a lattice line
    This is the case when one of the dimension ordinates is the same
    for all points.
    """
    point_list = list(points)
    vectors = [list(map(sub, p, point_list[0])) for p in point_list[1:]]
    for d in range(3):
        if all(v[d] == 0 for v in vectors):
            return True
    return False


def normalise_position(points):
    """Translate the pattern to the top left in a consistent fashion
    This will allow us to identify a unique pattern by its coordinate set"""
    min_r = min(p[1] for p in points)
    v = scalar_multiply(cube_vectors[1], min_r)
    points = translate_points(points, v)

    min_c = min(p[0] for p in points if p[1] == 0)
    v = scalar_multiply(cube_vectors[3], min_c)
    points = translate_points(points, v)

    return points


def translate_points(points, vector):
    """Translate all point by the given vector"""
    return tuple(tuple(map(add, p, vector)) for p in points)


def flip_point(p):
    """Reflect a point over vertical centre line through origin"""
    return p[2], p[1], p[0]


def flip_points(points):
    """Reflect the pattern over vertical centre line through origin"""
    return tuple(flip_point(p) for p in points)


def rotate_point_60_ACW_about_origin(p):
    """Shift coordinates right and x-1"""
    return tuple(-p[(i - 1) % 3] for i in range(3))


def rotate_points_60_ACW(points):
    """Returns points rotated 60 ACW about the origin"""
    points = tuple(rotate_point_60_ACW_about_origin(p) for p in points)
    return points


def generate_dihedral_symmetries(points):
    """Generator for the 12 dihedral symmetries"""

    def generate_rotations(points):
        for _ in range(6):
            points = normalise_position(points)
            yield points
            points = rotate_points_60_ACW(points)

    yield from generate_rotations(points)
    points = flip_points(points)
    yield from generate_rotations(points)


@lru_cache(maxsize=None)
def generate_tiling_patterns(n, max_collinear=None, lattice_lines_only=False):
    """Generate connected patterns of size n on the hex grid
    where there is a limit on the maximum number of collinear nodes
    over the underlying RxR space.
    """
    if n == 1:
        return {frozenset({origin})}
    new_patterns = set()

    # for every graph of the previous size
    for pattern in generate_tiling_patterns(
        n - 1, max_collinear=max_collinear, lattice_lines_only=lattice_lines_only
    ):
        p_set = frozenset(pattern)

        # for every node in that graph
        for p in pattern:

            # for ever possible neighbour of that node
            for v in cube_vectors:
                np = tuple(map(add, p, v))
                if np in p_set:
                    continue

                # a potential new pattern
                new_pattern = p_set | {np}

                # check if there are any k+1 points collinear
                # where k is the limit on the number of collinear points allowed
                valid = True
                if max_collinear:

                    for grp in combinations(new_pattern, max_collinear + 1):
                        # only need to consider those with this new point
                        if np not in grp:
                            continue

                        if lattice_lines_only:
                            if collinear_along_lattice_lines(grp):
                                valid = False
                                break
                        else:
                            if collinear(grp):
                                valid = False
                                break

                if not valid:
                    continue

                # normalise its position
                new_pattern = frozenset(normalise_position(new_pattern))

                # check this is not already known under symmetry
                is_new = True
                for new_pattern_sym in generate_dihedral_symmetries(new_pattern):
                    new_pattern_sym = frozenset(new_pattern_sym)
                    if new_pattern_sym in new_patterns:
                        is_new = False
                        break
                if not is_new:
                    continue

                new_patterns.add(new_pattern)

    return new_patterns


def output_table(N, lattice_lines_only=False, all_values=False):
    """Output a table for n,k"""
    print()
    if lattice_lines_only:
        print(f"Collinearity only considered along lattice lines")
    else:
        print(f"Collinearity for any line in the plane")
    print("   |  k")
    line = "n  | "
    for n in range(1, N + 1):
        line += f"{n:5d}"
    print(line)
    print("-" * len(line))
    for n in range(1, N + 1):
        line = f"{n:2d} | "
        k_stop = n + 1
        if all_values:
            k_stop = N + 1
        for k in range(1, k_stop):
            cnt = len(
                generate_tiling_patterns(
                    n, max_collinear=k, lattice_lines_only=lattice_lines_only
                )
            )
            line += f"{cnt:5d}"
        print(line)
    print()


# Result tables
# output_table(7, lattice_lines_only=False)
# output_table(7, lattice_lines_only=True)

# Patterns visualised
print()
print("Examples")
print()
for n in range(1, 6):
    print("----------------------------")
    print(f"n={n}")
    print("----------------------------")
    for points in generate_tiling_patterns(n, max_collinear=2, lattice_lines_only=True):
        print(sorted(points))
        draw_pattern(points)
        print()
