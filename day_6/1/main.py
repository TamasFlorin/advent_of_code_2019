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
    return graph

def dfs(start, graph):
    if not start in graph:
        return 0
    for node in graph[start]:
        return 1 + dfs(node, graph)
    return 0

def solve(graph: Dict[str, List[str]]) -> int:
    reachable = 0
    for node in graph.keys():
        reachable += dfs(node, graph)
    return reachable

if __name__ == "__main__":
    map_data = read_map_data(sys.argv[1])
    graph = build_graph(map_data)
    print(solve(graph))
