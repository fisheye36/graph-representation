import matplotlib.pyplot as plt
import math
import sys

def make_plot(data):
    nodes = len(data)
    edges = sum([sum(row) for row in data]) // 2

    nodes_x = [] # coordinates of nodes
    nodes_y = []
    radius = 10
    for i in range(nodes): # calculate coordinates
        nodes_x.append(radius * math.cos(i * 2.0 * math.pi / nodes))
        nodes_y.append(radius * math.sin(i * 2.0 * math.pi / nodes))

    fig = plt.figure(figsize=(10, 10), dpi=100) # create plot workspace
    plt.scatter(nodes_x, nodes_y) # draw nodes
    offset = radius / 20
    for i in range(nodes): # draw node numbers
        plt.annotate(i + 1, (nodes_x[i] + offset, nodes_y[i] + offset))

    for y in range(nodes):
        for x in range(y + 1, nodes):
            if data[x][y] == 1: # draw edge when there is a connection between nodes
                edge_x = [nodes_x[y], nodes_x[x]]
                edge_y = [nodes_y[y], nodes_y[x]]
                plt.plot(edge_x, edge_y)

    plt.show()
