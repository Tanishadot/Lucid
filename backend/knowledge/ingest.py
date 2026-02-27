import os
import json
import logging
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
DATASET_PATH = "knowledge/dataset"
PERSIST_DIR = "knowledge/vector_store/db"

# Verify OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY required for ingestion")

print("=== INGESTION STARTUP ===")
print(f"OPENAI_API_KEY detected: {bool(os.getenv('OPENAI_API_KEY'))}")
print(f"Embedding class: OpenAIEmbeddings")
print(f"Chroma persist directory: {PERSIST_DIR}")
print("Ingesting with OpenAIEmbeddings")
print("=== INGESTION READY ===")

def load_documents():
    """Load documents from JSON files in the dataset directory"""
    documents = []
    
    if not os.path.exists(DATASET_PATH):
        logger.error(f"Dataset directory not found: {DATASET_PATH}")
        return documents
    
    json_files = [f for f in os.listdir(DATASET_PATH) if f.endswith(".json")]
    
    if not json_files:
        logger.warning(f"No JSON files found in {DATASET_PATH}")
        return documents
    
    logger.info(f"Loading documents from {len(json_files)} JSON files")
    
    for file in json_files:
        file_path = os.path.join(DATASET_PATH, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                if not isinstance(data, list):
                    # Handle JSON files with different structure
                    if "units" in data and isinstance(data["units"], list):
                        data = data["units"]
                    else:
                        logger.warning(f"Expected list in {file}, got {type(data)}")
                        continue
                
                for i, item in enumerate(data):
                    if not isinstance(item, dict):
                        logger.warning(f"Expected dict in {file}[{i}], got {type(item)}")
                        continue
                    
                    # Handle different JSON structures and extract text content
                    text_content = ""
                    
                    # Try different field names that might contain text
                    for field in ["text", "core_reframe", "short_reframe", "short_question"]:
                        if field in item and isinstance(item[field], str) and item[field].strip():
                            text_content = item[field].strip()
                            break
                    
                    # If no direct text field, try to construct from question_bank
                    if not text_content and "question_bank" in item:
                        if isinstance(item["question_bank"], list) and item["question_bank"]:
                            # Use the first question as text content
                            first_question = item["question_bank"][0]
                            if isinstance(first_question, str) and first_question.strip():
                                text_content = first_question.strip()
                    
                    if not text_content:
                        logger.warning(f"No valid text content found in {file}[{i}]")
                        continue
                    
                    text = text_content
                    if not isinstance(text, str) or not text.strip():
                        logger.warning(f"Empty or invalid text in {file}[{i}]")
                        continue
                    
                    # Create document with metadata
                    metadata = {
                        "source": file,
                        "index": i
                    }
                    
                    # Add any additional metadata from the item
                    for key, value in item.items():
                        if key != "text" and isinstance(value, (str, int, float, bool)):
                            metadata[key] = value
                    
                    documents.append(
                        Document(
                            page_content=text.strip(),
                            metadata=metadata
                        )
                    )
                    
                logger.info(f"Loaded {len([d for d in documents if d.metadata['source'] == file])} documents from {file}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file}: {e}")
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")
    
    logger.info(f"Total documents loaded: {len(documents)}")
    return documents

def ingest():
    """Ingest documents into Chroma vector store"""
    # Load documents
    docs = load_documents()
    
    if not docs:
        logger.error("No documents to ingest")
        return
    
    try:
        # Initialize embeddings (OpenAI only)
        logger.info("Initializing OpenAI embeddings...")
        embeddings = OpenAIEmbeddings()
        
        # Create persist directory if it doesn't exist
        os.makedirs(PERSIST_DIR, exist_ok=True)
        
        # Initialize Chroma vector store
        logger.info(f"Creating Chroma vector store at {PERSIST_DIR}...")
        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )
        
        # Persist the vector store
        vectordb.persist()
        logger.info("Vector store persisted successfully")
        
        # Test the vector store
        logger.info("Testing vector store...")
        test_results = vectordb.similarity_search("test", k=2)
        logger.info(f"Vector store test: found {len(test_results)} documents")
        
        logger.info("Ingestion completed successfully")
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise

if __name__ == "__main__":
    ingest()
