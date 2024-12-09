from pydantic import BaseModel
from typing import List

class Dimensions(BaseModel):
    rows: int
    cols: int

class SolveRequest(BaseModel):
    dimensions: Dimensions
    binaryGrid: List[List[int]]
    charGrid: List[List[str]]