
import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------
# API Keys (read-only)
# -------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------
# Embedding Configuration
# -------------------------------
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# -------------------------------
# Chunking Configuration
# -------------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# -------------------------------
# LLM Defaults
# -------------------------------
DEFAULT_LLM_PROVIDER = "groq"   # or "gemini"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"

# -------------------------------
# Feature Flags
# -------------------------------
ENABLE_LLM = True
