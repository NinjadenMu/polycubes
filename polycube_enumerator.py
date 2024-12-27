import itertools
from collections import deque


ROTATIONS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (y, -z, -x),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (-z, -y, -x),
]

def normalize_translation(polycube):
    min_x = min(x for x, y, z in polycube)
    min_y = min(y for x, y, z in polycube)
    min_z = min(z for x, y, z in polycube)
    return {(x - min_x, y - min_y, z - min_z) for x, y, z in polycube}


def canonical_form(polycube):
    normalized = normalize_translation(polycube)
    rotations = [
        tuple(sorted(normalize_translation(apply_rotation_to_polycube(normalized, r))))
        for r in ROTATIONS
    ]
    return min(rotations)


def apply_rotation_to_polycube(polycube, rotation):
    return {rotation(x, y, z) for x, y, z in polycube}


def neighbors(point):
    x, y, z = point
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1),
    ]


def fits_bounding_box(polycube): #This is unnecessary for general polycube enumeration, I just added this for something specific to a school assignment
    min_x = min(x for x, y, z in polycube)
    max_x = max(x for x, y, z in polycube)
    min_y = min(y for x, y, z in polycube)
    max_y = max(y for x, y, z in polycube)
    min_z = min(z for x, y, z in polycube)
    max_z = max(z for x, y, z in polycube)
    return (max_x - min_x <= 2) and (max_y - min_y <= 2) and (max_z - min_z <= 2)
    #return True


def enumerate_polycubes(n):
    initial_polycube = {(0, 0, 0)}
    seen = set()
    queue = deque([initial_polycube])
    results = []

    while queue:
        polycube = queue.popleft()
        if len(polycube) == n:
            canonical = canonical_form(polycube)
            if canonical not in seen:
                seen.add(canonical)
                if fits_bounding_box(polycube): #This is unnecessary for general polycube enumeration, I just added this for something specific to a school assignment
                    results.append(polycube)
            continue

        for point in polycube:
            for neighbor in neighbors(point):
                if neighbor not in polycube:
                    new_polycube = polycube | {neighbor}
                    if canonical_form(new_polycube) not in seen:
                        queue.append(new_polycube)

    return results

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualize_polycube(polycube, ax, color='blue'):
    for x, y, z in polycube:
        vertices = [
            (x, y, z),
            (x + 1, y, z),
            (x + 1, y + 1, z),
            (x, y + 1, z),
            (x, y, z + 1),
            (x + 1, y, z + 1),
            (x + 1, y + 1, z + 1),
            (x, y + 1, z + 1),
        ]

        faces = [
            [vertices[i] for i in [0, 1, 2, 3]],
            [vertices[i] for i in [4, 5, 6, 7]],
            [vertices[i] for i in [0, 1, 5, 4]],
            [vertices[i] for i in [2, 3, 7, 6]],
            [vertices[i] for i in [1, 2, 6, 5]],
            [vertices[i] for i in [0, 3, 7, 4]],
        ]

        poly3d = Poly3DCollection(faces, alpha=0.7, linewidths=0.5, edgecolors='k')
        poly3d.set_facecolor(color)
        ax.add_collection3d(poly3d)

def visualize_all_polycubes(polycubes):
    fig = plt.figure(figsize=(10, 10))
    num_polycubes = len(polycubes)
    cols = int(num_polycubes ** 0.5) + 1
    rows = (num_polycubes // cols) + (num_polycubes % cols > 0)

    for i, polycube in enumerate(polycubes, 1):
        ax = fig.add_subplot(rows, cols, i, projection='3d')
        visualize_polycube(polycube, ax)
        ax.set_title(f"Polycube {i}", fontsize=8)
        ax.set_xlim([0, n])
        ax.set_ylim([0, n])
        ax.set_zlim([0, n])
        ax.set_box_aspect([1, 1, 1])
        ax.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    n = 3
    polycubes = enumerate_polycubes(n)
    print(f"Number of unique polycubes of size {n}: {len(polycubes)}")
    visualize_all_polycubes(polycubes)
