import os
from agents.extensions.models.any_llm_model import AnyLLMModel
from dotenv import load_dotenv

load_dotenv()

model = AnyLLMModel(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    model = "openrouter/z-ai/glm-5.1",
)