from pinecone import Pinecone, ServerlessSpec
from app.config import pin_cone_api_key, index_name
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import os

def embedding_init():
    # Initialize Pinecone
    if not pin_cone_api_key:
        raise ValueError("Pinecone API key is not set. Please set the PINECONE_API_KEY environment variable.")
    if not index_name:
        raise ValueError("Pinecone index name is not set. Please set the PINECONE_INDEX_NAME environment variable.")
    

    pc = Pinecone(
            api_key=pin_cone_api_key
        )

    # Now do stuff
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name, 
            dimension=1536, 
            metric='euclidean',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-2'
            )
        )

    
    index = pc.Index(index_name)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings, text_key="content")
    return vector_store