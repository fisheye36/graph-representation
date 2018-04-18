from writer import Writer

class ParserError(Exception):
    pass


class Parser():
    def parse_data(self, lines):
        raise NotImplementedError()

    def write_data(self, file_name, data):
        raise NotImplementedError()


class AdjacencyListParser(Parser):
    def __init__(self, nodes_num):
        self._nodes_num = nodes_num
        self._writer = Writer()

    def parse_data(self, lines):
        if self._nodes_num != len(lines):
            raise ParserError(
                "number of nodes ({}) doesn't match file contents ({} data lines)".format(
                    self._nodes_num, len(lines)))

        data = []
        for line in lines:
            row = [0] * self._nodes_num
            nodes = line.split(":")[1]
            for node in nodes.split():
                row[int(node) - 1] = 1
            data.append(row)

        return data, self._nodes_num

    def write_data(self, file_name, data):
        self._writer.write_as_adjacency_matrix(file_name, data)
        self._writer.write_as_incidence_matrix(file_name, data)


class AdjacencyMatrixParser(Parser):
    def __init__(self, nodes_num):
        self._nodes_num = nodes_num
        self._writer = Writer()

    def parse_data(self, lines):
        if self._nodes_num != len(lines):
            raise ParserError(
                "number of nodes ({}) doesn't match file contents ({} data lines)".format(
                    self._nodes_num, len(lines)))

        data = []
        for line in lines:
            row = []
            nodes = line.split(":")[1]
            for node in nodes.split():
                row.append(int(node))
            data.append(row)

        return data, self._nodes_num

    def write_data(self, file_name, data):
        self._writer.write_as_adjacency_list(file_name, data)
        self._writer.write_as_incidence_matrix(file_name, data)


class IncidenceMatrixParser(Parser):
    def __init__(self, nodes_num, edges_num):
        self._nodes_num = nodes_num
        self._edges_num = edges_num
        self._writer = Writer()

    def parse_data(self, lines):
        if self._nodes_num != len(lines):
            raise ParserError(
                "number of nodes ({}) doesn't match file contents ({} data lines)".format(
                    self._nodes_num, len(lines)))

        matrix = []
        for line in lines:
            row = [int(node) for node in line.split(":")[1].split()]

            if self._edges_num != len(row):
                raise ParserError(
                    "number of edges ({}) doesn't match file contents ({} data columns)"
                    .format(self._edges_num, len(row)))

            matrix.append(row)

        data = [[0 for node in range(self._nodes_num)] for row in range(self._nodes_num)]
        transposed_matrix = [list(i) for i in zip(*matrix)] # transpose matrix
        for row in transposed_matrix:
            x, y = tuple([index for index, value in enumerate(row) if value == 1])
            data[x][y] = data[y][x] = 1

        return data, self._nodes_num

    def write_data(self, file_name, data):
        self._writer.write_as_adjacency_list(file_name, data)
        self._writer.write_as_adjacency_matrix(file_name, data)
