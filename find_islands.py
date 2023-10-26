from collections import deque
from queue import PriorityQueue


islands1 = '''1010001111
0010101000
1111001000
1001010000
1111000111
0101001111
0000011100
0001001110
1010100100
1111000111
'''


class Node:
    def __init__(self, state, parent, action, path_cost=None):
        self.state = state  # текущее состояние
        self.parent = parent  # node
        self.action = action  # действие
        self.path_cost = path_cost  # Стоимость пути


class Frontier():
    def __init__(self, frontier_type):
        if frontier_type.lower() not in ("priority", "fifo", "lifo"):
            raise ValueError("Unsupported frontier type")
        self.frontier_type = frontier_type.lower()

        if self.frontier_type in ("fifo", "lifo"):
            self.queue = deque()
        else:
            self.queue = PriorityQueue()

    def add(self, node):
        if self.frontier_type in ("fifo", "lifo"):
            self.queue.append(node)
        else:
            self.queue.put((node.path_cost, node))

    def get(self):
        if self.frontier_type == 'lifo':
            return self.queue.pop()
        elif self.frontier_type == 'fifo':
            return self.queue.popleft()
        else:
            return self.queue.get()

    def empty(self):
        if self.frontier_type in ("fifo", "lifo"):
            return len(self.queue) == 0
        else:
            self.queue.empty()

    def contains_state(self, state):
        return any(node.state == state for node in self.queue)


class Islands():
    def __init__(self, islands):

        contents = islands

        self.contents = contents.splitlines()
        self.height = len(self.contents)
        self.width = max(len(line) for line in self.contents)

    def neighbors(self, state):

        row, col = state

        candidates = [
            ("up-left", (row - 1, col-1)),
            ("up", (row - 1, col)),
            ("up-right", (row - 1, col+1)),
            ("right", (row, col + 1)),
            ("down-right", (row + 1, col + 1)),
            ("down", (row + 1, col)),
            ("down-left", (row + 1, col - 1)),
            ("left", (row, col - 1))
        ]

        result = []

        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and self.contents[r][c] != '0':
                result.append((action, (r, c)))
        return result

    def find_ones(self):
        list_of_ones = []
        for i in range(self.height):
            for j in range(self.width):
                if self.contents[i][j] == '1':
                    list_of_ones.append((i, j))
        return list_of_ones

    def find_islands(self):
        starts = self.find_ones()
        start = Node(state=starts[0], parent=None, action=None)

        frontier = Frontier("LIFO")
        #frontier = Frontier("FIFO")

        frontier.add(start)

        self.explored = set()

        list_of_islands = []

        island_test = []

        while True:

            node = frontier.get()

            self.explored.add(node.state)

            island_test.append(node.state)

            starts.remove(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

            if frontier.empty() and len(starts) != 0:
                list_of_islands.append(island_test)
                island_test = []
                start = Node(state=starts[0], parent=None, action=None)
                frontier.add(start)
            elif frontier.empty() and len(starts) == 0:
                list_of_islands.append(island_test)
                print(list_of_islands)
                return len(list_of_islands)


l = Islands(islands1)

print(l.find_islands())
