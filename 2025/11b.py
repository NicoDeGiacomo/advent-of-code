import helper
from functools import lru_cache

'''
Some optimizations are needed for part two.

- Eliminated Path Revisiting: The BFS stored entire paths as tuples, creating exponential growth as paths were duplicated. Using DFS with memoization we can avoid redundant computation.
- Early Termination After Must-Visit Nodes: Even after passing both 'dac' and 'fft', the algorithm continued exploring all paths to 'out'. The recursive approach with memoization handles this, once we've visited both required nodes we just count paths forward without re-checking.
- State-Based Counting: Instead of storing entire paths, we only count the number of paths.

DFS utilizes recursion, which dives deep into one branch at a time.
Once we figure out that "being at node X having visited {'dac'} leads to 50 valid paths", we cache that fact.
If we reach node X with {'dac'} visited again via a different route, we just look up 50 instantly instead of searching all those paths again.

'''

data = helper.get_data(11).strip()

START = "svr"
END = "out"
MUST_VISIT = tuple(sorted(('dac', 'fft')))

graph = {}

def main():
    for line in data.split("\n"):
        key, value = line.split(":")
        graph[key] = value.split()
    
    return count_from(START, ())

@lru_cache(maxsize=None)
def count_from(node, current_must_visited):
    if node == END:
        return 1 if current_must_visited == MUST_VISIT else 0

    total = 0
    for next_node in graph[node]:
        new_visited = current_must_visited
        if next_node in MUST_VISIT and next_node not in current_must_visited:
            new_visited = tuple(sorted(set(current_must_visited) | {next_node}))
        
        total += count_from(next_node, new_visited)
    
    return total

if __name__ == "__main__":
    print(main())
