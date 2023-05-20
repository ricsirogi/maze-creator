import sys
import json

maze_to_convert = ""
maze_to_convert_file = "maze_to_convert.txt"

with open(maze_to_convert_file, "r") as bare_maze:
    maze_to_convert = bare_maze.read()
    if maze_to_convert == "":
        print(maze_to_convert_file, "is empty!")
        sys.exit(0)

converted_maze = ""
converted_maze = [[]]

skip = False
size_counter = 0
line = 0
for c, i in enumerate(maze_to_convert):
    if i == "\n":
        if c == len(maze_to_convert) - 1:
            break
        line += 1
        converted_maze.append([])
    elif i == "0":
        converted_maze[line].append("0")
    elif i == "w":
        converted_maze[line].append("w")
    else:
        print("Invalid character in", maze_to_convert_file)
        with open(maze_to_convert_file, "r") as txt:
            temp = txt.read()
        with open(maze_to_convert_file, "w") as txt:
            txt.write(temp + "\nInvalid character in " + maze_to_convert_file)
        sys.exit(0)

print(converted_maze)
converted_maze[0][0] = "w"
converted_maze[0][1] = "w"
converted_maze[1][0] = "w"
converted_maze[len(converted_maze) - 2].append("w")
converted_maze[len(converted_maze) - 1][len(converted_maze) - 2] = "w"
converted_maze[len(converted_maze) - 1].append("w")
converted_maze[1][1] = "s"
converted_maze[len(converted_maze) - 2][len(converted_maze) - 2] = "e"

map_size = f"{len(converted_maze)}x{len(converted_maze)}"

with open("mazes.json", "r") as f:
    data = json.load(f)

if data.get(map_size) is None:
    data[map_size] = {}

maze_number = -1
for i in range(9):
    if data[map_size].get(str(i)) is None:
        data[map_size][i] = converted_maze
        maze_number = i
        break

with open("mazes.json", "w") as f:
    json.dump(data, f)

if maze_number > -1:
    save_text = "Maze succesfully saved in mazes.json at maze_number " + str(maze_number)
else:
    save_text = "Maze was not able to be saved because all save slots are in use in that size"

with open(maze_to_convert_file, "w") as new_maze:
    for i in converted_maze:
        new_maze.writelines(str(i))
        new_maze.writelines("\n")
    new_maze.writelines(f"\nSet the size to: {map_size}\n")
    new_maze.writelines(save_text)
