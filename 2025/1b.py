import helper

data = helper.get_data(1)

"""
Simulate the movement of a pointer on a circular track (0-99).
- Parse rotation instructions (Order: L/R, Amount).
- Update the pointer position, wrapping around 0-99.
- Count how many times the pointer lands on 0.
"""

def main():
    pointer = 50
    count = 0
    for rotation in data.split():
        order, amount = rotation[0], int(rotation[1:])
        for i in range(amount):
            
            if order == 'L':
                pointer -= 1
            else:
                pointer += 1
            
            if pointer < 0:
                pointer = 99
            elif pointer > 99:
                pointer = 0

            if pointer == 0:
                count += 1

    return pointer, count


if __name__ == "__main__":
    print(main())

