import helper
import operator
from functools import reduce

data = helper.get_data(6)

def main():
    matrix = [[c for c in line.split()] for line in data.strip().split("\n")]
    t_matrix = list(zip(*matrix))

    result = 0
    for i in range(len(t_matrix)):
        op = sum if t_matrix[i][-1] == "+" else prod
        result += op(map(int, t_matrix[i][:-1]))

    return result

def prod(iterable):
    return reduce(operator.mul, iterable, 1)


if __name__ == "__main__":
    print(main())
