import chromadb
from chromadb.config import Settings

chroma_client = chromadb.Client(Settings(
    persist_directory="databases/chroma_db"
))

print("ChromaDB instance initialized at databases/chroma_db")