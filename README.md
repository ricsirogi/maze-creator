# maze-creator

I guess this will be an app where you can create a maze, and you will have a thing that solves it for you, or you can control a character to try to solve it yourself (but since you made the maze it will be easy for you)

How to use:

SAVING/LOADING
there are 10 save slots for each maze size (row_column)
by pressing the numbers 0-9 you can select the active save slot (if you are pressing a number and it isn't printing that it's selected, then it's already selected)
there are 3 ENTER-modes: print (default), save and load
ENTER-modes determine what happens when you press ENTER
I think they are pretty self-explanatory:
print-mode prints the maze_state to the console (press 'd' to select this mode)
save-mode saves the current maze to the currently selected maze-number (press 's' to select this mode)
load-mode loads the maze at the currently selected maze-number (if there is one) (press 'l' to select this mode)

SWITCHING BETWEEN EDITING AND PLAYING
there are 2 modes: edit (default) and play:
in edit mode you can edit the maze (press 'e' to select this mode)
in play mode you can control a player (that spawns at the maze's start point) inside the maze (press 'p' to select this mode)

PLAY MODE
move with the arrow keys
by pressing space twice you can reset back to the start poing

EDIT MODE
after running the app you are greeted with 3 buttons and a grid.
you can place walls, start and end points with LEFT CLICK (you can hold it down as well)
you can remove placed tiles with RIGHT CLICK (you can hold it down as well
you can clear the whole grid by double tapping SPACE

AUTOPLAY
there is also autoplay which you can toggle with 'a'
the autoplay is kinda bad, sometimes it just gets stuck but it can solve the maze like 80% of the time i guess

If you want to generate a maze, the easiest way is to

1. create one using https://www.dcode.fr/maze-generator (if you want a maze thats 14x14 tiles set it to 7x7 cuz reasons) (not my website)
   1.5) make sure that the walls are represented with "w" and the path is represented with "0"
   1.55) sometimes it leaves out some walls at the end, just write them in
   1.555) count how many lines it has, and thats what will be the size of the map (14 lines = 14x14 map)
2. paste it into a text editing program (preferably vscode)
3. with ctrl + h replace all '0's and 'w's to have a quote mark before and after and a comma after
4. put each line into square brackets (I recommend holding down alt and clicking at the end of each line in vscode and then you just have to do it once)
5. put a comma at the end of each line
6. modify self.GRID_ROW_COLUMN so it's your desired map size
7. start the game and then go into save mode and press enter
8. in mazes.json search for your desired map size and under that there will be a dictionary, and there in the "0" key will be a list with a bunch of 0s.
9. delete this list entirely so only the curly brackets remain
10. paste in the list that you made before between the curly brackets
11. start the game press 'l' and then enter and the map should appear, if not check if you did any mistakes, or read into the saving/loading section

todo:

- make select and drop system, so I can place down walls for the maze DONE
- make a "tile type selector" next to the grid, so I can choose between wall and starting point (to place down) DONE
- make a system to save mazes DONE
- make a player DONE
- make a simple player controller system DONE
  - winning What IS winning?
  - switching between editing and playing DONE
- make a bot that solves the maze :) Doneish (it DOES solve the maze, but not in the most optimal way, idk if I wanna continue this mess tho)
