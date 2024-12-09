# Test Scenarios

1. **GET /**  
   - When accessing the root endpoint (GET /), it should return HTTP 200 with a JSON payload:
     ```json
     {
       "message": "Hello World! This is pokemon crossword solver!"
     }
     ```
2. **POST /solve**
    - Input: A well-formed crossword puzzle JSON, for example:
    ```json
    {
        "dimensions": {
            "rows": 1,
            "cols": 6
        },
        "binaryGrid": [
            [1, 1, 1, 1, 1, 0]
        ],
        "charGrid": [
            ["ピ","カ","","","",""]
        ]
    }
    ```
    - Output:
        - The The response should be HTTP 200 OK.
        - The response JSON should be something like:
        ```json
        {
        "solved": true,
        "grid": [
        ["ピ","カ","チ","ュ","ウ"
        ]
        ]
        }

        ```


