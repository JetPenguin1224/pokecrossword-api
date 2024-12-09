# Test Scenarios

## GET /  
- When accessing the root endpoint (GET /), it should return HTTP 200 with a JSON payload:
     ```json
     {
       "message": "Hello World! This is pokemon crossword solver!"
     }
     ```
## POST /solve with simple valid JSON
- Input: A well-formed crossword puzzle JSON
    - Output:
        - The The response should be HTTP 200 OK.
        - The response JSON should be something

## POST /solve with invalid JSON
- Input: A JSON payload that is missing required fields. For instance, omit "dimensions"
    - Output: 
        - The response should return a 422 Unprocessable Entity status code
        - The response JSON should contain a validation error detail indicating that "dimensions" is missing.



