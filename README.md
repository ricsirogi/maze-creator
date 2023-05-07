# maze-creator

I guess this will be an app where you can create a maze, and you will have a thing that solves it for you, or you can control a character to try to solve it yourself (but since you made the maze it will be easy for you)

How to use:
after running the app you are greeted with 3 buttons and a grid.
you can place walls, start and end points with LEFT CLICK (you can hold it down as well)
you can remove placed tiles with RIGHT CLICK (you can hold it down as well
you can clear the whole grid with SPACE
there are 10 save slots for each maze size (row_column)
by pressing the numbers 0-9 you can select the active save slot (if you are pressing a number and it isn't printing that it's selected, then it's already selected)
there are 3 modes: print (default), save and load
I think they are pretty self explaning:
print-mode prints the maze_state to the console,
save-mode saves the current maze to the currently selected maze-number
load-mode loads the maze at the currently selected maze-number (if there is one)

todo:

- make select and drop system, so I can place down walls for the maze DONE
- make a "tile type selector" next to the grid, so I can choose between wall and starting point (to place down) DONE
- make a system to save mazes DONE
- make a player
- make a simple player controller system
  - winning
  - switching between editing and playing
  - move counter (?)
- make a bot that solves the maze :)
