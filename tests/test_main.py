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
        "dimensions": {"rows": 1, "cols": 6},
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
def test_post_solve_no_solution():
    # 入力用のテスト用JSON
    test_input = {
        "dimensions": {"rows": 1, "cols": 6},
        "binaryGrid": [
            [1,1,1,1,1,0]
        ],
        "charGrid": [
            ["ン", "カ", "", "", "", ""]
        ]
    }
    
    response = client.post("/solve", json=test_input)
    assert response.status_code == 200
    
    data = response.json()
    assert "solved" in data
    assert data["solved"] is False
    
def test_post_solve_large_puzzle():
    # 入力用のテスト用JSON
    test_input = {
        "dimensions": {"rows": 5, "cols": 5},
        "binaryGrid": [
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1]
        ],
        "charGrid": [
            ["", "", "", "", "デ"],
            ["",  "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""],
            ["", "", "", "", ""]
        ]
    }
    
    response = client.post("/solve", json=test_input)
    assert response.status_code == 200
    
    data = response.json()
    assert "solved" in data
    assert data["solved"] is True
    assert "grid" in data
    assert len(data["grid"]) == 5
    assert len(data["grid"][0]) == 5
    assert data["grid"] == [
        ["ド", "ヒ", "ド", "イ", "デ"],
        ["ー",  "#", "ダ", "#", "ィ"],
        ["ド", "サ", "イ", "ド", "ン"],
        ["リ", "#", "ト", "#", "ル"],
        ["オ", "ム", "ス", "タ", "ー"]
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
    
def test_post_solve_mismatched_dimensions():
    # dimensionsは2x2だがcharGridが2x3になっている
    payload = {
        "dimensions": {"rows": 2, "cols": 2},
        "binaryGrid": [
            [0, 0],
            [0, 0]
        ],
        "charGrid": [
            ["", "", ""],
            ["", "", ""]
        ]
    }
    response = client.post("/solve", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "mismatched" in data["detail"].lower()
