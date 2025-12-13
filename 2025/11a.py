import helper

'''
Find shortest path in a graph using BFS.
- Parse adjacency list from input.
- Start BFS from 'you' to find 'out'.
- Return the length of the path.
'''

data = helper.get_data(11).strip()


def main():
    graph = {}
    for line in data.split("\n"):
        key, value = line.split(":")
        graph[key] = value.split()

    start = "you"
    end = "out"

    queue = [(start,)]
    paths = []
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            paths.append(path)
            continue
        queue.extend((path + (n,)) for n in graph[node])
    
    return len(paths)

if __name__ == "__main__":
    print(main())
