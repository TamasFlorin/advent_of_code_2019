import sys
from typing import Dict, List

def read_map_data(filename):
    data = []
    with open(filename) as f:
        for line in f:
            tokens = line.split(')')
            data.append((tokens[0].strip('\n'), tokens[1].strip('\n')))
    return data

def build_graph(map_data):
    graph = {}
    for pair in map_data:
        (p1, p2) = pair
        if p2 in graph:
            graph[p2].append(p1)
        else:
            graph[p2] = [p1]
        if p1 in graph:
            graph[p1].append(p2)
        else:
            graph[p1] = [p2]
    return graph

def bfs(start, end, graph):
    q = [(start, 0)]
    visited = {start : True}
    while len(q) != 0:
        item, dist = q.pop(0)
        if item == end:
            return dist

        for node in graph[item]:
            if node not in visited:
                q.append((node, dist + 1))
                visited[node] = True
    return -1 # not found

if __name__ == "__main__":
    map_data = read_map_data(sys.argv[1])
    graph = build_graph(map_data)
    print(bfs('S2C', 'QKC', graph))