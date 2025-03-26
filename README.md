# LLM + RAG-Based Function Execution API

## Overview
This project implements a **Retrieval-Augmented Generation (RAG) and Large Language Model (LLM) powered API service** that dynamically retrieves and executes automation functions. The system processes user prompts, maps them to predefined functions, and generates executable Python code for function invocation.

## Features
✅ **Function Registry:** Predefined automation functions such as opening applications, monitoring system usage, and executing shell commands.
✅ **RAG for Function Retrieval:** Stores function metadata in a vector database and retrieves the best-matching function dynamically.
✅ **Dynamic Code Generation:** Generates structured, executable Python scripts for invoking retrieved functions.
✅ **Session-Based Context Management:** Maintains interaction history to enhance function retrieval and execution.
✅ **REST API Service:** Implements endpoints using FastAPI for function execution via HTTP requests.

---

## Requirements Fulfilled
The project successfully meets all the given requirements:

### 1️⃣ Function Registry
- Implements a registry of common automation functions:
  - **Application Control:** Open Chrome, Calculator, Notepad.
  - **System Monitoring:** Retrieve CPU/RAM usage.
  - **Command Execution:** Run shell commands.

Example:
```python
import os
import webbrowser

def open_chrome():
    webbrowser.open("https://www.google.com")

def open_calculator():
    os.system("calc")
```

### 2️⃣ LLM + RAG for Function Retrieval
- Uses **SentenceTransformer (all-MiniLM-L6-v2)** to convert user queries into embeddings.
- Stores function metadata in **Pinecone** vector database for retrieval.
- Dynamically retrieves the best-matching function.

### 3️⃣ Dynamic Code Generation
- Generates structured, executable Python code for function execution.
- Ensures:
  - Proper imports
  - Error handling
  - Modularity

Example Generated Code for "Launch Chrome":
```python
from automation_functions import open_chrome

def main():
    try:
        open_chrome()
        print("Chrome opened successfully.")
    except Exception as e:
        print(f"Error executing function: {e}")

if __name__ == "__main__":
    main()
```

### 4️⃣ Context Management
- Integrates **session-based memory** to track user queries.
- Enhances function retrieval and execution with historical context.

### 5️⃣ API Service Implementation
- Implements an API using **FastAPI** with the following endpoint:

#### `POST /execute`
**Request:**
```json
{
  "prompt": "Open calculator"
}
```
**Response:**
```json
{
  "function": "open_calculator",
  "code": "<Generated Code Snippet>",
  "description": "Executes the calculator application."
}
```

---

## Deliverables Checklist ✅
✔️ **Function Registry** (Python script with predefined functions)  
✔️ **RAG Model** (Vector search + LLM for function retrieval)  
✔️ **Dynamic Code Generation** (Structured function invocation scripts)  
✔️ **API Service** (Function execution via REST API)  

## Evaluation Criteria 🎯
- ✅ **Accuracy of Function Retrieval using RAG**
- ✅ **Quality and Structure of Generated Code**
- ✅ **API Robustness and Error Handling**
- ✅ **Extendability for Future Automation Tasks**

---

## Bonus Enhancements 🚀
✅ **Implemented Logging and Monitoring** for function execution.  
✅ **Designed Extendable Architecture** to support future user-defined functions.

## How to Run 📌
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up environment variables** (Pinecone API Key, etc.).
3. **Run the API server**
   ```bash
   python main.py
   ```
4. **Test the API using cURL or Postman**

```bash
curl -X POST "http://localhost:8000/execute" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Open calculator"}'
```

---

## Screenshot
![Output](screenshot\Screenshot 2025-03-26 122613.png)  


