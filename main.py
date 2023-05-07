import pygame
import sys
import Grid
import Sprite
import Button
import json


class Main():
    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()

        self.SIDE_MENU_WIDTH = 400

        self.BUTTON_ACOLOR = (100, 100, 255)
        self.BUTTON_IACOLOR = (0, 0, 255)
        self.BUTTON_TEXT_COLOR = (0, 0, 0)
        self.BUTTON_TEXT_SIZE = 40

        self.WALL_BUTTON_SIZE = (120, 60)
        self.WALL_BUTTON_TEXT = "WALLS"
        self.WALL_BUTTON_POS = (50, 50)

        self.MAZE_START_POINT_BUTTON_SIZE = (320, 60)
        self.MAZE_START_POINT_BUTTON_TEXT = "MAZE START POINT"
        self.MAZE_START_POINT_BUTTON_POS = (
            50, self.WALL_BUTTON_POS[1] + self.MAZE_START_POINT_BUTTON_SIZE[1] + 50)

        self.MAZE_END_POINT_BUTTON_SIZE = (290, 60)
        self.MAZE_END_POINT_BUTTON_TEXT = "MAZE END POINT"
        self.MAZE_END_POINT_BUTTON_POS = (
            50, self.MAZE_START_POINT_BUTTON_POS[1] + self.MAZE_START_POINT_BUTTON_SIZE[1] + 50)

        self.GRID_POS = (self.SIDE_MENU_WIDTH, 0)
        self.GRID_ROW_COLUMN = [18, 18]
        self.GRID_CELL_SIZE = (50, 50)
        self.GRID_CELL_COLOR = (100, 100, 100)
        self.GRID_BORDER_COLOR = (255, 255, 255)
        self.GRID_BORDER_SIZE = 1

        self.WALL_COLOR = (200, 200, 200)
        self.MAZE_START_POINT_COLOR = (255, 0, 0)
        self.MAZE_END_POINT_COLOR = (0, 255, 0)

        size_x = self.GRID_ROW_COLUMN[0] * (self.GRID_CELL_SIZE[0] +
                                            self.GRID_BORDER_SIZE) + self.GRID_BORDER_SIZE + self.SIDE_MENU_WIDTH
        size_y = self.GRID_ROW_COLUMN[1] * (self.GRID_CELL_SIZE[1] +
                                            self.GRID_BORDER_SIZE) + self.GRID_BORDER_SIZE
        self.SIZE = (size_x, size_y)
        self.screen = pygame.display.set_mode(self.SIZE)

        self.grid = Grid.Grid(self.GRID_POS, self.GRID_ROW_COLUMN, self.GRID_CELL_SIZE,
                              self.GRID_CELL_COLOR, self.GRID_BORDER_COLOR, self.GRID_BORDER_SIZE, self.screen)

        self.wall = Sprite.Sprite(
            self.GRID_CELL_SIZE, self.WALL_COLOR, self.screen)

        self.maze_start_point = Sprite.Sprite(
            self.GRID_CELL_SIZE, self.MAZE_START_POINT_COLOR, self.screen)

        self.maze_end_point = Sprite.Sprite(
            self.GRID_CELL_SIZE, self.MAZE_END_POINT_COLOR, self.screen)

        self.maze_start_point_button = Button.Button(self.MAZE_START_POINT_BUTTON_TEXT, self.MAZE_START_POINT_BUTTON_POS, self.MAZE_START_POINT_BUTTON_SIZE,
                                                     self.BUTTON_ACOLOR, self.BUTTON_IACOLOR, self.BUTTON_TEXT_COLOR, lambda: self.select_tile("maze_start_point"), self.screen, self.BUTTON_TEXT_SIZE)

        self.maze_end_point_button = Button.Button(self.MAZE_END_POINT_BUTTON_TEXT, self.MAZE_END_POINT_BUTTON_POS, self.MAZE_END_POINT_BUTTON_SIZE,
                                                   self.BUTTON_ACOLOR, self.BUTTON_IACOLOR, self.BUTTON_TEXT_COLOR, lambda: self.select_tile("maze_end_point"), self.screen, self.BUTTON_TEXT_SIZE)

        self.wall_button = Button.Button(self.WALL_BUTTON_TEXT, self.WALL_BUTTON_POS, self.WALL_BUTTON_SIZE,
                                         self.BUTTON_ACOLOR, self.BUTTON_IACOLOR, self.BUTTON_TEXT_COLOR, lambda: self.select_tile("wall"), self.screen, self.BUTTON_TEXT_SIZE)

        self.buttons = [self.maze_start_point_button,
                        self.maze_end_point_button, self.wall_button]
        self.active = "wall"
        self.m1_clicked = False
        self.m2_clicked = False
        self.enter_pressed = False
        self.walls = []
        self.placed_maze_start_point = None
        self.placed_maze_end_point = None
        self.all_occupied_positions = []
        self.occupied_wall_positions = []
        self.maze_start_point_pos = -1
        self.maze_end_point_pos = -1
        self.NUMBER_ID_0_TO_9 = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
        self.map_size = f"{str(self.GRID_ROW_COLUMN[0])}x{str(self.GRID_ROW_COLUMN[1])}"
        self.maze_state = []
        self.mode = "print"
        self.maze_number = 0

    def select_tile(self, new_active_tile):
        self.active = new_active_tile

    def wall_stuff(self):
        if self.active == "wall" and self.check_if_cursor_in_window():
            self.wall.follow()
            self.check_place()
            self.wall.draw()
        elif self.active == "wall":
            self.wall.draw()
        if len(self.walls) != 0:
            for i in self.walls:
                i.draw()

    def maze_start_point_stuff(self):
        if self.active == "maze_start_point" and self.check_if_cursor_in_window():
            self.maze_start_point.follow()
            self.check_place()
            self.maze_start_point.draw()
        elif self.active == "maze_start_point" and (self.maze_start_point.rect.left != 0 and self.maze_start_point.rect.top != 0):
            self.maze_start_point.draw()
        if self.placed_maze_start_point is not None:
            self.placed_maze_start_point.draw()

    def maze_end_point_stuff(self):
        if self.active == "maze_end_point" and self.check_if_cursor_in_window():
            self.maze_end_point.follow()
            self.check_place()
            self.maze_end_point.draw()
        elif self.active == "maze_end_point" and (self.maze_end_point.rect.left != 0 and self.maze_end_point.rect.top != 0):
            self.maze_end_point.draw()
        if self.placed_maze_end_point is not None:
            self.placed_maze_end_point.draw()

    def check_if_cursor_in_window(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.SIDE_MENU_WIDTH < mouse_pos[0] < self.screen.get_width() and 0 < mouse_pos[1] < self.screen.get_height()

    def button_stuff(self):
        for i in self.buttons:
            i.get_mouse()
            i.draw()

    def check_place(self):
        """
        checks if a mouse button is pressed, if m1 is pressed it tries to place down the currently active tile
        and if m2 is pressed then it removes the tile that is currently being hovered over.
        """
        mouse_press = pygame.mouse.get_pressed()
        placement_pos = "undefined"
        if mouse_press[0]:
            placed_a_new_tile = False
            if self.active == "wall":
                placement_pos = self.grid.find_closest_cell(
                    (self.wall.rect.left, self.wall.rect.top))
                if placement_pos not in self.all_occupied_positions:
                    new_wall = Sprite.Sprite(
                        self.GRID_CELL_SIZE, self.WALL_COLOR, self.screen, placement_pos)
                    self.walls.append(new_wall)
                    self.occupied_wall_positions.append(placement_pos)
                    placed_a_new_tile = True

            elif self.active == "maze_start_point":
                placement_pos = self.grid.find_closest_cell(
                    (self.maze_start_point.rect.left, self.maze_start_point.rect.top))
                if placement_pos not in self.all_occupied_positions:
                    self.placed_maze_start_point = Sprite.Sprite(
                        self.GRID_CELL_SIZE, self.MAZE_START_POINT_COLOR, self.screen, placement_pos)
                    if self.maze_start_point_pos in self.all_occupied_positions:
                        self.all_occupied_positions.remove(
                            self.maze_start_point_pos)
                    self.maze_start_point_pos = placement_pos
                    placed_a_new_tile = True

            elif self.active == "maze_end_point":
                placement_pos = self.grid.find_closest_cell(
                    (self.maze_end_point.rect.left, self.maze_end_point.rect.top))
                if placement_pos not in self.all_occupied_positions:
                    self.placed_maze_end_point = Sprite.Sprite(
                        self.GRID_CELL_SIZE, self.MAZE_END_POINT_COLOR, self.screen, placement_pos)
                    if self.maze_end_point_pos in self.all_occupied_positions:
                        self.all_occupied_positions.remove(
                            self.maze_end_point_pos)
                    self.maze_end_point_pos = placement_pos
                    placed_a_new_tile = True

            if placed_a_new_tile and placement_pos != "undefined":
                self.all_occupied_positions.append(placement_pos)

        elif mouse_press[2]:
            remove_pos = self.grid.find_closest_cell(
                (pygame.mouse.get_pos()[0] - int(self.GRID_CELL_SIZE[0] / 2), pygame.mouse.get_pos()[1] - int(self.GRID_CELL_SIZE[1] / 2)))
            if remove_pos in self.all_occupied_positions:
                if remove_pos == self.maze_start_point_pos:
                    self.placed_maze_start_point = None
                    self.maze_start_point_pos = -1
                elif remove_pos == self.maze_end_point_pos:
                    self.placed_maze_end_point = None
                    self.maze_end_point_pos = -1
                for wall in self.walls:
                    if (wall.rect.left, wall.rect.top) == remove_pos:
                        self.walls.remove(wall)
                        self.occupied_wall_positions.remove(remove_pos)
                self.all_occupied_positions.remove(remove_pos)

    def save_maze_state(self):
        with open("mazes.json", "r") as f:
            data = json.load(f)
        try:
            data[self.map_size][str(
                self.maze_number)] = self.maze_state
        except KeyError:
            data[self.map_size] = {}
            data[self.map_size][str(
                self.maze_number)] = self.maze_state
        with open("mazes.json", "w") as f:
            json.dump(data, f)

    def load_maze_state(self):
        self.clear_all()
        with open("mazes.json", "r") as f:
            data = json.load(f)
        allpos = self.grid.all_positions
        for y_count, y in enumerate(data[self.map_size][str(self.maze_number)]):
            for x_count, x in enumerate(y):
                placement_pos = allpos[y_count][x_count]
                if x == "w":
                    new_wall = Sprite.Sprite(
                        self.GRID_CELL_SIZE, self.WALL_COLOR, self.screen, placement_pos)
                    self.walls.append(new_wall)
                    self.occupied_wall_positions.append(
                        placement_pos)

                elif x == "s":
                    self.placed_maze_start_point = Sprite.Sprite(
                        self.GRID_CELL_SIZE, self.MAZE_START_POINT_COLOR, self.screen, placement_pos)
                    self.maze_start_point_pos = placement_pos

                elif x == "e":
                    self.placed_maze_end_point = Sprite.Sprite(
                        self.GRID_CELL_SIZE, self.MAZE_END_POINT_COLOR, self.screen, placement_pos)
                    self.maze_end_point_pos = placement_pos
                self.all_occupied_positions.append(
                    placement_pos)

    def update_maze_state(self):
        self.maze_state = []
        for y_count, y in enumerate(self.grid.all_positions):
            self.maze_state.append([])
            for x in y:
                if x in self.occupied_wall_positions:
                    self.maze_state[y_count].append("w")
                elif x == self.maze_start_point_pos:
                    self.maze_state[y_count].append("s")
                elif x == self.maze_end_point_pos:
                    self.maze_state[y_count].append("e")
                else:
                    self.maze_state[y_count].append("0")

    def clear_all(self):
        self.walls = []
        self.placed_maze_start_point = None
        self.placed_maze_end_point = None
        self.all_occupied_positions = []
        self.occupied_wall_positions = []
        self.maze_start_point_pos = -1
        self.maze_end_point_pos = -1

    def mainloop(self) -> None:
        while True:
            events = pygame.event.get()
            key_pressed = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)

            self.screen.fill([0, 0, 0])

            self.grid.draw()

            if key_pressed[pygame.K_SPACE]:
                self.clear_all()

            if key_pressed[pygame.K_RETURN]:
                if not self.enter_pressed:
                    self.update_maze_state()

                    if self.mode == "print":
                        print("\n\n\n")
                        for i in self.maze_state:
                            print(i)

                    elif self.mode == "save":
                        print("Saving maze to maze number", self.maze_number)
                        self.save_maze_state()
                        print("Save succesful!")

                    elif self.mode == "load":
                        try:
                            print("Loading maze", self.maze_number)
                            self.load_maze_state()
                            print("Load succesful!")
                        except KeyError:
                            print("No maze saved at that number")

                    self.enter_pressed = True
            else:
                self.enter_pressed = False

            for count, number in enumerate(self.NUMBER_ID_0_TO_9):
                if key_pressed[number]:
                    if self.maze_number != count:
                        self.maze_number = count
                        print("Currently selected maze_number:", count)

            if key_pressed[pygame.K_l]:
                if self.mode != "load":
                    self.mode = "load"
                    print("Current mode: load")
            if key_pressed[pygame.K_s]:
                if self.mode != "save":
                    self.mode = "save"
                    print("Current mode: save")
            if key_pressed[pygame.K_p]:
                if self.mode != "print":
                    self.mode = "print"
                    print("Current mode: print")

            if self.active == "wall":
                self.maze_end_point_stuff()
                self.maze_start_point_stuff()
                self.wall_stuff()
            elif self.active == "maze_start_point":
                self.maze_end_point_stuff()
                self.wall_stuff()
                self.maze_start_point_stuff()
            elif self.active == "maze_end_point":
                self.maze_start_point_stuff()
                self.wall_stuff()
                self.maze_end_point_stuff()
            self.button_stuff()

            pygame.display.flip()
            self.clock.tick(75)


if __name__ == "__main__":
    app = Main()
    app.mainloop()
