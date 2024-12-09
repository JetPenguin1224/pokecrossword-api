import json
import pytest
import os
from tempfile import NamedTemporaryFile
from app.cnf_generator import CnfGenerator  

@pytest.fixture
def pokemon_names_file():
    # テスト用ポケモン名ファイルを一時的に作成
    pokemon_names = ["ピッピ", "ピィ", "ルリリ","パモ"]
    with NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as f:
        json.dump(pokemon_names, f, ensure_ascii=False)
        temp_name = f.name
    yield temp_name
    os.remove(temp_name)


@pytest.fixture
def simple_cnf_gen(pokemon_names_file):
    rows = 3
    cols = 3
    grid = [
        [1,1,1],
        [1,0,0],
        [0,0,0]
    ]
    
    pre_filled = [
        ["", "", "ピ"],
        ["", "", ""],
        ["", "", ""]
    ]
    return CnfGenerator(rows, cols, grid, pre_filled, pokemon_names_file)


def test_find_slots(simple_cnf_gen):
    slots = simple_cnf_gen.find_slots()
    # 3文字スロットが1つ、2文字スロットが1つのはず
    assert len(slots) == 2
    assert [(0,0), (0,1), (0,2)] in slots

def test_filter_words(simple_cnf_gen):
    slots = [
        [(0,0), (1,0), (2,0)],  # 3文字スロット
        [(0,0), (0,1)]          # 2文字スロット  (ダミー用)
    ]
    filtered = simple_cnf_gen.filter_words(slots)
    # 3文字スロットにはピッピとルリリが、2文字スロットにはピィとパモが候補となるはず
    assert len(filtered) == 2
    assert filtered[0] == ["ピッピ", "ルリリ"]  
    assert set(filtered[1]) == {"ピィ","パモ" }


def test_assign_cell_char_vars(simple_cnf_gen):
    simple_cnf_gen.assign_cell_char_vars()
    for (coord, char), var in simple_cnf_gen.cell_char_vars.items():
        assert isinstance(coord, tuple)
        assert len(coord) == 2
        assert isinstance(char, str)
        assert isinstance(var, int)


def test_assign_slot_word_vars(simple_cnf_gen):
    # スロットとワードを仮に設定
    slots = [
        [(0,0), (1,0), (2,0)],
        [(0,0), (0,1)]
    ]
    slot_words = [
        ["ピッピ", "ルリリ"],   # 3文字スロット
        ["ピィ", "パモ"]  # 2文字スロット
    ]
    simple_cnf_gen.assign_slot_word_vars(slots, slot_words)
    for (s_id, word), var in simple_cnf_gen.word_vars.items():
        assert isinstance(s_id, int)
        assert isinstance(word, str)
        assert isinstance(var, int)

def test_generate_cell_constraints(simple_cnf_gen):
    simple_cnf_gen.assign_cell_char_vars()
    cnf = simple_cnf_gen.generate_cell_constraints()
    assert len(cnf) > 0
    for clause in cnf:
        assert len(clause) > 0
        for lit in clause:
            assert isinstance(lit, int)


def test_generate_prefilled_constraints(simple_cnf_gen):
    simple_cnf_gen.assign_cell_char_vars()
    cnf = simple_cnf_gen.generate_prefilled_constraints()
    # ピが入っているセルに対する埋め込み制約が生成されているはず
    assert len(cnf) > 0


def test_generate_slot_constraints(simple_cnf_gen):
    # slots, slot_words を仮に設定
    slots = [
        [(0,0), (1,0), (2,0)],
        [(0,0), (0,1)]
    ]
    slot_words = [
        [],  # 3文字該当なし
        ["ヤドン", "ミュウ"]
    ]
    simple_cnf_gen.assign_slot_word_vars(slots, slot_words)
    cnf = simple_cnf_gen.generate_slot_constraints(slots, slot_words)
    # 2スロット目に2ワード → 「少なくとも一つ」「両方同時にはダメ」の制約が発生
    assert len(cnf) > 0
    # 条件確認(基本的なCNF形式チェック)
    for clause in cnf:
        for lit in clause:
            assert isinstance(lit, int)





