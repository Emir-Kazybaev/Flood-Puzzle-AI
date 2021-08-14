import math
from collections import deque
from heapq import heappop, heappush
import time


class Solver:
    def __init__(self, start_node):
        self.nodes = deque([start_node], maxlen=1000000)
        self.start_node = start_node
        self.key = None
        self.id_set = {}
        self.solved = False
        self.NN = len(start_node.grid)
        self.start_time = time.time()
        self.nodes_explored = 0

    def bfs(self):
        while not self.solved:
            children = deque()
            for color in self.nodes[0].child_colors:
                self.nodes_explored += 1
                node = self.nodes[0].child_node()
                node.start_coloring(color)
                node.generate_id()
                if node.solution_ready():
                    self.solved = True
                    self.key = node
                if node.node_id not in self.id_set:
                    self.id_set[node.node_id] = node
                    children.append(node)
            self.nodes.popleft()
            self.nodes.extend(children)
        return self.get_solution()

    def optimized_bfs(self):
        while not self.solved:
            children = deque()
            flag = False
            parent_node = self.nodes.popleft()
            for color in parent_node.child_colors:
                self.nodes_explored += 1
                node = parent_node.child_node()
                if flag:
                    if node.start_coloring(color):
                        node.generate_id()
                    if node.solution_ready():
                        self.solved = True
                        self.key = node
                    if node.node_id not in self.id_set:
                        self.id_set[node.node_id] = node
                        children.append(node)
                        self.nodes.append(node)
                else:
                    if node.start_coloring(color):
                        flag = True
                        children.clear()
                    node.generate_id()
                    if node.solution_ready():
                        self.solved = True
                        self.key = node
                    if node.node_id not in self.id_set:
                        self.id_set[node.node_id] = node
                        children.append(node)
            self.nodes.extend(children)
        return self.get_solution()

    def des(self):
        list_of_queues = []
        depth = 0
        next_depth = 1
        list_of_queues.append(deque([self.start_node]))
        while True:
            list_of_queues.append(deque())
            flag = False
            while len(list_of_queues[depth]):
                parent_node = list_of_queues[depth].popleft()
                for color in parent_node.child_colors:
                    self.nodes_explored += 1
                    node = parent_node.child_node()
                    if flag:
                        if node.start_coloring(color):
                            node.generate_id()
                            if node.solution_ready():
                                self.solved = True
                                self.key = node
                                return self.get_solution()
                            list_of_queues[next_depth].append(node)
                            if node.node_id not in self.id_set:
                                self.id_set[node.node_id] = node
                    else:
                        if node.start_coloring(color):
                            node.generate_id()
                            if node.solution_ready():
                                self.solved = True
                                self.key = node
                                return self.get_solution()
                            flag = True
                            list_of_queues[next_depth].clear()
                            list_of_queues[next_depth].append(node)
                        else:
                            node.generate_id()
                            if node.node_id not in self.id_set:
                                self.id_set[node.node_id] = node
                                list_of_queues[next_depth].append(node)
            depth += 1
            next_depth += 1

    def a_star(self):
        pq = self.PriorityQueue(self.start_node)
        while not self.solved:
            parent_node = pq.pop()
            for color in parent_node.child_colors:
                node = parent_node.child_node()
                node.start_coloring(color)
                node.generate_id()
                if node.solution_ready():
                    self.key = node
                    self.solved = True
                    break
                if node.node_id not in self.id_set:
                    self.id_set[node.node_id] = node
                    pq.add(node)
        self.nodes_explored = pq.num
        return self.get_solution()

    def get_solution(self):
        last_node = self.key.child_node()
        last_node.start_coloring(list(last_node.colors_num.keys())[0])
        last_node.generate_id()
        end_time = time.time()
        solution = []
        current_node = last_node
        solution.append(current_node)
        while True:
            current_node = current_node.parent
            solution.append(current_node)
            if current_node.parent is self.start_node:
                break
        solution.reverse()
        coloring_path = ''
        for n in range(len(solution)):
            coloring_path += solution[n].color
        return solution, len(solution), end_time - self.start_time, self.nodes_explored, coloring_path

    class PriorityQueue:
        def __init__(self, start_node):
            self.prior_que = []
            self.NN = len(start_node.grid)
            self.STEP_COST = math.sqrt(self.NN) * 2
            self.num = 0
            heappush(self.prior_que, (start_node.steps * self.STEP_COST - len(start_node.filled_indexes), 0, start_node))

        def add(self, node):
            self.heuristic(node)
            self.num += 1
            heappush(self.prior_que, (node.score, self.num, node))

        def pop(self):
            return heappop(self.prior_que)[2]

        def empty(self):
            return not self.prior_que

        def heuristic(self, node):
            if node.steps != 0:
                node.score = node.parent.score + self.STEP_COST - node.last_fill
            else:
                node.score = self.NN - len(node.filled_indexes)
