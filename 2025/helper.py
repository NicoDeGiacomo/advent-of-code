import requests

from secrets import SESSION

def get_data(day: int):
    r = requests.get(f"https://adventofcode.com/2025/day/{day}/input", headers = {'Cookie': f'session={SESSION}'})
    r.raise_for_status()
    return r.text

def print_matrix(matrix):
    for l in matrix:
        for c in l:
            print(c, end="")
        print()
    print()
