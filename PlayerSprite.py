import pygame
import time
import random
import math


class Sprite(object):
    def __init__(self, size: tuple[int, int], color: tuple[int, int, int], screen: pygame.surface.Surface, unit: tuple[int, int]):
        self.rect = pygame.rect.Rect((0, 0), size)
        self.screen = screen
        self.color = color
        self.size = size
        self.unit = unit
        self.following = True
        self.dead_ends = []
        self.visited_positions = []  # all of the visited locations
        self.last_visited_positions = []  # only the last x visited locations
        self.MAX_LAST_VISITED_POSITIONS = 50
        self.useful_positons = []
        self.tries = 0
        self.max_tries = 5
        self.deadlock = 0
        self.max_deadlock = 3
        self.wall_positions = []
        self.start_position = ()
        self.end_position = ()
        self.DIRECTIONS = ["u", "r", "d", "l"]
        self.in_dead_end_hallway = False
        self.try_number = 0
        self.moves = 0

        # I wanted to make it so it sometimes moves randomly so it would may be able to find
        # new paths because the original algorithm doesn't find the closest path
        # but it won't work because of the way I do like all of this and this
        # auto solving algorithm thing quickly made me burn out
        self.RANDOM_MOVE_CHANCE = 0

    def move(self, auto_mode: bool = False):
        new_pos = (self.rect.left, self.rect.top)
        original = (self.rect.left, self.rect.top)

        if not auto_mode:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:
                new_pos = (self.rect.left, self.rect.top - self.unit[1])
            elif keys_pressed[pygame.K_RIGHT]:
                new_pos = (self.rect.left + self.unit[0], self.rect.top)
            elif keys_pressed[pygame.K_DOWN]:
                new_pos = (self.rect.left, self.rect.top + self.unit[1])
            elif keys_pressed[pygame.K_LEFT]:
                new_pos = (self.rect.left - self.unit[0], self.rect.top)
            else:
                return
            if new_pos != original and new_pos not in self.wall_positions:
                self.move_to(new_pos)

        else:
            moved = False

            # Check if I'm in a dead end or a dead end hallway
            self.check_for_dead_end()

            # Get all locations that I can move to
            possible_new_positions = self.get_possible_new_positions()

            if len(possible_new_positions) == 1:
                print("only", possible_new_positions[0], self.moves)
                self.move_to(possible_new_positions[0])
                return

            if self.try_number != 0 and len(possible_new_positions) > 1:
                if random.random() < self.RANDOM_MOVE_CHANCE:
                    if not (len(possible_new_positions) == 2 and (possible_new_positions[0][0] == possible_new_positions[1][0] or possible_new_positions[0][1] == possible_new_positions[1][1])):
                        print("random", possible_new_positions, self.moves)
                        rannum = random.randint(0, len(possible_new_positions) - 1)
                        if possible_new_positions[rannum] == self.last_visited_positions[len(self.last_visited_positions) - 2]:
                            temp = rannum
                            while temp == rannum:
                                rannum = random.randint(0, len(possible_new_positions) - 1)
                        self.move_to(possible_new_positions[rannum])
                        return

            # Try to move to the tile that is closest to the end point,
            # but if that tile is a tile that I've already visited,
            # then try the second closest and then the third and then the fourth
            for currently_checked_position in possible_new_positions:

                # If this is not the first try at this maze, then only step on tiles that were stepped on
                # during the previous attempt
                if self.try_number != 0 and currently_checked_position not in self.useful_positons:
                    continue

                if currently_checked_position not in self.dead_ends and currently_checked_position not in self.last_visited_positions:
                    print("ideal", currently_checked_position, self.moves)
                    self.move_to(currently_checked_position)
                    moved = True
                    break

            if not moved:
                for currently_checked_position in possible_new_positions:
                    if currently_checked_position not in self.dead_ends and currently_checked_position != self.last_visited_positions[len(self.last_visited_positions) - 2]:
                        print("at last", currently_checked_position, self.moves)
                        self.move_to(currently_checked_position)
                        moved = True
                        break

            if not moved:
                for currently_checked_position in possible_new_positions:
                    if currently_checked_position not in self.dead_ends:
                        print("at laster", currently_checked_position, self.moves)
                        self.move_to(currently_checked_position)
                        moved = True
                        break

            if not moved:
                for currently_checked_position in possible_new_positions:
                    if currently_checked_position not in self.last_visited_positions:
                        print("at leastest", currently_checked_position, self.moves)
                        self.move_to(currently_checked_position)
                        moved = True
                        break

            if not moved:
                how_much_time_since_visiting_position = self.MAX_LAST_VISITED_POSITIONS
                print("finally")
                got_a_position = False
                for c, i in enumerate(possible_new_positions):
                    if i in self.last_visited_positions:
                        if self.last_visited_positions.index(i) < how_much_time_since_visiting_position:
                            how_much_time_since_visiting_position = self.last_visited_positions.index(i)
                            got_a_position = True
                if got_a_position:
                    self.move_to(self.last_visited_positions[how_much_time_since_visiting_position])

    def move_to(self, new_pos):
        self.moves += 1
        self.visited_positions.append(new_pos)

        # keep track of the last 5 locations that I've stepped in
        if len(self.last_visited_positions) > self.MAX_LAST_VISITED_POSITIONS:
            self.last_visited_positions.pop(0)
        self.last_visited_positions.append(new_pos)

        self.rect.left = new_pos[0]
        self.rect.top = new_pos[1]

    def get_possible_new_positions(self):
        possible_positions = []
        new_positions = []
        distances_from_end_point = []
        to_remove = []

        possible_positions.append((self.rect.left, self.rect.top - self.unit[1]))
        possible_positions.append((self.rect.left + self.unit[0], self.rect.top))
        possible_positions.append((self.rect.left, self.rect.top + self.unit[1]))
        possible_positions.append((self.rect.left - self.unit[0], self.rect.top))

        print("\n")

        for i in range(4):
            if possible_positions[i] in self.wall_positions:
                to_remove.append(possible_positions[i])
            else:
                distances_from_end_point.append(
                    self.distance_between_two_points(possible_positions[i], self.end_position))

        for i in to_remove:
            possible_positions.pop(possible_positions.index(i))
        to_remove = []

        for i in range(len(distances_from_end_point) - 1):
            smallest_so_far = (9999, -1)
            for c, j in enumerate(distances_from_end_point):
                if j < smallest_so_far[0]:
                    smallest_so_far = (j, c)
            new_positions.append(possible_positions[smallest_so_far[1]])
            distances_from_end_point.pop(smallest_so_far[1])
            possible_positions.pop(smallest_so_far[1])

        new_positions.append(possible_positions[0])

        print(new_positions)
        return new_positions

    def distance_between_two_points(self, point_1, point_2) -> float:
        a = abs(point_1[0] - point_2[0])
        b = abs(point_1[1] - point_2[1])

        return math.sqrt(a**2 + b**2)

    def check_for_dead_end(self):
        """
        checks if the player is in the dead end
        if yes, add the current pos to a list
        also adds the hallway leading to the dead end
        """

        surrounding_walls = 0
        current_pos = (self.rect.left, self.rect.top)
        if (self.rect.left, self.rect.top - self.unit[1]) in self.wall_positions:
            surrounding_walls += 1
        if (self.rect.left + self.unit[0], self.rect.top) in self.wall_positions:
            surrounding_walls += 1
        if (self.rect.left, self.rect.top + self.unit[1]) in self.wall_positions:
            surrounding_walls += 1
        if (self.rect.left - self.unit[0], self.rect.top) in self.wall_positions:
            surrounding_walls += 1

        if current_pos not in self.dead_ends:
            if surrounding_walls == 3:
                self.dead_ends.append(current_pos)
                self.in_dead_end_hallway = True
            elif self.in_dead_end_hallway:
                if surrounding_walls == 2:
                    self.dead_ends.append(current_pos)
                else:
                    self.in_dead_end_hallway = False

    def retry(self):

        self.useful_positons = self.visited_positions
        self.visited_positions = []
        self.rect.left = self.start_position[0]  # type: ignore
        self.rect.top = self.start_position[1]  # type: ignore
        self.try_number += 1
        self.moves = 0

    def reset_values(self):
        self.dead_ends = []
        self.visited_positions = []
        self.useful_positons = []
        self.tries = 0
        self.try_number = 0
        self.max_tries = 10
        self.deadlock = 0
        self.max_deadlock = 3
        self.wall_positions = []
        self.end_position = ()
        self.moves = 0

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
