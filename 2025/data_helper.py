import requests

SESSION = ""

def get_data(day: int):
    r = requests.get(f"https://adventofcode.com/2025/day/{day}/input", headers = {'Cookie': f'session={SESSION}'})
    return r.text
