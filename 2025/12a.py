import helper

'''
This problem is a variation of the exact cover problem, which can often be solved efficiently using Algorithm X (a recursive, nondeterministic, depth-first, backtracking algorithm) often implemented using the Dancing Links (DLX) data structure.

Here is an example of the Exact Cover problem.
X = {1, 2, 3, 4, 5, 6, 7}
Y = {
    'A': [1, 4, 7],
    'B': [1, 4],
    'C': [4, 5, 7],
    'D': [3, 5, 6],
    'E': [2, 3, 6, 7],
    'F': [2, 7]
}

The unique solution in this case is ['B', 'D', 'F'].

We will try solving one system by hand first.

4x4: 0 0 0 0 2 0

4:
###
#..
###

There is four rotations of shape 4:

A
###
#..
###

B
###
#.#
#.#

C
###
..#
###

D
#.#
#.#
###

Now the system is:

X = {(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3), (2,0), (2,1), (2,2), (2,3), (3,0), (3,1), (3,2), (3,3)}
Y = {
    'A': {(0,0), (0,1), (0,2), (1,0), (2,0), (2,1), (2,2)},
    'B': {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,2)},
    'C': {(0,0), (0,1), (0,2), (1,2), (2,0), (2,1), (2,2)},
    'D': {(0,0), (2,1), (0,2), (1,0), (1,2), (2,0), (2,2)},
}

If we feed that system into the solver...


'''

data = helper.get_data(12).strip()
data = '''
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
'''.strip()

ALL_SHAPES = {}

def main():
    for line in data.split('\n\n'):
        X = {}
        Y = {}

        if line[1] == ':':
            shape_index = line[0]
            ALL_SHAPES[shape_index] = []
            for i, row in enumerate(line.split('\n')[1:]):
                for j, col in enumerate(row):
                    if col == '#':
                        ALL_SHAPES[shape_index].append([i, j])
        else:
            for system in line.split('\n'):
                dimensions, shapes = system.split(':')
                
                dimensions = dimensions.split('x')
                w, h = int(dimensions[0]), int(dimensions[1])

                for i, shape_index in enumerate(shapes.split(' ')):
                    if int(shape_index) > 0:
                        Y[i] = ALL_SHAPES[i]



    return ALL_SHAPES

if __name__ == "__main__":
    print(main())
