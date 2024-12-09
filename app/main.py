from fastapi import FastAPI, HTTPException
from app.schemas import SolveRequest
from app.utils import solve_pokecrossword

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World! This is pokemon crossword solver!"}

@app.post("/solve")
def solve_puzzle(payload: SolveRequest):
    rows = payload.dimensions.rows
    cols = payload.dimensions.cols
    binaryGrid = payload.binaryGrid
    charGrid = payload.charGrid
    pokemon_names = "data/pokemon_names.json"

    # binaryGridのサイズチェック
    if len(payload.binaryGrid) != rows or any(len(row) != cols for row in payload.binaryGrid):
        raise HTTPException(status_code=400, detail="Grid dimensions mismatched: binaryGrid")

    # charGridのサイズチェック
    if len(payload.charGrid) != rows or any(len(row) != cols for row in payload.charGrid):
        raise HTTPException(status_code=400, detail="Grid dimensions mismatched: charGrid")
    # ここで本来はpayloadを解析してパズルを解く処理が入るが、
    # 今はテストを通すために決め打ちでレスポンスを返す
    result = solve_pokecrossword(rows, cols, binaryGrid, charGrid, pokemon_names)
    if result is not None:
        return {"solved": True, "grid": result}
    else:
        return {"solved": False
    }