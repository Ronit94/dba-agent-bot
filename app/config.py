from dotenv import load_dotenv
import os
load_dotenv()


database_url = os.getenv("DATABASE_URL")
database_name = os.getenv("DATABASE_NAME")
pin_cone_api_key = os.getenv("PINCONE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")
anthropic_api_key = os.getenv("ANTROPIC_API_KEY")
