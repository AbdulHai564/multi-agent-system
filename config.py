from dotenv import load_dotenv
import os


load_dotenv()



GROQ_API_KEY=os.getenv("GROQ_API_KEY")
QDRANT_URL=os.getenv("QDRANT_URL")
QDRANT_API_KEY=os.getenv("QDRANT_API_KEY")
TAVILY_API_KEY=os.getenv("TIVALY_API_KEY")
COHERE_API_KEY=os.getenv("COHERE_API_KEY")
E2B_API_KEY=os.getenv("E2B_API_KEY")
COLLECTION_NAME="AgenticAI"

