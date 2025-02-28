import itertools
from Manager import getTestcase, load_input, measure_performance, write_result

class MasyuPuzzle:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def check_goal(self, path, count):
        if count > 0:
            return False
        if path[-1] != path[0]:
            return False

        startPos = path[0]

        if self.board[startPos[0]][startPos[1]] == -1:
            return True
        else:
            if self.is_turn(path[-2], path[1]):
                return False
            if not self.is_turn(startPos, path[-3]) and not self.is_turn(startPos, path[2]):
                return False
            return True

    def pos_valid(self, pos):
        return 0 <= pos[0] < self.size and 0 <= pos[1] < self.size

    def is_turn(self, prePos, nextPos):
        return prePos[0] != nextPos[0] and prePos[1] != nextPos[1]

    def filter_directions(self, steps, prePos, currPos, need_to_turn, need_to_straight):
        if need_to_straight and need_to_turn:
            return []
        temp = []
        for dx, dy in steps:
            nextPos = (dx + currPos[0], dy + currPos[1])
            if not self.pos_valid(nextPos):
                continue

            if need_to_turn and self.is_turn(prePos, nextPos):
                temp.append((dx, dy))
            elif need_to_straight and not self.is_turn(prePos, nextPos):
                temp.append((dx, dy))
            elif not need_to_turn and not need_to_straight:
                temp.append((dx, dy))
        return temp

    def movements(self, path, count):
        currPos = path[-1]

        if len(path) <= 1:
            for dx, dy in self.directions:
                x, y = dx + currPos[0], dy + currPos[1]
                if self.pos_valid((x, y)):
                    new_path = path + [(x, y)]
                    new_count = count - (self.board[x][y] != 0)
                    yield new_path, new_count
            return

        prePos = path[-2]
        need_to_turn = False
        need_to_straight = False

        if self.board[currPos[0]][currPos[1]] == 1 or self.board[prePos[0]][prePos[1]] == -1:
            need_to_straight = True

        if self.board[currPos[0]][currPos[1]] == -1:
            need_to_turn = True
        if self.board[prePos[0]][prePos[1]] == 1 and len(path) >= 4 and not self.is_turn(path[-4], path[-2]):
            need_to_turn = True

        next_steps = self.filter_directions(self.directions, prePos, currPos, need_to_turn, need_to_straight)

        for dx, dy in next_steps:
            x, y = dx + currPos[0], dy + currPos[1]
            nextPos = (x, y)
            if nextPos in path and not (nextPos == path[0] and count == 0):
                continue
            if self.board[x][y] == -1 and self.is_turn(prePos, nextPos):
                continue
            new_path = path + [nextPos]
            new_count = count - (self.board[nextPos[0]][nextPos[1]] != 0)
            yield new_path, new_count

class State:
    def __init__(self, path, circle_count=0):
        self.path = path
        self.circle_count = circle_count

    def expand(self, puzzle):
        return [State(path, count) for path, count in puzzle.movements(self.path, self.circle_count)]

class AStarSearcher:
    def __init__(self, board):
        self.board = board
        self.size = len(board)
        self.puzzle = MasyuPuzzle(board)
        self.start = None
        self.initialize()

    def initialize(self):
        start_point = (-1, -1)
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    count += 1
                    if start_point == (-1, -1):
                        start_point = (i, j)

        self.start = State([start_point], count - 1)

    def heuristic(self, state):
        curren_pos = state.path[-1]
        start_pos = self.start.path[0]

        manhattan_distance = abs(curren_pos[0] - start_pos[0]) + abs(curren_pos[1] - start_pos[1])
        #euclidean_distance = math.sqrt((curren_pos[0] - start_pos[0]) ** 2 + (curren_pos[1] - start_pos[1]) ** 2)

        #
        return manhattan_distance + state.circle_count *3

    def a_star_search(self):
        import heapq
        open_set = []
        closed_set = set()
        came_from = {}
        counter = itertools.count()

        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start)}

        heapq.heappush(open_set, (f_score[self.start], next(counter), self.start))

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if self.puzzle.check_goal(current.path, current.circle_count):
                print("Found")
                print(current.path)
                write_result(2, testcase, current.path)
                return

            for neighbor in current.expand(self.puzzle):
                if current in closed_set:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)
                    heapq.heappush(open_set, (f_score[neighbor], next(counter), neighbor))

            closed_set.add(current)

        print("Not found")

if __name__ == "__main__":
    testcase = getTestcase()
    board = load_input(testcase)

    searcher = AStarSearcher(board)
    measure_performance(searcher.a_star_search)

