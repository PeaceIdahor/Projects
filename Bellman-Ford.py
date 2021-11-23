# Python3 program for Bellman-Ford's single source
# shortest path algorithm.

from pythonds.graphs import PriorityQueue, Graph, Vertex

# The main function that finds shortest distances from src to

# all other vertices using Bellman-Ford algorithm. The function
# also detects negative weight cycle

def BellmanFord(aGraph, src):
    dist = {}
    # Step 1: Initialize distances from src to all other vertices
    # as INFINITE
    for v in aGraph.getVertices():
        if v  == src:
            dist[v] = 0
        else:
            dist[v] = float('inf')

    # Step 2: Relax all edges |V| - 1 times. A simple shortest
    # path from src to any other vertex can have at-most |V| - 1
    # edge
    for v in aGraph:
        # Update dist value and parent index of the adjacent vertices of
        # the picked vertex. Consider only those vertices which are still in
        # queue
        for nextVert in v.getConnections():
            if dist[v.id] != float("Inf") and dist[v.id] + v.getWeight(nextVert) < dist[nextVert.id]:
                dist[nextVert.id] = dist[v.id] + v.getWeight(nextVert)

    # print all distances
    for v in aGraph.getVertices():
        print("{0}\t\t{1}".format(v, dist[v]))


g = Graph()
g.addEdge("A","B",-1)
g.addEdge("A","C",4)
g.addEdge("B","C",3)
g.addEdge("B","D",2)
g.addEdge("B","E",2)
g.addEdge("D","B",1)
g.addEdge("D","C",5)
g.addEdge("E","D",-3)

BellmanFord(g,"A")