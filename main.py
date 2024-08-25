import math
import time
import random
import numpy as np
from collections import deque


class PacmanGame:
    def __init__(self, width=18, height=9):
        self.width = width
        self.height = height
        self.score = 0
        self.ground = np.zeros((height + 2, width + 2), dtype='int32')
        self.initial_dots(self.ground)
        self.initial_obstacles()
        self.pacman = {'x': 0, 'y': 0}
        self.ghost1 = {'x': 0, 'y': 0}
        self.ghost2 = {'x': 0, 'y': 0}
        while self.ground[self.pacman['y']][self.pacman['x']] == 4:
            self.pacman = {'x': random.randint(1, 18), 'y': random.randint(1, 9)}
        while self.ground[self.ghost1['y']][self.ghost1['x']] == 4:
            self.ghost1 = {'x': random.randint(1, 18), 'y': random.randint(1, 9)}
        while self.ground[self.ghost2['y']][self.ghost2['x']] == 4:
            self.ghost2 = {'x': random.randint(1, 18), 'y': random.randint(1, 9)}
        self.ground[self.pacman['y']][self.pacman['x']] = 2
        self.ground[self.ghost1['y']][self.ghost1['x']] = 3
        self.ground[self.ghost2['y']][self.ghost2['x']] = 3

    def initial_obstacles(self):
        self.ground[2][2] = 4
        self.ground[2][3] = 4
        self.ground[3][2] = 4
        self.ground[4][2] = 4
        self.ground[6][2] = 4
        self.ground[7][2] = 4
        self.ground[8][2] = 4
        self.ground[8][3] = 4
        self.ground[6][4] = 4
        self.ground[6][5] = 4
        self.ground[4][4] = 4
        self.ground[4][5] = 4
        self.ground[2][5] = 4
        self.ground[1][5] = 4
        self.ground[2][7] = 4
        self.ground[2][8] = 4
        self.ground[2][9] = 4
        self.ground[2][10] = 4
        self.ground[2][11] = 4
        self.ground[2][12] = 4
        self.ground[4][7] = 4
        self.ground[4][8] = 4
        self.ground[5][7] = 4
        self.ground[6][7] = 4
        self.ground[6][8] = 4
        self.ground[6][9] = 4
        self.ground[6][10] = 4
        self.ground[6][11] = 4
        self.ground[6][12] = 4
        self.ground[5][12] = 4
        self.ground[4][12] = 4
        self.ground[4][14] = 4
        self.ground[4][11] = 4
        self.ground[8][12] = 4
        self.ground[8][11] = 4
        self.ground[8][10] = 4
        self.ground[8][9] = 4
        self.ground[8][8] = 4
        self.ground[8][7] = 4
        self.ground[8][5] = 4
        self.ground[9][5] = 4
        self.ground[9][14] = 4
        self.ground[8][14] = 4
        self.ground[8][7] = 4
        self.ground[8][7] = 4
        for j in range(self.width + 1):
            self.ground[self.height + 1][j] = 4
            self.ground[0][j] = 4
        for i in range(self.height + 1):
            self.ground[i][0] = 4
            self.ground[i][self.width + 1] = 4
        self.ground[self.height + 1][self.width + 1] = 4

        self.ground[8][16] = 4
        self.ground[8][17] = 4
        self.ground[7][17] = 4
        self.ground[6][17] = 4
        self.ground[6][15] = 4
        self.ground[6][14] = 4
        self.ground[4][14] = 4
        self.ground[4][15] = 4
        self.ground[4][17] = 4
        self.ground[3][17] = 4
        self.ground[2][17] = 4
        self.ground[2][16] = 4
        self.ground[2][14] = 4
        self.ground[1][14] = 4


    def check_collision(self):
        for x in range(1, self.width):
            for y in range(1, self.height):
                if x == self.pacman['x'] and y == self.pacman['y'] and (x == self.ghost1['x'] and y == self.ghost1['y'] or x == self.ghost2['x'] and y == self.ghost2['y']):
                    return True
        return False

    def print_board(self):
        for y in range(self.height + 2):
            for x in range(self.width + 2):
                if self.ground[y][x] == 0:
                    print(" ", end=' ')
                elif self.ground[y][x] == 1:
                    print(".", end=' ')
                elif self.ground[y][x] == 2:
                    print("P", end=' ')
                elif self.ground[y][x] == 3:
                    print("G", end=' ')
                elif self.ground[y][x] == 4:
                    print("M", end=' ')
            print()
        print(f"Score: {self.score}")
        print('-' * 50)

    def initial_dots(self, ground):
        for i in range(self.height + 2):
            for j in range(self.width + 2):
                self.ground[i][j] = 1

    def update_dots(self, ground, last_x, last_y):
        ground[last_y][last_x] = 0


    def move(self, x, y, direction):
        if direction == 0:
            if y != self.height + 1 and self.ground[y + 1][x] != 4:
                return True, x, y + 1
        elif direction == 1:
            if x != self.width + 1 and self.ground[y][x + 1] != 4:
                return True, x + 1, y
        elif direction == 2:
            if y != 0 and self.ground[y - 1][x] != 4:
                return True, x, y - 1
        elif direction == 3:
            if x != 0 and self.ground[y][x - 1] != 4:
                return True, x - 1, y
        return False, x, y

    def update_score(self, score, x, y):
        if self.ground[y][x] == 1:
            score += 10
        else:
            score -= 1
        return score

    def move_pacman(self):
        x1 = self.pacman['x']
        y1 = self.pacman['y']
        self.update_dots(self.ground, x1, y1)
        start = (x1, y1)
        next_state = self.bfs(start)
        if self.get_distance(x1, y1, next_state[0], next_state[1]) == 1 and self.ground[next_state[0], next_state[1]] != 3:
            self.pacman['x'], self.pacman['y'] = next_state
        elif x1 - next_state[0] < 0 and self.ground[self.pacman['y'], self.pacman['x'] + 1] != 4 and self.ground[self.pacman['y'], self.pacman['x'] + 1] != 3:
            self.pacman['x'], self.pacman['y'] = self.pacman['x'] + 1, self.pacman['y']
        elif x1 - next_state[0] > 0 and self.ground[self.pacman['y'], self.pacman['x'] - 1] != 4 and self.ground[self.pacman['y'], self.pacman['x'] - 1] != 3:
            self.pacman['x'], self.pacman['y'] = self.pacman['x'] - 1, self.pacman['y']
        elif y1 - next_state[1] < 0 and self.ground[self.pacman['y'] + 1, self.pacman['x']] != 4 and self.ground[self.pacman['y'] + 1, self.pacman['x']] != 3:
            self.pacman['x'], self.pacman['y'] = self.pacman['x'], self.pacman['y'] + 1
        elif y1 - next_state[1] > 0 and self.ground[self.pacman['y'] - 1, self.pacman['x']] != 4 and self.ground[self.pacman['y'] - 1, self.pacman['x']] != 3:
            self.pacman['x'], self.pacman['y'] = self.pacman['x'], self.pacman['y'] - 1

        x = self.pacman['x']
        y = self.pacman['y']
        self.score = self.update_score(self.score, x, y)
        self.ground[y][x] = 2

    def get_distance(self, x_now, y_now, x, y):
        return math.sqrt((x_now - x) ** 2 + (y_now - y) ** 2)

    def bfs(self, start):
        cols, rows = len(self.ground), len(self.ground[0])
        visited = set()

        queue = deque([(start[0], start[1], 0)])  # (row, col, distance)

        while queue:
            row, col, distance = queue.popleft()

            # Check if the current position is a 1 (dot)
            if self.ground[col][row] == 1:
                return distance, 0

            # Mark the current position as visited
            visited.add((row, col))

            # Add adjacent positions to the queue if they are valid and not visited
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # delta row and delta column
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < rows and 0 <= new_col < cols and (new_row, new_col) not in visited:
                    if self.ground[new_col][new_row] == 1:
                        return new_row, new_col
                    queue.append((new_row, new_col, distance + 1))
                    visited.add((new_row, new_col))  # Mark as visited to avoid revisiting

        # If no 1 is found
        return -1, -1

    def move_ghost1(self):
        x1 = self.ghost1['x']
        y1 = self.ghost1['y']
        self.update_dots(self.ground, x1, y1)
        direction = random.randint(0, 3)
        is_changed, x, y = self.move(x1, y1, direction)
        while not is_changed:
            is_changed, x, y = self.move(x1, y1, random.randint(0, 3))
        self.ghost1['x'] = x % (self.width + 1)
        self.ghost1['y'] = y % (self.height + 1)
        x = self.ghost1['x']
        y = self.ghost1['y']
        if is_changed:
            self.ground[y][x] = 3
        else:
            self.ground[y1][x1] = 3

    def move_ghost2(self):
        x1 = self.ghost2['x']
        y1 = self.ghost2['y']
        self.update_dots(self.ground, x1, y1)
        direction = random.randint(0, 3)
        is_changed, x, y = self.move(x1, y1, direction)
        while not is_changed:
            is_changed, x, y = self.move(x1, y1, random.randint(0, 3))
        self.ghost2['x'] = x % (self.width + 1)
        self.ghost2['y'] = y % (self.height + 1)
        x = self.ghost2['x']
        y = self.ghost2['y']
        if is_changed:
            self.ground[y][x] = 3
        else:
            self.ground[y1][x1] = 3

    def play(self, num_moves):
        for _ in range(num_moves):
            self.move_pacman()
            if self.check_collision():
                raise ValueError
            self.print_board()
            time.sleep(1)  # Pause for 1 second
            self.move_ghost1()
            self.move_ghost2()
            if self.check_collision():
                raise ValueError
            self.print_board()
            time.sleep(1)  # Pause for 1 second

if __name__ == "__main__":
    pacman_game = PacmanGame()
    try:
        while True:
            pacman_game.play(5)  # Play for 5 moves
    except KeyboardInterrupt:
        print("\nGame Finished!")
        print(f"Score: {pacman_game.score}")
    except ValueError:
        print("You hit the ghost!")
        print(f"score: {pacman_game.score - 500}")
