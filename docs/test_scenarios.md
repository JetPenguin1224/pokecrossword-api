# Test Scenarios

## GET /  
- When accessing the root endpoint (GET /), it should return HTTP 200 with a greeting message JSON
 
## POST /solve with simple valid JSON
- Input: A well-formed crossword puzzle JSON
    - Output:
        - The The response should be HTTP 200 OK.
        - The response JSON should be something

## POST /solve with invalid JSON
- Input: A JSON payload that is missing required fields
    - Output: 
        - The response should return a 422 Unprocessable Entity status code
        - The response JSON should contain a validation error detail indicating that "dimensions" is missing.
- Input: A JSON payload where `dimensions` specifies (rows=2, cols=2) but `binaryGrid` or `charGrid` does not match these dimensions.
    - Output:
        - The endpoint should return HTTP 400 (Bad Request) because the grids do not match the specified dimensions.
        - The response JSON should include an error message explaining the mismatch.

    




