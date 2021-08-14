class Node:
    def __init__(self, parent, board, color, N, steps, colors_num, filled_indexes, neighbor_indexes, child_colors):
        self.parent = parent
        self.grid = board
        self.color = color
        self.steps = steps
        self.N = N
        self.colors_num = colors_num
        self.score = 0
        self.node_id = ""
        self.child_colors = child_colors
        self.filled_indexes = filled_indexes
        self.neighbor_indexes = neighbor_indexes
        self.last_fill = 0

    def start_coloring(self, color):
        self.color = color
        self.last_fill = len(self.filled_indexes)
        for ind in self.neighbor_indexes.copy():
            if self.grid[ind] == self.color:
                self._coloring(ind)
                self.neighbor_indexes.remove(ind)
        self.last_fill = (len(self.filled_indexes) - self.last_fill)
        self.colors_num[self.color] -= self.last_fill
        self.child_colors.discard(color)
        for k, v in self.colors_num.items():
            if v == 0:
                del self.colors_num[k]
                return k

    def _coloring(self, ind):
        self.filled_indexes.add(ind)
        if (ind + 1) % self.N != 0 and self._legal(ind + 1):
            self._coloring(ind + 1)
        if self._legal(ind + self.N):
            self._coloring(ind + self.N)
        if self._legal(ind - self.N):
            self._coloring(ind - self.N)
        if ind % self.N != 0 and self._legal(ind - 1):
            self._coloring(ind - 1)

    def _legal(self, ind):
        if ind not in self.filled_indexes and ind not in self.neighbor_indexes and 0 < ind < len(self.grid):
            if self.grid[ind] == self.color:
                return True
            self.neighbor_indexes.add(ind)
            self.child_colors.add(self.grid[ind])
        return False

    def solved(self):
        if len(self.colors_num) == 0:
            return True
        return False

    def solution_ready(self):
        if len(self.colors_num) <= 1:
            return True
        return False

    def generate_id(self):
        self.node_id = frozenset(self.filled_indexes)

    def child_node(self):
        return Node(self, self.grid, self.color, self.N, self.steps + 1, self.colors_num.copy(),
                    self.filled_indexes.copy(), self.neighbor_indexes.copy(), self.child_colors.copy())