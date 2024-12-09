from pysat.formula import CNF
from pysat.solvers import Solver
from collections import defaultdict
import json
from itertools import combinations, product

class CnfGenerator:
    def __init__(self, rows, cols, grid, pre_filled, pokemon_names_file):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.pre_filled = pre_filled
        with open(pokemon_names_file, 'r') as f:
            self.pokemon_names = json.load(f)
        # 使用されているカタカナ文字の集合を作成
        self.katakana_chars = set()
        for name in self.pokemon_names:
            for char in name:
                self.katakana_chars.add(char)
        self.katakana_chars = list(self.katakana_chars)
        self.katakana_chars.sort()
        # 変数のマッピングを初期化
        self.var_num = 1
        self.cell_char_vars = {}  # (セル座標, 文字) -> 変数番号
        self.var_cell_char = {}   # 変数番号 -> (セル座標, 文字)
        self.word_vars = {}       # (スロットID, 単語) -> 変数番号
        self.var_slot_word = {}   # 変数番号 -> (スロットID, 単語)

    # スロットを見つける関数（縦方向と横方向）
    def find_slots(self):
        slots = []
        # 縦方向のスロットを探索
        for j in range(self.cols):
            i = 0
            while i < self.rows:
                if self.grid[i][j] == 1:
                    cells = []
                    while i < self.rows and self.grid[i][j] == 1:
                        cells.append((i,j))
                        i += 1
                    if len(cells) > 1:
                        slots.append(cells)
                else:
                    i += 1
        # 横方向のスロットを探索
        for i in range(self.rows):
            j = 0
            while j < self.cols:
                if self.grid[i][j] == 1:
                    cells = []
                    while j < self.cols and self.grid[i][j] == 1:
                        cells.append((i,j))
                        j += 1
                    if len(cells) > 1:
                        slots.append(cells)
                else:
                    j += 1
        return slots

    # 各スロットに適合するポケモン名をフィルタリング
    def filter_words(self, slots):
        slot_words = []
        for slot in slots:
            length = len(slot)
            words = [name for name in self.pokemon_names if len(name) == length]
            slot_words.append(words)
        return slot_words

    # セルと文字の変数を割り当て
    def assign_cell_char_vars(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:  # 白マスの場合
                    for k in self.katakana_chars:
                        self.cell_char_vars[((i,j), k)] = self.var_num
                        self.var_cell_char[self.var_num] = ((i,j), k)
                        self.var_num +=1

    # スロットと単語の変数を割り当て
    def assign_slot_word_vars(self, slots, slot_words):
        for s_id, words in enumerate(slot_words):
            for word in words:
                self.word_vars[(s_id, word)] = self.var_num
                self.var_slot_word[self.var_num] = (s_id, word)
                self.var_num += 1

    # 各セルに対して「ちょうど1つの文字」を割り当てる制約を生成
    def generate_cell_constraints(self):
        cnf = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1:  # 白マスの場合
                    vars_in_cell = []
                    for k in self.katakana_chars:
                        v = self.cell_char_vars[((i,j), k)]
                        vars_in_cell.append(v)
                    # 少なくとも1つの文字が割り当てられる
                    cnf.append(vars_in_cell)
                    # 2つの文字が同時に割り当てられない
                    for v1, v2 in combinations(vars_in_cell, 2):
                        cnf.append([-v1, -v2])
        return cnf

    # 事前に埋められたセルの制約を生成
    def generate_prefilled_constraints(self):
        cnf = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 1 and self.pre_filled[i][j] != '':
                    k = self.pre_filled[i][j]
                    # X_{(i,j), k} = True
                    v_true = self.cell_char_vars[((i,j), k)]
                    cnf.append([v_true])
                    # 他の文字はFalse
                    for k_prime in self.katakana_chars:
                        if k_prime != k:
                            v_false = self.cell_char_vars[((i,j), k_prime)]
                            cnf.append([-v_false])
        return cnf

    # 各スロットに対して「ちょうど1つの単語」を割り当てる制約を生成
    def generate_slot_constraints(self, slots, slot_words):
        cnf = []
        for s_id, words in enumerate(slot_words):
            vars_in_slot = []
            for word in words:
                v = self.word_vars[(s_id, word)]
                vars_in_slot.append(v)
            # 少なくとも1つの単語が割り当てられる
            cnf.append(vars_in_slot)
            # 2つの単語が同時に割り当てられない
            for v1, v2 in combinations(vars_in_slot, 2):
                cnf.append([-v1, -v2])
        return cnf

    # スロットの単語とセルの文字をリンクする制約を生成
    def generate_word_cell_link_constraints(self, slots, slot_words):
        cnf = []
        for s_id, (slot, words) in enumerate(zip(slots, slot_words)):
            for word in words:
                v_word = self.word_vars[(s_id, word)]
                for idx, (i,j) in enumerate(slot):
                    k = word[idx]
                    v_cell_char = self.cell_char_vars[((i,j), k)]
                    # (¬Y_{s,w} ∨ X_{c_i,k_i})
                    cnf.append([-v_word, v_cell_char])
        return cnf

    # 同じ単語が二度使われないようにする制約を生成
    def generate_unique_word_constraints(self, slot_words):
        cnf = []
        total_slots = len(slot_words)
        for s1 in range(total_slots):
            for s2 in range(s1 + 1, total_slots):
                common_words = set(slot_words[s1]) & set(slot_words[s2])
                for word in common_words:
                    v1 = self.word_vars[(s1, word)]
                    v2 = self.word_vars[(s2, word)]
                    # (¬Y_{s1,word} ∨ ¬Y_{s2,word})
                    cnf.append([-v1, -v2])
        return cnf

    # CNFを生成するメイン関数
    def generate_cnf(self):
        slots = self.find_slots()
        slot_words = self.filter_words(slots)
        self.assign_cell_char_vars()
        self.assign_slot_word_vars(slots, slot_words)
        cnf = []
        cnf += self.generate_cell_constraints()
        cnf += self.generate_prefilled_constraints()
        cnf += self.generate_slot_constraints(slots, slot_words)
        cnf += self.generate_word_cell_link_constraints(slots, slot_words)
        cnf += self.generate_unique_word_constraints(slot_words)
        self.slots = slots
        self.slot_words = slot_words
        return cnf

def solve_pokecrossword(rows, cols, grid, pre_filled, pokemon_names_file):
    cnf_gen = CnfGenerator(rows, cols, grid, pre_filled, pokemon_names_file)
    cnf = cnf_gen.generate_cnf()
    slots = cnf_gen.slots
    slot_words = cnf_gen.slot_words
    with Solver(name='g4') as solver:
        for clause in cnf:
            solver.add_clause(clause)
        if solver.solve():
            model = solver.get_model()
            # 解を格納するグリッドを作成
            solution = [['#' for _ in range(cols)] for _ in range(rows)]
            cell_assignments = {}
            for var in model:
                if var > 0:
                    if var in cnf_gen.var_cell_char:
                        (i,j), k = cnf_gen.var_cell_char[var]
                        solution[i][j] = k
                        cell_assignments[(i,j)] = k
            return solution
        else:
            return None
