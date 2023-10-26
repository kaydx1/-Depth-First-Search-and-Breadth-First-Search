import time
from collections import deque
from queue import PriorityQueue


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


class Letters():
    def __init__(self, letters):

        # Read letters
        contents = letters

        # Determine height and width of board
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
            if 0 <= r < self.height and 0 <= c < self.width:
                result.append((action, (r, c)))
        return result

    # Проверка на повторение букв с одинаковой позицией в матрице в дереве

    def contains_parents(self, node):

        state = node.state

        while node.parent is not None:
            node = node.parent
            if state == node.state:
                return True

        return False

    # Поиск в ширину

    def bfs(self, word, start_pos):

        frontier = Frontier("FIFO")  # bfs

        self.explored = set()

        # Все возможные позиции начала слова(его первой буквы)
        for pos in start_pos:

            start = Node(state=pos, parent=None, action=None)

            frontier.add(start)

            path = ''

            while True:

                if frontier.empty():
                    break

                node = frontier.get()

                # if self.contents[node.state[0]][node.state[1]] not in word:
                #     self.explored.add(
                #         self.contents[node.state[0]][node.state[1]])

                for action, state in self.neighbors(node.state):

                    child = Node(state=state, parent=node, action=action)

                    if not self.contains_parents(child) and self.contents[child.state[0]][child.state[1]] in word:
                        frontier.add(child)

                path = ''

                while node.parent is not None:
                    path += self.contents[node.state[0]][node.state[1]]
                    node = node.parent

                path += self.contents[pos[0]][pos[1]]

                path = path[::-1]

                # if len(path) > len(word):
                #     return False

                if path == word:
                    return True

    def solve(self, words):

        start_pos = {}

        for word in words:  # Составляем словарь слов и возможных позиций их начала
            for row in range(self.height):
                for col in range(self.width):
                    if self.contents[row][col] == word[0]:
                        if (word not in start_pos):
                            start_pos[word] = [(row, col)]
                        else:
                            start_pos[word].append((row, col))
        print(start_pos)

        solution = []

        for word in start_pos:
            if self.bfs(word, start_pos[word]):
                solution.append(word)
        print(solution)


time_start = time.time()

letters = '''MSEF
RATD
LONE
KAFB
'''

words = ['ATA', 'NOTE', 'SAND', 'STONED']

m = Letters(letters)

m.solve(words)

print(m.contents)

print(time.time() - time_start)
