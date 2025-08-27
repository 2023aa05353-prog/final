# utils/vector_store_setup.py
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_PATH = "data/documents"
DB_PATH = "vectorstore"

def create_vector_db():
    """Creates a FAISS vector store from documents in the data/documents directory."""
    print("Starting document loading...")
    loader = DirectoryLoader(
        DATA_PATH,
        glob="*.txt",
        loader_cls=TextLoader,
        show_progress=True
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents.")

    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    print("Embedding model loaded.")

    print("Creating FAISS vector store...")
    if os.path.exists(DB_PATH):
        print(f"Vector store already exists at {DB_PATH}. Deleting old version.")
        import shutil
        shutil.rmtree(DB_PATH)
        
    db = FAISS.from_documents(texts, embeddings)
    db.save_local(DB_PATH)
    print(f"Vector store created and saved at {DB_PATH}.")

if __name__ == "__main__":
    create_vector_db()
