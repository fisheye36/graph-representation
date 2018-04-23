from parser import AdjacencyListParser, AdjacencyMatrixParser, IncidenceMatrixParser
import plot as gp

import random as rd
import sys

class GraphException(Exception):
    pass

class Graph:
    def _read(self, file_name):
        print("Opening file '{}'...".format(file_name))
        with open(file_name, mode="rt", encoding="utf-8") as file:
            lines = file.read().splitlines()

        lines = self._remove_comments(lines)
        graph_type, args = self._read_type_and_args(lines[0])

        self._parser = self._get_parser(graph_type, args)
        self._graph_data, self._nodes = self._parser.parse_data(lines[1:])

    def convert(self, file_name):
        self._read(file_name)
        self._parser.write_data(file_name, self._graph_data)

    def display(self, file_name):
        pass
#        self._read(file_name)
#        gp.make_plot(self._graph_data)

    def generate(self, file_name, nodes_num, edges_or_probability):
        suffix = edges_or_probability[-1]
        if suffix == "e":
            self._gen_edges(file_name, nodes_num, int(edges_or_probability[:-1]))
        elif suffix == "p":
            self._gen_probability(file_name, nodes_num, float(edges_or_probability[:-1]))
        else:
            raise ValueError("invalid suffix in '{}'".format(edges_or_probability))

    def _gen_edges(self, file_name, nodes_num, edges_num):
        # create empty incidence matrix
        matrix = [[0 for edge in range(edges_num)] for node in range(nodes_num)]
        for edge in range(edges_num):
            values_changed = 0
            while values_changed != 2: # check if edge has been set
                node = rd.randrange(nodes_num)

                if matrix[node][edge] == 1:
                    continue
                matrix[node][edge] = 1
                values_changed += 1

        # write incidence matrix
        with open(file_name, mode="wt", encoding="utf-8") as file:
            file.write("incidence-matrix: {} {}\n\n".format(nodes_num, edges_num))
            node_no = 1
            for row in matrix:
                file.write("{} : {}\n".format(node_no,
                                              " ".join(str(node) for node in row)))
                node_no += 1

    def _gen_probability(self, file_name, nodes_num, prob):
        if prob < 0.0: prob = 0.0
        elif prob > 1.0: prob = 1.0

        # create empty adjacency matrix
        matrix = [[0 for node in range(nodes_num)] for node in range(nodes_num)]
        for y in range(nodes_num):
            for x in range(y + 1, nodes_num):
                if rd.random() <= prob:
                    matrix[x][y] = matrix[y][x] = 1

        # write adjacency matrix
        with open(file_name, mode="wt", encoding="utf-8") as file:
            file.write("adjacency-matrix: {}\n\n".format(nodes_num))
            node_no = 1
            for row in matrix:
                file.write("{} : {}\n".format(node_no,
                                              " ".join(str(node) for node in row)))
                node_no += 1

    def _remove_comments(self, lines):
        stripped_lines = []
        for line in lines:
            line, _, _ = line.strip().partition("#")
            if len(line) > 0:
                stripped_lines.append(line)

        return stripped_lines

    def _read_type_and_args(self, header_line):
        ret = header_line.split(":")
        return ret[0], ret[1]

    def _get_parser(self, graph_type, args):
        if graph_type == "adjacency-list":
            return AdjacencyListParser(int(args))
        elif graph_type == "adjacency-matrix":
            return AdjacencyMatrixParser(int(args))
        elif graph_type == "incidence-matrix":
            sizes = args.split()
            return IncidenceMatrixParser(int(sizes[0]), int(sizes[1]))
        else:
            raise GraphException("unknown graph representation")

def print_help():
    print("usage: python {} <command> <file_name> [nodes] [extra]".format(sys.argv[0]))
    print("available commands:")
    print("'convert'  -- converts <file_name> to remaining representations")
    print("'display'  -- display graph from <file_name>")
    print("'generate' -- generate graph based upon [extra] with [nodes] nodes")
    print("              [extra] is either number of edges, e.g. '10e'")
    print("              or probability that edge exists between nodes, e.g. '0.5p'")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] == "help":
        print_help()

    g = Graph()
    if sys.argv[1] == "convert":
        g.convert(sys.argv[2])
    elif sys.argv[1] == "display":
        g.display(sys.argv[2])
    elif sys.argv[1] == "generate":
        if len(sys.argv) < 5:
            print_help()
        g.generate(sys.argv[2], int(sys.argv[3]), sys.argv[4])
