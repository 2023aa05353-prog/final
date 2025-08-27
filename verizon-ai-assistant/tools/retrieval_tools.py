# tools/retrieval_tools.py
import json
from langchain_core.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_PATH = "vectorstore"

@tool
def search_business_documents(query: str) -> str:
    """
    Performs a semantic search on internal business documents like policy manuals and product brochures.
    Use this to find information about installation clauses, return policies, product specifications, etc.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    results = db.similarity_search(query, k=2) # Get top 2 results
    
    if not results:
        return "No relevant information found in the documents."
        
    snippets = [
        {"snippet": doc.page_content, "source": doc.metadata.get("source", "Unknown")}
        for doc in results
    ]
    return json.dumps(snippets)
