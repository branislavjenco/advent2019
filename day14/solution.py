from utils import file_into_list, test
import math
from queue import Queue


class Node:
    def __init__(self,  name):
        self.name = name
        self.out_edges = set()
        self.in_edges = set()
        self.value = 0
        self.processed = 0

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name + "(" + str(self.value) + ")"


class Edge:
    def __init__(self, start, end, out_val, in_val):
        self.start = start
        self.out_val = out_val
        self.end = end
        self.in_val = in_val

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.start == other.start and self.end == other.end

    def __hash__(self):
        return hash(self.start) + hash(self.end)

    def __repr__(self):
        return "Edge from " + str(self.start) + " to " + str(self.end)


def add_to_graph(line, nodes):
    sides = line.split(" => ")
    out_val, name = sides[1].split(" ")
    if name in nodes:
        out_node = nodes[name]
    else:
        out_node = Node(name)
        nodes[name] = out_node

    spl = sides[0].split(", ")
    for target in spl:
        in_val, target_name = target.split(" ")
        if target_name in nodes:
            target_node = nodes[target_name]
        else:
            target_node = Node(target_name)
            nodes[target_name] = target_node
        edge = Edge(out_node, target_node, int(out_val), int(in_val))
        out_node.out_edges.add(edge)
        target_node.in_edges.add(edge)


def input_to_graph(filename):
    graph = {}
    lines = file_into_list(filename)
    for line in lines:
        add_to_graph(line, graph)
    return graph


solution_graph = input_to_graph("day14/input.txt")
test_graph_1 = input_to_graph("day14/test_input_1.txt")
test_graph_2 = input_to_graph("day14/test_input_2.txt")
test_graph_3 = input_to_graph("day14/test_input_3.txt")
test_graph_4 = input_to_graph("day14/test_input_4.txt")
test_graph_5 = input_to_graph("day14/test_input_5.txt")

test_graphs = [test_graph_1, test_graph_2, test_graph_3, test_graph_4, test_graph_5]

expected_1 = 31
expected_2 = 165
expected_3 = 13312
expected_4 = 180697
expected_5 = 2210736

expecteds = [expected_1, expected_2, expected_3, expected_4, expected_5]


def find_minimum_ore(graph, start_val=1):
    def calculate_children(queue):
        node = queue.get()
        for edge in node.out_edges:
            node_value = math.ceil(node.value / edge.out_val)
            edge.end.value = edge.end.value + (edge.in_val * node_value)
            edge.end.processed += 1
            if edge.end.processed == len(edge.end.in_edges):
                queue.put(edge.end)
        node.processed = True
        if queue.empty():
            return
        calculate_children(queue)

    start_node = graph['FUEL']
    start_node.value = start_val
    q = Queue()
    q.put(start_node)
    calculate_children(q)
    return graph


def part_1():
    test(lambda graph: find_minimum_ore(graph)["ORE"].value, test_graphs, expecteds)
    return find_minimum_ore(solution_graph)["ORE"].value


# print(part_1())

def find_maximum_fuel(filename):
    fuel = 1000
    diff = 1000
    while True:
        input_graph = input_to_graph(filename)
        filled_graph = find_minimum_ore(input_graph, fuel)
        if filled_graph["ORE"].value < 1000000000000:
            fuel += diff
        else:
            if diff == 1000:
                fuel = fuel - 1000
                diff = 1
            elif diff == 1:
                break
    return fuel - 1


# Extremely slow way of doing part 2 but I spent too much time trying to implement copy
# deepcopy for my Node and Edge classes without success (to be able to clone graphs)
# Therefore I parse the input many times in the find_maximum_fuel function again and again
def part_2():
    test(lambda filename: find_maximum_fuel(filename), ["day14/test_input_3.txt", "day14/test_input_4.txt", "day14/test_input_5.txt"], [82892753, 5586022, 460664])
    print(find_maximum_fuel("day14/input.txt"))

part_2()
