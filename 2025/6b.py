import helper
import operator
from functools import reduce

data = helper.get_data(6).strip("\n").split("\n")

def main():
    operations = []
    operation = []
    for i in range(len(data[0])):
        number = ""
        for line in data:
            c = line[-i-1]
            if c not in "*+":
                number += c
            else:
                operation.append(number)
                operation.append(c)
                operations.append(operation.copy())
                operation.clear()
                number = ""
                break
        if number.strip().isdigit():
            operation.append(number)
    
    result = 0
    for i in range(len(operations)):
        op = sum if operations[i][-1] == "+" else prod
        result += op(map(int, operations[i][:-1]))

    return result

def prod(iterable):
    return reduce(operator.mul, iterable, 1)

if __name__ == "__main__":
    print(main())
