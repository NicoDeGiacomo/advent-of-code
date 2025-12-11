import helper

data = helper.get_data(7).strip("\n").split("\n")

matrix = [[c for c in line] for line in data]

def main():
    for i in range(len(matrix) - 1):
        for j in range(len(matrix[i])):
            if matrix[i][j] in ["S", "|"]:
                if matrix[i+1][j] == ".":
                    matrix[i+1][j] = "|"
                elif matrix[i+1][j] == "^":
                    matrix[i+1][j-1] = "|"
                    matrix[i+1][j+1] = "|"
    
    divisions_count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "^" and matrix[i-1][j] == "|":
                divisions_count += 1
    return divisions_count
                    

if __name__ == "__main__":
    print(main())
