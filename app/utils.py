from pysat.formula import CNF
from pysat.solvers import Solver
from app.cnf_generator import CnfGenerator

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
