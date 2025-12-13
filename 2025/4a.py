import helper

data = helper.get_data(4)

"""
Grid traversal to count safe spots.
- Iterate through all cells in the grid.
- Check accessibility of each cell by examining neighbors (8 directions).
- Count cells that have fewer than 4 dangerous neighbors ('@').
"""


def main():
    matrix = [[c for c in line] for line in data.split()]
    result = 0
    
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ".":
                continue
            if is_accessible(matrix, i, j):
                result += 1
    return result


def is_accessible(matrix, i, j):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    sum = 0
    for direction in directions:
        if i + direction[0] < 0 or i + direction[0] >= len(matrix) or j + direction[1] < 0 or j + direction[1] >= len(matrix[i]):
            continue
        if matrix[i + direction[0]][j + direction[1]] == "@":
            sum += 1
    return sum < 4
            


if __name__ == "__main__":
    print(main())