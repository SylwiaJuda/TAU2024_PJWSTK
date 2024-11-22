import unittest
from game_logic import generate_board, move_player, is_game_over, spawn_player, find_path
from game_logic import EMPTY, OBSTACLE, PLAYER, START, STOP

class TestGameLogic(unittest.TestCase):

    def test_generate_board_dimensions(self):
        for rows, cols in [(5, 5), (10, 10)]:
            board, _, _ = generate_board(rows, cols, 0)
            self.assertEqual(len(board), rows)
            self.assertEqual(len(board[0]), cols)

    def test_generate_board_start_stop_not_adjacent(self):
        board, start, stop = generate_board(7, 7, 0)
        self.assertNotEqual((start["row"], start["col"]), (stop["row"], stop["col"]))
        self.assertGreater(
            abs(start["row"] - stop["row"]) + abs(start["col"] - stop["col"]), 1
        )

    def test_move_player_valid_direction(self):
        board = [
            [EMPTY, EMPTY],
            [EMPTY, PLAYER],
        ]
        player = {"row": 1, "col": 1}
        player = move_player(board, player, "left")
        self.assertEqual(player, {"row": 1, "col": 0})

    def test_move_player_obstacle(self):
        board = [
            [EMPTY, EMPTY],
            [OBSTACLE, PLAYER],
        ]
        player = {"row": 1, "col": 1}
        player = move_player(board, player, "left")
        self.assertEqual(player, {"row": 1, "col": 1})

    def test_move_player_out_of_bounds(self):
        board = [
            [PLAYER, EMPTY],
            [EMPTY, EMPTY],
        ]
        player = {"row": 0, "col": 0}
        player = move_player(board, player, "up")
        self.assertEqual(player, {"row": 0, "col": 0})

    def test_is_game_over_true(self):
        stop = {"row": 2, "col": 2}
        player = {"row": 2, "col": 2}
        self.assertTrue(is_game_over(player, stop))

    def test_is_game_over_false(self):
        stop = {"row": 2, "col": 2}
        player = {"row": 0, "col": 0}
        self.assertFalse(is_game_over(player, stop))

    def test_spawn_player(self):
        board = [
            [EMPTY, EMPTY],
            [EMPTY, EMPTY],
        ]
        player = {"row": 1, "col": 1}
        spawn_player(board, player)
        expected_board = [
            [EMPTY, EMPTY],
            [EMPTY, PLAYER],
        ]
        self.assertEqual(board, expected_board)

    def test_find_path(self):
        board = [
            [START, EMPTY, OBSTACLE],
            [EMPTY, EMPTY, EMPTY],
            [OBSTACLE, EMPTY, STOP],
        ]
        start = {"row": 0, "col": 0}
        stop = {"row": 2, "col": 2}
        path = find_path(board, start, stop)
        self.assertIn({"row": 1, "col": 1}, path)
        self.assertEqual(path[-1], stop)

if __name__ == "__main__":
    unittest.main()
