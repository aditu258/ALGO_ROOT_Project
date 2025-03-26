import requests
import json

response = requests.post(
    "http://localhost:56165/execute",
    json={"prompt": "Open calculator"}
)

# Pretty-print the JSON response
formatted = json.dumps(response.json(), indent=2)
print("API Response:")
print(formatted)

# Extract and display the executable code separately
print("\nGenerated Python Code:")
print(response.json()["code"])

'''
curl -X POST "http://localhost:53243/execute" ^
More? -H "Content-Type: application/json" ^
More? -d "{\"prompt\":\"Calculator code\"}"'''