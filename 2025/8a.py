#!/usr/bin/env python3

'''
1. Parse 3D coordinates and calculate all pairwise Euclidean distances.
2. Sort pairs by distance and iteratively connect the closest points that are not already directly connected.
3. Merge connected circuits accordingly.
4. Multiply the sizes of the three largest circuits.
'''

from cmath import sqrt
import helper

data = helper.get_data(8).strip("\n").split("\n")

matrix = [list(map(int, line.split(','))) for line in data]
STEPS = 1000
LARGEST = 3

distances = []

circuits = []
direct_connections = []
def main():
    for p1 in matrix:
        for p2 in matrix:
            if p1 == p2:
                continue
            distances.append((p1, p2, calculate_distance(p1, p2)))

    distances.sort(key=lambda x: x[2])

    for _ in range(STEPS):
        p1, p2, _ = distances.pop(0)
        while directly_connected(p1, p2):
            p1, p2, _ = distances.pop(0)
        add_connection(p1, p2)
    
    circuits.sort(key=len)

    result = 1
    for _ in range(LARGEST):
        result *= len(circuits.pop())

    return result

def add_connection(node1, node2):
    if directly_connected(node1, node2):
        return
    
    direct_connections.append((node1, node2))

    circuit1 = None
    circuit2 = None
    for circuit in circuits:
        if node1 in circuit:
            circuit1 = circuit
        if node2 in circuit:
            circuit2 = circuit
    
    if circuit1 and circuit2 and circuit1 == circuit2:
        return
    
    if not circuit1 and not circuit2:
        circuits.append([node1, node2])
        return
    
    if circuit1 and not circuit2:
        circuit1.append(node2)
        return
    
    if circuit2 and not circuit1:
        circuit2.append(node1)
        return
    
    circuits.remove(circuit1)
    circuits.remove(circuit2)
    circuits.append(circuit1 + circuit2)

def directly_connected(node1, node2):
    for connection in direct_connections:
        if node1 in connection and node2 in connection:
            return True
    return False

def calculate_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2).real

if __name__ == "__main__":
    print(main())
