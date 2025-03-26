import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

load_dotenv()  # Load API keys from .env file

class VectorDB:
    """
    Uses AI to understand user requests and find matching functions
    Leverages Pinecone for fast similarity search
    """
    def __init__(self):
        # Configure AI search components
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # Understands text
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))  # Cloud database
        self.index = self._initialize_index()  # Prepare search system

    def _initialize_index(self):
        """Sets up the search database if it doesn't exist"""
        index_name = "function-registry"
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=384,  # Matches our AI model
                metric="cosine",  # How we compare requests
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        return self.pc.Index(index_name)

    def upsert_functions(self, functions):
        """Stores all available functions for future searching"""
        # Convert function descriptions to AI-understandable format
        function_embeddings = [
            (name, self.model.encode(desc).tolist(), {"description": desc})
            for name, desc in functions.items()
        ]
        self.index.upsert(vectors=function_embeddings)

    def retrieve_function(self, user_query):
        """Finds the best function for a user's request"""
        # Convert query to AI format
        query_embedding = self.model.encode(user_query).tolist()
        # Search database
        results = self.index.query(vector=query_embedding, top_k=1, include_metadata=True)
        # Return best match if confident
        if results and results.get("matches"):
            best_match = results["matches"][0]
            if best_match["score"] > 0.1:  # Minimum confidence threshold
                return best_match["id"], best_match["metadata"]["description"]
        return None, None