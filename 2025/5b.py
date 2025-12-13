import helper

data = helper.get_data(5)

"""
Compute the total length of the union of multiple intervals.
- Parse ranges and sort them.
- Iteratively merge overlapping or contained ranges into a reduced set.
- Sum the lengths of the final non-overlapping ranges.
"""

def main():
    split_data = data.strip().split("\n\n")
    
    ranges = [tuple(map(int, range.split("-"))) for range in split_data[0].split("\n")]
    ranges.sort(key=lambda x: x[0])
    
    reduced_ranges = [ranges[0]]
    for r in ranges:
        should_add = True
        for rr in reduced_ranges:
            if contains(rr, r):
                should_add = False
                break
            
            if contains(r, rr):
                reduced_ranges.remove(rr)
                reduced_ranges.append(r)
                should_add = False
                break

            if overlaps(r, rr):
                reduced_ranges.remove(rr)
                reduced_ranges.append((min(r[0], rr[0]), max(r[1], rr[1])))
                should_add = False
                break

        if should_add:
            reduced_ranges.append(r)

    return sum([rr[1] - rr[0] + 1 for rr in reduced_ranges])


def contains(range1, range2):
    return range1[0] <= range2[0] and range1[1] >= range2[1]

def overlaps(range1, range2):
    if range1[0] <= range2[1] and range1[0] >= range2[0]:
        return True
    if range2[1] <= range1[1] and range2[1] >= range1[0]:
        return True
    return False

if __name__ == "__main__":
    print(main())
