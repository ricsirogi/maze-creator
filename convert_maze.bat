@echo off

set /p INPUT=Make sure that only the bare maze is inside maze_to_convert (type q to quit) 
IF "%INPUT%"=="q" (
    echo Quitting...
    pause
) ELSE (
    echo Converting...
    py convert_maze.py
    echo Check maze_to_convert.txt!
    pause
)