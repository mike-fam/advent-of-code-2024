import time
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import TypeVar, Generic, Optional
from collections import deque

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds.")
        return result

    return wrapper


class Operator(str, Enum):
    MULTIPLY = "*"
    ADD = "+"
    CONCAT = "||"


@dataclass
class Node:
    value: int

    def __post_init__(self):
        self.result: int = self.value
        self.children: dict[Operator, 'Node'] = {}
        self.parent: Optional[tuple[Operator, 'Node']] = None

    def add_child(self, child: 'Node', operator: Operator) -> None:
        self.children[operator] = child
        child.parent = (operator, self)

    def is_leaf(self):
        return len(self.children) == 0


@dataclass
class Tree:
    root: Node

    def bfs(self) -> list[Node]:
        queue = deque()
        queue.append(self.root)
        while len(queue) > 0:
            node = queue.pop()
            yield node
            for child in node.children.values():
                queue.append(child)


def get_data():
    data = {}
    with open("input.txt") as fin:
        for line in fin:
            line = line.strip()
            result, elements = line.split(": ")
            result = int(result)
            num_elements = list(map(int, elements.split(" ")))
            data[result] = num_elements
    return data


@timed
def part1():
    data = get_data()
    result_sum = 0
    for result, elements in data.items():
        previous_nodes = []
        tree = None
        # Build operation tree
        for element in elements:
            if len(previous_nodes) == 0:
                # Root node
                root_node = Node(element)
                previous_nodes = [root_node]
                tree = Tree(root_node)
                continue
            current_nodes = []
            for previous_node in previous_nodes:
                for operator in (Operator.MULTIPLY, Operator.ADD):
                    new_node = Node(element)
                    previous_node.add_child(new_node, operator)
                    current_nodes.append(new_node)
                previous_nodes = current_nodes
        for node in tree.bfs():
            if node.parent is None:
                continue
            operator, parent = node.parent
            if operator == Operator.MULTIPLY:
                node.value *= parent.value
            elif operator == Operator.ADD:
                node.value += parent.value
            if node.is_leaf() and node.value == result:
                result_sum += result
                break
    print(f"Part 1: {result_sum}")


@timed
def part2():
    data = get_data()
    result_sum = 0
    for result, elements in data.items():

        previous_nodes = []
        tree = None
        # Build operation tree
        for element in elements:
            if len(previous_nodes) == 0:
                # Root node
                root_node = Node(element)
                previous_nodes = [root_node]
                tree = Tree(root_node)
                continue
            current_nodes = []
            for previous_node in previous_nodes:
                for operator in (Operator.MULTIPLY, Operator.ADD, Operator.CONCAT):
                    new_node = Node(element)
                    previous_node.add_child(new_node, operator)
                    current_nodes.append(new_node)
                previous_nodes = current_nodes
        for node in tree.bfs():
            if node.parent is None:
                continue
            operator, parent = node.parent
            if operator == Operator.MULTIPLY:
                node.value *= parent.value
            elif operator == Operator.ADD:
                node.value += parent.value
            elif operator == Operator.CONCAT:
                node.value = int(str(parent.value) + str(node.value))
            if node.is_leaf() and node.value == result:
                result_sum += result
                break
    print(f"Part 2: {result_sum}")


if __name__ == "__main__":
    part1()
    part2()
