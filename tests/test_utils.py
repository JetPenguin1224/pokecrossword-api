import pytest
from app.utils import solve_pokecrossword

def test_solve_pokemon_crossword_basic():
    rows, cols = 4, 5
    binaryGrid = [
        [1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
    ]
    charGrid = [
        ["ピ", "", "", "ュ", "ウ"],
        ["",  "", "", "", ""],
        ["", "ゴ", "", "", ""],
        ["", "ン", "", "", ""],
    ]
    # テスト用JSONファイル
    pokemon_names_file = "tests/data/pokemon_names.json"
    
    result = solve_pokecrossword(rows, cols, binaryGrid, charGrid, pokemon_names_file)
    assert len(result) == rows
    assert len(result[0]) == cols
    assert result == [
        ["ピ", "カ", "チ", "ュ", "ウ"],
        ["#",  "ビ", "#", "#", "#"],
        ["#", "ゴ", "#", "#", "#"],
        ["#", "ン", "#", "#", "#"],
    ]

def test_solve_pokemon_crossword_no_solution():
    rows, cols = 4, 5
    binaryGrid = [
        [1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0],
    ]
    charGrid = [
        ["ン", "", "", "ュ", "ウ"],
        ["",  "", "", "", ""],
        ["", "ゴ", "", "", ""],
        ["", "ン", "", "", ""],
    ]
    # テスト用JSONファイル
    pokemon_names_file = "tests/data/pokemon_names.json"
    
    result = solve_pokecrossword(rows, cols, binaryGrid, charGrid, pokemon_names_file)
    assert result is None