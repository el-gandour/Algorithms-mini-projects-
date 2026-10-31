from collections import deque
import numpy as np

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def parse_grid(text):
    """Milestone 1: read a grid like '11000' per line into a numpy array.
    Spaces between digits are allowed ('1 1 0 0 0')."""
    rows = []
    for line in text.strip().splitlines():
        digits = line.replace(" ", "").strip()
        if digits:
            if set(digits) - {"0", "1"}:
                raise ValueError(f"Grid may only contain 0 and 1, got: {line!r}")
            rows.append([int(ch) for ch in digits])
    if not rows:
        raise ValueError("Grid is empty.")
    if len({len(r) for r in rows}) != 1:
        raise ValueError("All rows must have the same length.")
    return np.array(rows, dtype=int)


def flood_fill(grid, visited, start_r, start_c):
    """Milestone 3: mark every land cell reachable from (start_r, start_c).
    Returns the size of that island."""
    rows, cols = grid.shape
    queue = deque([(start_r, start_c)])
    visited[start_r, start_c] = True
    size = 0

    while queue:
        r, c = queue.popleft()
        size += 1
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr, nc] == 1 and not visited[nr, nc]):
                visited[nr, nc] = True
                queue.append((nr, nc))
    return size


def count_islands(grid):
    visited = np.zeros_like(grid, dtype=bool)
    sizes = []

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 1 and not visited[r, c]:
                sizes.append(flood_fill(grid, visited, r, c))

    return len(sizes), sizes


def report(title, text):
    grid = parse_grid(text)
    count, sizes = count_islands(grid)
    print(f"\n== {title} ==")
    for row in grid:
        print("  " + " ".join(str(v) for v in row))
    print(f"Result: {count} island{'s' if count != 1 else ''}")
    if sizes:
        print(f"Island sizes: {sizes}")
        print(f"Largest island: {max(sizes)} cell{'s' if max(sizes) != 1 else ''}")


if __name__ == "__main__":
    report("Example from the brief", """
        11000
        11000
        00100
        00011
    """)

    report("No land", """
        000
        000
    """)

    report("One big island", """
        111
        111
    """)

    report("Diagonals are separate", """
        100
        010
        001
    """)

    print("\nTry your own grid! Enter rows of 0/1 (blank line to finish):")
    lines = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    if lines:
        try:
            report("Your grid", "\n".join(lines))
        except ValueError as e:
            print("Error:", e)