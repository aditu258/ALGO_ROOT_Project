# Import necessary libraries for building the API
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # For data validation
from typing import Optional
import logging
from datetime import datetime

# Import custom modules we created
from vector_db import VectorDB          # Handles function search
from code_generator import CodeGenerator  # Creates executable code
from session_manager import SessionManager  # Tracks user conversations
from functions import FUNCTION_REGISTRY  # List of available functions

# Initialize all components
vector_db = VectorDB()           # Sets up search functionality
code_generator = CodeGenerator() # Prepares code generation
session_manager = SessionManager() # Manages user sessions

# Create the API application
app = FastAPI(title="AI Function Execution API")

# Allow web browsers to communicate with our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all websites (for development)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Configure logging to track API activity
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_service.log'),  # Save logs to file
        logging.StreamHandler()  # Also show logs in console
    ]
)

# Load functions into search database if empty
if vector_db.index.describe_index_stats()['total_vector_count'] == 0:
    # Prepare function descriptions for AI search
    functions_to_index = {name: data["description"] for name, data in FUNCTION_REGISTRY.items()}
    vector_db.upsert_functions(functions_to_index)  # Store in database

# Define what the API expects to receive
class ExecuteRequest(BaseModel):
    prompt: str                   # User's text request
    session_id: Optional[str] = None  # Optional conversation ID

# Define what the API will respond with
class ExecuteResponse(BaseModel):
    function: str    # Name of matched function
    code: str        # Ready-to-run Python code
    description: str # Plain English explanation

# Debug endpoint to check registered functions
@app.get("/debug/functions")
def list_functions():
    """Shows all available functions and search database status"""
    return {
        "registered_functions": list(FUNCTION_REGISTRY.keys()),
        "indexed_functions": vector_db.index.describe_index_stats()
    }

# Main API endpoint
@app.post("/execute", response_model=ExecuteResponse)
async def execute_function(request: ExecuteRequest):
    """
    Takes a user's request in plain English,
    finds the best matching function,
    and returns executable Python code
    """
    logger.info(f"Processing request: {request.prompt}")
    
    # Step 1: Find the most relevant function using AI search
    function_name, description = vector_db.retrieve_function(request.prompt)
    
    if not function_name:
        logger.warning(f"No function found for: {request.prompt}")
        raise HTTPException(status_code=404, detail="No matching function found")
    
    # Step 2: Generate ready-to-use Python code
    generated_code = code_generator.generate_execution_code(function_name)
    
    # Step 3: Remember this interaction if part of a conversation
    if request.session_id:
        session_manager.add_to_session(request.session_id, request.prompt, function_name)
    
    # Return the results
    return {
        "function": function_name,
        "code": generated_code,
        "description": description
    }

# Start the API server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=0)  # Auto-select available port