import chromadb
from chromadb.config import Settings
from html import escape
from typing import Dict, List, Optional
from pathlib import Path
import os

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
    # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)
    list_of_chroma_dirs = [d for d in current_dir.iterdir() if d.is_dir() and d.name.startswith("chroma_")]
    


    # TODO: Loop through each discovered directory
    for chroma_dir in list_of_chroma_dirs:
        
        # TODO: Wrap connection attempt in try-except block for error handling
        try:
            client = chromadb.PersistentClient(path=str(chroma_dir), settings=Settings())
            print(f"Connected to ChromaDB at {chroma_dir}")
            
                
            for collection in client.list_collections():
                try: 
                    document_count = str(client.get_collection(collection.name).count())
                except Exception as e:
                    print(f"Failed to count documents in {collection.name}: {e}")
                    document_count = "Unknown"
                                
                backend_key=chroma_dir.name + "_" + collection.name
                backends[backend_key] = {
                    "directory": str(chroma_dir),
                    "collection": collection.name,
                    "display_name": f"{chroma_dir.name} - {collection.name}",
                    "document_count": document_count,
                }
            
        except Exception as e:
            print(f"Failed to connect to ChromaDB at {chroma_dir}: {e}")
            
        
                
            
    return backends
            
        
            # TODO: Initialize database client with directory path and configuration settings
            
            # TODO: Retrieve list of available collections from the database
            
            # TODO: Loop through each collection found
                # TODO: Create unique identifier key combining directory and collection names
                # TODO: Build information dictionary containing:
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                # TODO: Add collection information to backends dictionary
        
        # TODO: Handle connection or access errors gracefully
            # TODO: Create fallback entry for inaccessible directories
            # TODO: Include error information in display name with truncation
            # TODO: Set appropriate fallback values for missing information

    # TODO: Return complete backends dictionary with all discovered collections
    

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient
    # TODO: Return the collection with the collection_name
    try:
        client = chromadb.PersistentClient(path=chroma_dir, settings=Settings())
        collection = client.get_collection(collection_name)
        return collection,True,None
    except Exception as e:
        print(f"Failed to initialize RAG system with ChromaDB at {chroma_dir}: {e}")
        return None,False,str(e)

def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""
    
    
    where_filter = None
    if mission_filter and mission_filter.lower() != "all":
        where_filter = {"mission": mission_filter}
    
    
    results = collection.query(query_text=query, n_results=n_results, where=where_filter)
    return results

    # TODO: Initialize filter variable to None (represents no filtering)

    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs

    # TODO: Execute database query with the following parameters:
        # TODO: Pass search query in the required format
        # TODO: Set maximum number of results to return
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)

    # TODO: Return query results to caller

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""

    # Wrap the formatted sources in a context element.
    context_parts = ["<context>"]
    for index, document in enumerate(documents, start=1):
        # Use fallback values when metadata is missing, and normalize display labels.
        metadata = metadatas[index - 1] if index <= len(metadatas) else {}
        mission = str(metadata.get("mission", "Unknown")).replace("_", " ").capitalize()
        source = str(metadata.get("source", "Unknown"))
        category = str(metadata.get("category", "General")).replace("_", " ").capitalize()

        # Escape metadata and document text so it remains content, not markup.
        context_parts.extend([
            f'<source id="{index}">',
            f"<mission>{escape(mission)}</mission>",
            f"<file>{escape(source)}</file>",
            f"<category>{escape(category)}</category>",
            f"<content>{escape(document)}</content>",
            "</source>",
        ])

    context_parts.append("</context>")
    return "\n".join(context_parts)

#####TESTING#####
#backends = discover_chroma_backends()
#print(backends)
