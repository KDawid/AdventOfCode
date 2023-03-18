class GraphEdge:
    def __init__(self, from_node, to_node):
        self.nodes = {from_node, to_node}

    def get_nodes(self):
        return self.nodes

    def __str__(self):
        nodes = list(self.nodes)
        return f'{nodes[0]} - {nodes[1]}'


class Graph:
    START_NODE = 'start'
    END_NODE = 'end'

    def __init__(self, edges, max_lower_edge=1):
        self.edges = edges
        self.max_lower_edge = max_lower_edge
        self.lower_nodes = self.__collect_lower_edges()

    def __collect_lower_edges(self):
        res = set()
        for edge in self.edges:
            for node in edge.get_nodes():
                if node.islower():
                    res.add(node)
        return res

    def generate_paths(self):
        start_node = Graph.START_NODE
        paths = self.__generate_paths(start_node, {start_node: self.max_lower_edge+1}, start_node, [])
        return set(paths)

    def __generate_paths(self, act_node, used_lower_nodes, prefix, paths):
        destinations = self.__collect_possible_next_steps(act_node, used_lower_nodes)
        for destination in destinations:
            act_used_lower_nodes = {node: num for (node, num) in used_lower_nodes.items()}
            if destination.islower():
                Graph.__add_lower_nodes_reached(act_used_lower_nodes, destination)
            if destination == Graph.END_NODE:
                paths.append(f'{prefix}-{destination}')
            else:
                self.__generate_paths(destination, act_used_lower_nodes, f'{prefix}-{destination}', paths)
        return paths

    def __collect_possible_next_steps(self, act_node, used_lower_nodes):
        if act_node == Graph.END_NODE:
            return set()
        res = set()
        for edge in self.edges:
            nodes = list(edge.get_nodes())
            if act_node in nodes:
                next_node = nodes[0] if nodes[0] != act_node else nodes[1]
                if next_node == Graph.START_NODE:
                    continue
                if next_node not in used_lower_nodes or self.__max_not_reached(used_lower_nodes):
                    res.add(next_node)
        return res

    @staticmethod
    def __add_lower_nodes_reached(lower_nodes, node):
        if node not in lower_nodes:
            lower_nodes[node] = 1
        else:
            lower_nodes[node] += 1

    def __max_not_reached(self, used_lower_nodes):
        without_start = {node: value for (node, value) in used_lower_nodes.items() if node != Graph.START_NODE}
        if len(without_start) == 0:
            return True
        return max(without_start.values()) < self.max_lower_edge

    def __str__(self):
        res = ''
        for edge in self.edges:
            res += str(edge) + '\n'
        return res


def first_task(file_path):
    graph = Graph(read_data(file_path))
    return len(graph.generate_paths())


def read_data(file_path):
    edges = []
    with open(file_path) as f:
        for line in f.readlines():
            from_node, to_node = line.strip().split('-')
            edges.append(GraphEdge(from_node, to_node))
    return edges


def second_task(file_path):
    graph = Graph(read_data(file_path), max_lower_edge=2)
    return len(graph.generate_paths())


if __name__ == '__main__':
    FILE_PATH = 'input.txt'
    res_1 = first_task(FILE_PATH)
    print(res_1)
    res_2 = second_task(FILE_PATH)
    print(res_2)
