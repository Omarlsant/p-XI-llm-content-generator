import os
import shutil
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# --- Configuration ---
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
PDF_DIR = os.path.join(os.path.dirname(__file__), "temp_pdf")
os.makedirs(PDF_DIR, exist_ok=True)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# --- FIX: Hardcoded list of direct PDF links to famous RAG papers ---
PAPER_URLS = [
    "https://arxiv.org/pdf/2005.11401",  # The original RAG paper by Lewis et al.
    "https://arxiv.org/pdf/2302.07842",  # A paper on In-Context RALM
    "https://arxiv.org/pdf/2401.05022",  # A recent survey on RAG for LLMs
]

def download_papers_manually(urls: list):
    """Downloads papers directly from a list of URLs."""
    filepaths = []
    print("Starting manual download of specified papers...")
    for url in urls:
        try:
            # Create a simple filename from the URL
            filename = url.split("/")[-1] + ".pdf"
            filepath = os.path.join(PDF_DIR, filename)
            
            # Use requests for a robust download
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status() # Raise an exception for bad status codes (404, 500 etc)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"-> Downloaded: {filename}")
            filepaths.append(filepath)
        except Exception as e:
            print(f"!!! Error downloading {url}: {e}")
            
    return filepaths


def load_and_split_documents(filepaths: list):
    """Loads PDFs and splits them into chunks."""
    all_chunks = []
    for path in filepaths:
        try:
            loader = PyPDFLoader(path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(documents)
            all_chunks.extend(chunks)
            print(f"Loaded and split {len(chunks)} chunks from {os.path.basename(path)}")
        except Exception as e:
            print(f"Error processing file {path}: {e}")
    return all_chunks

def main():
    print("--- Starting MANUAL Data Ingestion Process ---")
    
    # Clean up old database if it exists
    if os.path.exists(DB_DIR):
        print(f"Deleting old database at: {DB_DIR}")
        shutil.rmtree(DB_DIR)

    # Download the papers from the hardcoded list
    paper_filepaths = download_papers_manually(PAPER_URLS)
    
    if not paper_filepaths:
        print("No papers were downloaded. Please check network connection. Exiting.")
        return

    document_chunks = load_and_split_documents(paper_filepaths)

    if not document_chunks:
        print("No document chunks were created. Exiting.")
        return

    print(f"Creating new ChromaDB at: {DB_DIR}")
    db = Chroma.from_documents(
        documents=document_chunks, 
        embedding=embedding_function,
        persist_directory=DB_DIR
    )
    print("--- Data Ingestion Complete ---")
    print(f"Total chunks indexed: {db._collection.count()}")
    
    # Clean up temporary PDF files
    for pdf in paper_filepaths:
        os.remove(pdf)
    shutil.rmtree(PDF_DIR)
    print("Temporary PDF files and directory have been removed.")

if __name__ == "__main__":
    main()