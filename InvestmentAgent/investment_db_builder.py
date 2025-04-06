import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Configuration
persist_directory = "chroma_db"
pdf_directory = "data"  # Folder containing your PDFs
text_embedding_model = "nomic-embed-text"

def build_investment_db():
    """Builds a ChromaDB from PDFs in the specified directory."""

    if os.path.exists(persist_directory):
        print("ChromaDB already exists. Skipping build.")
        return

    documents = []
    for filename in os.listdir(pdf_directory):
        print(f"Processing file {filename}")
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_directory, filename))
            documents.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model=text_embedding_model)
    Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    print("ChromaDB built successfully.")


if __name__ == "__main__":
    build_investment_db()