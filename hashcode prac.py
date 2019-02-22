import matplotlib.pyplot as plt

import numpy as np
from tqdm import tqdm

# Load input
EXAMPLE = 'a_example.in'
SMALL = 'b_small.in'
MEDIUM = 'c_medium.in'
BIG = 'd_big.in'

in_file = BIG 

SCAN_RANGE_MIN = 0

with open(in_file, 'r') as f:
    R, C, L, H = [int(x) for x in f.readline().split()]
    pizza = np.empty(shape=(R, C), dtype=np.bool)
    for r in range(R):
        pizza[r] = [char == "T" for char in f.readline()[:-1]]
slices = np.full(shape=(R, C), fill_value=-1, dtype=np.int32)
slice_list = []


def check_slice(r, c, w, h):
    if np.sum(slices[r:r + h, c:c + w] > -1) > 0:
        return False
    if (r+h-1) >= R or (w+c-1) >= C:
        return False
    area = w * h
    assert 2 * L <= area <= H
    tomatoes = np.sum(pizza[r:r + h, c:c + w])
    mushrooms = area - tomatoes
    return tomatoes >= L and mushrooms >= L


def put_slice(r, c, w, h):
    slices[r:r + h, c:c + w] = len(slice_list)
    slice_list.append((r, c, w, h))


def print_ans():
    print(len(slice_list))
    for (r, c, w, h) in slice_list:
        print(r, c, (r + h-1), (c + w-1))


def calc_score():
    return np.sum(slices > -1)


min_area = L * 2
max_area = H

# Generate possible shapes
shapes = []
for w in range(H):
    for h in range(H):
        if min_area <= w * h <= max_area:
            shapes.append((w, h))
shapes.reverse()

def find_best_shape(start_r):
    start_r = max(0, start_r)
    max_area = 0
    max_shape = None
    max_coord = None
    for r in range(start_r, R):
        for c in range(0, C):
            if not slices[r][c] > -1:
                for shape in shapes:
                    if shape[0] * shape[1] > max_area and check_slice(r, c, shape[0], shape[1]):
                        max_area = shape[0] * shape[1]
                        max_shape = shape
                        max_coord = (r, c)
                        return max_area, max_shape, max_coord

    return max_area, max_shape, max_coord


def solve():
    pbar = tqdm(total=75000)
    prev_coord = (0, 0)
    while True:
        pbar.update(1)
        max_area, max_shape, max_coord = find_best_shape(prev_coord[0] - SCAN_RANGE_MIN)

        if max_shape is None:
            max_area, max_shape, max_coord = find_best_shape(0)

        if max_shape is not None:
            put_slice(max_coord[0], max_coord[1], max_shape[0], max_shape[1])
            prev_coord = (max_coord[0], max_coord[1])
        else:
            break

def write_ans(out_name):
    with open(out_name,'w') as out_file:
        out_file.write(str(len(slice_list)) + '\n')
        for (r, c, w, h) in slice_list:
            out_file.write(str(r) + " " +  str(c) + " " + str(r + h-1) + " " + str(c + w-1) + "\n")

solve()
# print(slices)
# print_ans()
write_ans("out_" + in_file)

score = calc_score()
print(score, score / (R * C))

print(R*C)

_, ax = plt.subplots()
ax.imshow(slices)
plt.show()
