import random

# Stałe
ROWS = 7
COLS = 7
START = "A"
STOP = "B"
OBSTACLE = "X"
EMPTY = " "
PLAYER = "P"

# Funkcje pomocnicze
def generate_random_position(max_rows, max_cols):
    """Generuje losową pozycję na planszy."""
    return {"row": random.randint(0, max_rows - 1), "col": random.randint(0, max_cols - 1)}

def is_adjacent(pos1, pos2):
    """Sprawdza, czy dwie pozycje są przyległe."""
    row_diff = abs(pos1["row"] - pos2["row"])
    col_diff = abs(pos1["col"] - pos2["col"])
    return row_diff + col_diff <= 1

# Funkcje gry
def generate_board(rows, cols, number_of_obstacles):
    """Generuje planszę o podanych wymiarach, z przeszkodami, START i STOP."""
    board = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    # Ustaw START i STOP
    start = generate_random_position(rows, cols)
    stop = generate_random_position(rows, cols)
    while is_adjacent(start, stop):
        stop = generate_random_position(rows, cols)

    board[start["row"]][start["col"]] = START
    board[stop["row"]][stop["col"]] = STOP

    # Dodaj przeszkody
    obstacles_placed = 0
    while obstacles_placed < number_of_obstacles:
        pos = generate_random_position(rows, cols)
        if board[pos["row"]][pos["col"]] == EMPTY:
            board[pos["row"]][pos["col"]] = OBSTACLE
            obstacles_placed += 1

    return board, start, stop

def move_player(board, player, direction):
    """Przesuwa gracza w zadanym kierunku, jeśli ruch jest możliwy."""
    new_position = player.copy()
    if direction == "up":
        new_position["row"] -= 1
    elif direction == "down":
        new_position["row"] += 1
    elif direction == "left":
        new_position["col"] -= 1
    elif direction == "right":
        new_position["col"] += 1
    else:
        return player  # Nieznany kierunek, brak ruchu

    # Sprawdź, czy ruch jest w granicach i nie prowadzi na przeszkodę
    if (
        0 <= new_position["row"] < len(board)
        and 0 <= new_position["col"] < len(board[0])
        and board[new_position["row"]][new_position["col"]] != OBSTACLE
    ):
        board[player["row"]][player["col"]] = EMPTY
        board[new_position["row"]][new_position["col"]] = PLAYER
        return new_position
    return player

def is_game_over(player, stop):
    """Sprawdza, czy gracz dotarł do celu."""
    return player["row"] == stop["row"] and player["col"] == stop["col"]

def spawn_player(board, player):
    """Umieszcza gracza na planszy."""
    board[player["row"]][player["col"]] = PLAYER

def find_path(board, start, stop):
    """Znajduje ścieżkę z START do STOP przy użyciu algorytmu BFS."""
    from collections import deque

    rows, cols = len(board), len(board[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start, [])])  # Kolejka przechowuje (pozycja, ścieżka)

    directions = [
        (-1, 0),  # Góra
        (1, 0),   # Dół
        (0, -1),  # Lewo
        (0, 1),   # Prawo
    ]

    while queue:
        current, path = queue.popleft()
        row, col = current["row"], current["col"]

        if visited[row][col]:
            continue
        visited[row][col] = True

        # Jeśli osiągnęliśmy STOP, zwracamy ścieżkę
        if row == stop["row"] and col == stop["col"]:
            return path + [stop]

        # Przeglądaj sąsiadów
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < rows
                and 0 <= new_col < cols
                and not visited[new_row][new_col]
                and board[new_row][new_col] != OBSTACLE
            ):
                queue.append(({"row": new_row, "col": new_col}, path + [{"row": row, "col": col}]))

    return []  # Brak ścieżki

if __name__ == "__main__":
    # Przykładowa demonstracja
    board, start, stop = generate_board(ROWS, COLS, 10)
    player = start
    spawn_player(board, player)

    for row in board:
        print(" ".join(row))
    print("START:", start, "STOP:", stop)
