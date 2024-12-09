from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World! This is pokemon crossword solver!"}

def test_post_solve_basic_puzzle():
    # 入力用のテスト用JSON
    test_input = {
        "dimensions": {"rows": 6, "cols": 1},
        "binaryGrid": [
            [1,1,1,1,1,0]
        ],
        "charGrid": [
            ["ピ", "カ", "", "", "", ""]
        ]
    }
    
    response = client.post("/solve", json=test_input)
    assert response.status_code == 200
    
    data = response.json()
    assert "solved" in data
    assert data["solved"] is True
    assert "grid" in data
    assert len(data["grid"]) == 1
    assert len(data["grid"][0]) == 6
    assert data["grid"] == [
        ["ピ", "カ", "チ", "ュ", "ウ", "#"]
    ]

def test_post_solve_without_dimensions():
    # dimensions がない
    invalid_payload = {
        "binaryGrid": [
            [0, 0],
            [0, 0]
        ],
        "charGrid": [
            ["", ""],
            ["", ""]
        ]
    }
    response = client.post("/solve", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("dimensions" in str(err.get("loc", "")) for err in data["detail"])
    
def test_post_solve_without_binaryGrid():
    # binaryGrid がない
    invalid_payload = {
        "dimensions": {"rows": 2, "cols": 2},
        "charGrid": [
            ["", ""],
            ["", ""]
        ]
    }
    response = client.post("/solve", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("binaryGrid" in str(err.get("loc", "")) for err in data["detail"])
    
def test_post_solve_without_charGrid():
    # charGrid がない
    invalid_payload = {
        "dimensions": {"rows": 2, "cols": 2},
        "binaryGrid": [
            [0, 0],
            [0, 0]
        ]
    }
    response = client.post("/solve", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert any("charGrid" in str(err.get("loc", "")) for err in data["detail"])
