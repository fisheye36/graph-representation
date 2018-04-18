class Writer:
    def write_as_adjacency_list(self, file_name, data):
        nodes_num = len(data)
        file_name = self._modify_file_name(file_name, "-al")
        print("Writing file '{}'...".format(file_name))

        with open(file_name, mode="wt", encoding="utf-8") as file:
            file.write("adjacency-list: {}\n\n".format(nodes_num))
            node_no = 1
            for row in data:
                nodes = [index + 1 for index, value in enumerate(row) if value == 1]
                file.write("{} : {}\n".format(node_no,
                                              " ".join(str(node) for node in nodes)))
                node_no += 1

    def write_as_adjacency_matrix(self, file_name, data):
        nodes_num = len(data)
        file_name = self._modify_file_name(file_name, "-am")
        print("Writing file '{}'...".format(file_name))

        with open(file_name, mode="wt", encoding="utf-8") as file:
            file.write("adjacency-matrix: {}\n\n".format(nodes_num))
            node_no = 1
            for row in data:
                file.write("{} : {}\n".format(node_no,
                                              " ".join(str(node) for node in row)))
                node_no += 1

    def write_as_incidence_matrix(self, file_name, data):
        nodes_num = len(data)
        edges_num = sum([sum(row) for row in data]) // 2
        file_name = self._modify_file_name(file_name, "-im")
        print("Writing file '{}'...".format(file_name))

        matrix = [[0 for node in range(edges_num)] for rows in range(nodes_num)]
        index = 0
        for row in range(nodes_num):
            for node in range(row + 1, nodes_num):
                if data[row][node] == 1:
                    matrix[row][index] = matrix[node][index] = 1
                    index += 1

        with open(file_name, mode="wt", encoding="utf-8") as file:
            file.write("incidence-matrix: {} {}\n\n".format(nodes_num, edges_num))
            node_no = 1
            for row in matrix:
                file.write("{} : {}\n".format(node_no,
                                              " ".join(str(node) for node in row)))
                node_no += 1

    def _modify_file_name(self, file_name, suffix):
        prefix, dot, extension = file_name.rpartition(".")
        return "".join((prefix + suffix, dot, extension))
