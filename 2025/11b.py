import helper
from functools import lru_cache

'''
Some optimizations are needed for part two.

- Eliminated Path Revisiting: The BFS stored entire paths as tuples, creating exponential growth as paths were duplicated. Using memoization with @lru_cache, we cache results for each (node, visited_must_nodes) state, avoiding redundant computation.
- Early Termination After Must-Visit Nodes: Even after passing both 'dac' and 'fft', the algorithm continued exploring all paths to 'out'. The recursive approach with memoization handles this, once we've visited both required nodes we just count paths forward without re-checking.
- State-Based Counting: Instead of storing entire paths, we only count the number of paths.

'''

data = helper.get_data(11).strip()

START = "svr"
END = "out"
MUST_VISIT = ('dac', 'fft')

graph = {}

def main():
    for line in data.split("\n"):
        key, value = line.split(":")
        graph[key] = value.split()
    
    return count_from(START, ())

@lru_cache(maxsize=None)
def count_from(node, visited_must):
    if node == END:
        return 1 if visited_must == MUST_VISIT else 0
    
    total = 0
    for next_node in graph[node]:
        new_visited = visited_must
        if next_node in MUST_VISIT and next_node not in visited_must:
            new_visited = tuple(sorted(set(visited_must) | {next_node}))
        
        total += count_from(next_node, new_visited)
    
    return total

if __name__ == "__main__":
    print(main())
