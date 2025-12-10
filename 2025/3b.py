import data_helper

data = data_helper.get_data(3)

# Generalization of 3a
N_DIGITS = 12

def main():
    total = 0

    for line in data.split():
        number = []
        
        for i in range(len(line)):
            candidate = line[i]

            while number and candidate > number[-1] and len(line) - i > N_DIGITS - len(number):
                number.pop()
            
            if len(number) < N_DIGITS:
                number.append(candidate)
        
        total += int(''.join(number))

    return total

if __name__ == "__main__":
    print(main())