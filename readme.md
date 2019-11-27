# minesweeper
Minesweeper game on pygame

This is an implementation of the classic logical sapper game.
The goal of the game is to open the entire field without being blown up by a mine.
If mines are present in neighboring cells, the number in the cell indicates the number of mines around it.
Control Keys:
• transition through cells is carried out by arrows on the keyboard;
• a space opens the cell if it is not flagged;
• using the F key sets or removes the flag from the cell;
Also added autosave of the current game when closing.
The next time the game starts, it automatically loads the save.
