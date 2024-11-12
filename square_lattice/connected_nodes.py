"""Code for finding connected planer graphs with nodes that 
lie on the lattice. 

With a particular interest on restricting the collinearity
of the nodes/tiles

i.e. Polyonimoes with restrictions on collinearity 
"""

from functools import lru_cache
from itertools import combinations
from operator import add, sub
from sys import setrecursionlimit
from numpy.linalg import matrix_rank


setrecursionlimit(3000)

origin = (0, 0)

vectors = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def scalar_multiply(v, s):
    return tuple(x * s for x in v)


def draw_pattern(points):
    """Visualise a pattern of nodes"""
    min_r = min(p[0] for p in points)
    min_c = min(p[1] for p in points)
    max_r = max(p[0] for p in points)
    max_c = max(p[1] for p in points)

    for r in range(min_r, max_r + 1):
        row = ""
        for c in range(min_c, max_c + 1):
            p = r, c
            c = " "
            if p in points:
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
    for d in range(2):
        if all(v[d] == 0 for v in vectors):
            return True
    return False


def normalise_position(points):
    """Translate the pattern to the top left in a consistent fashion
    This will allow us to identify a unique pattern by its coordinate set"""
    min_r = min(p[0] for p in points)
    min_c = min(p[1] for p in points)
    v = (-min_r, -min_c)
    points = translate_points(points, v)
    return points


def translate_points(points, vector):
    """Translate all point by the given vector"""
    return tuple(tuple(map(add, p, vector)) for p in points)


def flip_point(p):
    """Reflect a point over vertical centre line through origin"""
    return -p[0], p[1]


def flip_points(points):
    """Reflect the pattern over vertical centre line through origin"""
    return tuple(flip_point(p) for p in points)


def rotate_point_90_ACW_about_origin(p):
    """Rotate 90 ACW"""
    return -p[1], p[0]


def rotate_points_90_ACW(points):
    """Returns points rotated 60 ACW about the origin"""
    points = tuple(rotate_point_90_ACW_about_origin(p) for p in points)
    return points


def generate_dihedral_symmetries(points):
    """Generator for the 8 dihedral symmetries"""

    def generate_rotations(points):
        for _ in range(4):
            points = normalise_position(points)
            yield points
            points = rotate_points_90_ACW(points)

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
            for v in vectors:
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


def output_table(N, lattice_lines_only=False, all_values=False, cumulative=False):
    """Output a table for n,k"""
    print()
    if lattice_lines_only:
        print(f"Collinearity only considered along rows or columns")
    else:
        print(f"Collinearity considered for any line in the plane across tile centres")
    print("   |  k")
    line = "n  | "
    for n in range(1, N + 1):
        line += f"{n:8d}"
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
            if not cumulative and k > 1:
                prv = len(
                    generate_tiling_patterns(
                        n, max_collinear=k - 1, lattice_lines_only=lattice_lines_only
                    )
                )
                cnt -= prv

            line += f"{cnt:8d}"
        print(line)
    print()


def output_patterns_to_console(N, max_collinear=3, lattice_lines_only=True):
    """Display the pattern images"""
    print()
    print("Examples")
    print()
    for n in range(1, N + 1):
        print("----------------------------")
        print(f"n={n}")
        print("----------------------------")
        for points in generate_tiling_patterns(
            n, max_collinear=max_collinear, lattice_lines_only=lattice_lines_only
        ):
            print(sorted(points))
            draw_pattern(points)
            print()


# Result tables
output_table(8, lattice_lines_only=False)
output_table(8, lattice_lines_only=True)

# Patterns visualised
# output_patterns_to_console(4)
