import data_helper

data = data_helper.get_data(5)


def main():
    split_data = data.strip().split("\n\n")
    
    ranges = [tuple(map(int, range.split("-"))) for range in split_data[0].split("\n")]
    ingredients = [int(ingredient) for ingredient in split_data[1].split("\n")]
    
    available = 0
    for ingredient in ingredients:
        for range in ranges:
            if range[0] <= ingredient <= range[1]:
                available += 1
                break
    return available

if __name__ == "__main__":
    print(main())
