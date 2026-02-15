from agno.models.groq import Groq
from config.settings import settings
from agno.models.ollama import Ollama

ollama_model = Ollama(
    id="qwen3:1.7b"
)

groq_model = Groq(
    id="openai/gpt-oss-20b",
    api_key=settings.API_KEY_GROQ
)