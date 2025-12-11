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
            for j in range(0, len(number)):
                if does_repeat(number, number[:j]):
                    sum += i
                    break

    return sum

def does_repeat(number, pattern):
    if len(pattern) == 0:
        return False

    if len(number) % len(pattern) != 0:
        return False

    for i in range(len(number)):
        if number[i] != pattern[i % len(pattern)]:
            return False
    return True

if __name__ == "__main__":
    print(main())