class Node:
    def __init__(self, data):
        self.data = data
        self.neighbors = []
        self.in_degree = 0

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __str__(self):
        return str(self.data)


class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class DependencyGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.nodeTable = {}

    def __add_node(self, data):
        node = Node(data)
        self.nodes.append(node)
        return node

    def __get_node_by_hash_table(self, data):
        hash_data = (data[0], str(data[1]))
        if hash_data in self.nodeTable:
            node = self.nodes[self.nodeTable[hash_data]]
        else:
            node = self.__add_node(data)
        return node

    def __add_edge(self, start_data, end_data):
        start_node = self.__get_node_by_hash_table(start_data)
        end_node = self.__get_node_by_hash_table(end_data)

        edge = Edge(start_node, end_node)
        self.edges.append(edge)
        start_node.add_neighbor(end_node)
        end_node.add_neighbor(start_node)

    def __str__(self):
        result = []
        for edge in self.edges:
            result.append(f"{edge.start} <-> {edge.end}")
        return "\n".join(result)

    def __createNode(self, block):
        for data in block:
            self.__add_node(data)
            key = (data[0], str(data[1]))
            self.nodeTable[key] = len(self.nodes) - 1

    def build_dependency_Graph(self, block, dependency_table, addition_relation):
        self.__createNode(block)
        length = len(dependency_table)
        for index in range(length):
            for target_index in dependency_table[index]:
                self.__add_edge(block[index], block[target_index])
        return
