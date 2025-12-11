#!/usr/bin/env python3

'''
The idea is to iterate each row and count the posibilities for each cell to be a valid path. Then sum the last row.

In the example:

000000010000000
000000010000000
0000001^1000000
000000101000000
000001^2^100000
000001020100000
00001^3^3^10000
000010303010000
0001^4^331^1000
000104033101000
001^5^434^2^100
001050434020100
01^154^74021^10
010154074021010
1^2^10^11^11^211^1
1 0 2 0 10 0 11 0 11 0 2 1 1 0 1
-------------------
40

'''

import helper

data = helper.get_data(7).strip("\n").split("\n")

matrix = [[c for c in line] for line in data]

def main():
    for j in range(len(matrix[0])):
        if matrix[0][j] == ".":
            matrix[0][j] = 0
        elif matrix[0][j] == "S":
            matrix[0][j] = 1

    for i in range(1, len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == '^':
                continue

            if isinstance(matrix[i - 1][j], int):
                matrix[i][j] = matrix[i - 1][j]
            elif matrix[i - 1][j] == '^':
                matrix[i][j] = 0
            
            if j - 1 >= 0 and matrix[i][j - 1] == '^':
                matrix[i][j] += matrix[i-1][j - 1]
            
            if j + 1 < len(matrix[i]) and matrix[i][j + 1] == '^':
                matrix[i][j] += matrix[i-1][j + 1]

    return sum(matrix[-1])

if __name__ == "__main__":
    print(main())
