import helper

data = helper.get_data(3)

"""
Find the largest N-digit number subsequence using a greedy stack approach.
- Maintain a monotonic decreasing stack to maximize the resulting number.
- Pop smaller elements if a larger one is found and sufficient digits remain to fill the quota.
"""

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