def read_maze_file(input_file):
    """Reads the maze data from a file."""
    maze_data = []
    with open(input_file, 'r') as file:
        for line in file:
            maze_data.append(tuple(map(int, line.strip().split())))
    return maze_data


def write_maze_file(output_file, maze):
    """Writes the ASCII maze to a file."""
    with open(output_file, 'w') as file:
        for row in maze:
            file.write(row + '\n')


def generate_ascii_maze(maze_data, size=16):
    """
    Generates an ASCII maze from the input data.
    Each cell is 5 spaces wide and 3 spaces tall.
    Walls and corners are properly connected.
    """
    # Initialize ASCII maze grid
    w = size * 4
    h = size * 2
    ascii_maze = [[" " for _ in range(size * 4 + 1)]
                  for _ in range(size * 2 + 1)]

    # Iterate through maze data to construct walls
    for x, y, north, east, south, west in maze_data:
        ascii_x, ascii_y = x * 4, y * 2  # Map (x, y) to ASCII coordinates

        # Draw the north wall
        if north:
            for j in range(1, 4):
                ascii_maze[h - ascii_y - 2][ascii_x + j] = "-"

        # Draw the south wall
        if south:
            for j in range(1, 4):
                ascii_maze[h - ascii_y][ascii_x + j] = "-"

        # Draw the west wall
        if west:
            ascii_maze[h - ascii_y - 1][ascii_x] = "|"

        # Draw the east wall
        if east:
            ascii_maze[h - ascii_y - 1][ascii_x + 4] = "|"

        # Draw corners if necessary
        if north or west:  # Top-left corner
            ascii_maze[h - ascii_y][ascii_x] = "+"
        if north or east:  # Top-right corner
            ascii_maze[h - ascii_y][ascii_x + 4] = "+"
        if south or west:  # Bottom-left corner
            ascii_maze[h - ascii_y - 2][ascii_x] = "+"
        if south or east:  # Bottom-right corner
            ascii_maze[h - ascii_y - 2][ascii_x + 4] = "+"

    # Convert the 2D list to a list of strings
    ascii_maze_strings = ["".join(row) for row in ascii_maze]
    return ascii_maze_strings


def main():
    input_file = "/home/lulu/Desktop/edunex/edunex_micromouse/archive/BFS_FloodFill-Maze1.txt"
    output_file = "BFS_FloodFill_Maze1.txt"

    # Read maze data from file
    maze_data = read_maze_file(input_file)

    # Generate ASCII maze
    ascii_maze = generate_ascii_maze(maze_data)

    # Write ASCII maze to file
    write_maze_file(output_file, ascii_maze)
    print(f"Maze written to {output_file}")


if __name__ == "__main__":
    main()
