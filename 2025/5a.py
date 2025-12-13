import helper

data = helper.get_data(5)

"""
Count ingredients that fall into at least one valid range.
- Parse a list of valid ranges and a list of ingredients.
- For each ingredient, check if it lies within any of the ranges.
"""


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
