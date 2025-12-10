import data_helper

data = data_helper.get_data(1)

def main():
    pointer = 50
    stops_at_zero = 0
    passes_zero = 0
    
    for rotation in data.split():
        direction, amount = rotation[0], int(rotation[1:])
        
        if direction == 'L':
            first_k = pointer if pointer > 0 else 100
            if first_k <= amount:
                passes_zero += 1 + (amount - first_k) // 100
            pointer = (pointer - amount) % 100
        else:
            first_k = 100 - pointer if pointer > 0 else 100
            if first_k <= amount:
                passes_zero += 1 + (amount - first_k) // 100
            pointer = (pointer + amount) % 100
        
        if pointer == 0:
            stops_at_zero += 1
    
    return pointer, stops_at_zero, passes_zero


if __name__ == "__main__":
    print(main())

