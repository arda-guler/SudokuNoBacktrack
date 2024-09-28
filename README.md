# No-Backtrack Sudoku Solver

Code nomenclature:

**Cell** is a single number

**Box** is a 3x3 region

**Board** is the entire 9x9 game area


This solver not only checks rows, columns and boxes, but also checks the possible fillers in horizontally and vertically 
neighboring boxes among themselves as to further narrow-down which rows and columns in which boxes can have which possible 
fillers dictated by the possible fillers in neighboring boxes.

This is probably as far as I can go, without any trial-and-error involved.

As it uses cold-hard logic, it is more sequential and human-like. If it can't solve an extremely difficult sudoku, it will
also print out what cells can have what potential numbers.

![solver2](https://github.com/user-attachments/assets/25938d92-77f5-4551-aaf7-2523728c83be)

## Why no backtracking, though?
Because I came up with this algorithm while playing sudoku on public transport. Sorry, backtracking isn't fun when you do it manually.
