import helper

data = helper.get_data(3)

def main():
    sum = 0

    for line in data.split():
        number = (line[0], line[1])
        for i in range(1, len(line)):
            n = line[i]
            
            if n > number[0]:
                if i + 1 < len(line):
                    number = (n, line[i + 1])
                    continue
            
            if n > number[1]:
                number = (number[0], n)

        print(number)
        sum += int(number[0] + number[1])

    return sum

if __name__ == "__main__":
    print(main())