import pytest
from app.utils import solve_pokecrossword
import json
import string
import os
from hypothesis import given, strategies as st, assume
from hypothesis import HealthCheck, settings, Phase
from hypothesis.strategies import composite


with open("data/pokemon_names.json", "r", encoding="utf-8") as f:
    pokemon_names = set(json.load(f))

katakana_chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴ"
katakana_strategy = st.sampled_from(list(katakana_chars) + [""])

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
    


@composite
def crossword_strategies(draw):
    rows = draw(st.integers(min_value=2, max_value=6))
    cols = draw(st.integers(min_value=2, max_value=6))
    
    # rows, colsに合わせてbinaryGridを生成
    # 必ず rows x cols サイズで、1マス以上1が存在する
    binaryGrid = draw(
        st.lists(
            st.lists(st.integers(min_value=0, max_value=1), min_size=cols, max_size=cols),
            min_size=rows, max_size=rows
        ).filter(lambda g: any(1 in row for row in g))
    )

    # charGrid生成: 1マスはカタカナまたは空文字、0マスは空文字
    charGrid = []
    for r in range(rows):
        row_chars = []
        for c in range(cols):
            if binaryGrid[r][c] == 1:
                ch = draw(katakana_strategy)
                row_chars.append(ch)
            else:
                row_chars.append("")
        charGrid.append(row_chars)

    return rows, cols, binaryGrid, charGrid

@given(crossword_strategies())
def test_property_solve_pokemon_crossword(params):
    rows, cols, binaryGrid, charGrid = params
    pokemon_names_file = "data/pokemon_names.json"
    
    result = solve_pokecrossword(rows, cols, binaryGrid, charGrid, pokemon_names_file)
    if result is None:
        # 解なしは問題なし
        return

    # 結果がポケモンの名前のみで構成されているかチェック
    # 横方向の単語チェック
    for r in range(rows):
        word = ""
        for c in range(cols):
            if binaryGrid[r][c] == 1:
                word += result[r][c]
            else:
                # 黒マスで単語区切り
                if len(word) > 1 and word not in pokemon_names:
                    pytest.fail(f"Found a word not in pokemon_names: {word}")
                word = ""
        # 行末でまだwordが残っている場合
        if len(word) > 1 and word not in pokemon_names:
            pytest.fail(f"Found a word not in pokemon_names: {word}")

    # 縦方向の単語チェック
    for c in range(cols):
        word = ""
        for r in range(rows):
            if binaryGrid[r][c] == 1:
                word += result[r][c]
            else:
                # 黒マスで単語区切り
                if len(word) > 1 and word not in pokemon_names:
                    pytest.fail(f"Found a word not in pokemon_names: {word}")
                word = ""
        # 列末でまだwordが残っている場合
        if len(word) > 1 and word not in pokemon_names:
            pytest.fail(f"Found a word not in pokemon_names: {word}")
    
    # #が入っているマスがBinaryGridの0のマスと一致しているかチェック
    for r in range(rows):
        for c in range(cols):
            if result[r][c] == "#":
                assert binaryGrid[r][c] == 0
            else:
                assert binaryGrid[r][c] == 1