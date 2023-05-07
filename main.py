import pygame
import sys
import Grid
import Sprite
import Button


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
        self.GRID_ROW_COLUMN = [15, 15]
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
        self.walls = []
        self.placed_maze_start_point = None
        self.placed_maze_end_point = None
        self.all_occupied_positions = []
        self.occupied_wall_positions = []
        self.maze_start_point_pos = -1
        self.maze_end_point_pos = -1

    def select_tile(self, new_active_tile):
        self.active = new_active_tile

    def wall_stuff(self):
        if self.active == "wall" and self.SIDE_MENU_WIDTH < pygame.mouse.get_pos()[0]:
            self.wall.follow()
            self.check_place()
            self.wall.draw()
        elif self.active == "wall":
            self.wall.draw()
        if len(self.walls) != 0:
            for i in self.walls:
                i.draw()

    def maze_start_point_stuff(self):
        if self.active == "maze_start_point" and self.SIDE_MENU_WIDTH < pygame.mouse.get_pos()[0]:
            self.maze_start_point.follow()
            self.check_place()
            self.maze_start_point.draw()
        elif self.active == "maze_start_point" and (self.maze_start_point.rect.left != 0 and self.maze_start_point.rect.top != 0):
            self.maze_start_point.draw()
        if self.placed_maze_start_point is not None:
            self.placed_maze_start_point.draw()

    def maze_end_point_stuff(self):
        if self.active == "maze_end_point" and self.SIDE_MENU_WIDTH < pygame.mouse.get_pos()[0]:
            self.maze_end_point.follow()
            self.check_place()
            self.maze_end_point.draw()
        elif self.active == "maze_end_point" and (self.maze_end_point.rect.left != 0 and self.maze_end_point.rect.top != 0):
            self.maze_end_point.draw()
        if self.placed_maze_end_point is not None:
            self.placed_maze_end_point.draw()

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

    def mainloop(self) -> None:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit(0)

            self.screen.fill([0, 0, 0])

            self.grid.draw()

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.walls = []
                self.placed_maze_start_point = None
                self.all_occupied_positions = []
                self.occupied_wall_positions = []
                self.maze_start_point_pos = -1
                self.maze_end_point_pos = -1
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
