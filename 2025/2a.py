import helper

data = helper.get_data(2)

def main():
    sum = 0

    for r in data.split(','):
        start, end = r.split('-')
        start = int(start)
        end = int(end)

        for i in range(start, end + 1):
            number = str(i)
            half = len(number) // 2
            if number[:half] == number[half:]:
                sum += i

    return sum

if __name__ == "__main__":
    print(main())