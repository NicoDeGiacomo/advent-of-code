import helper

data = helper.get_data(9).strip("\n").split("\n")

points = [tuple(map(int, line.split(","))) for line in data]


def main():
    biggest_area = 0
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            if p1[0] == p2[0] or p1[1] == p2[1]:
                continue
            area = calculate_area(p1, p2)
            if area > biggest_area:
                biggest_area = area
        
    return biggest_area

def calculate_area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

if __name__ == "__main__":
    print(main())

