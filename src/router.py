import os
from google import genai
from groq import Groq
# from semantic_router import Route
# from semantic_router.layer import RouteLayer
from semantic_router import Route, SemanticRouter
from semantic_router.encoders import LiteLLMEncoder
# In src/router.py
from src.config import GEMINI_API_KEY, GROQ_API_KEY

# Initialize SDK Clients
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

# ...

# # Initialize SDK Clients
# gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
# groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define Route Intents
chitchat_route = Route(
    name="chitchat",
    utterances=[
        "hello", "hi there", "how are you?", 
        "good morning", "what is your name?", "tell me a joke"
    ]
)

coding_route = Route(
    name="coding",
    utterances=[
        "write a python script to parse json", 
        "how do I debug a null pointer exception", 
        "implement a binary search algorithm", 
        "fix this javascript loop"
    ]
)

# Initialize Route Layer
encoder = LiteLLMEncoder(
    name="gemini/gemini-embedding-001",
    api_key=GEMINI_API_KEY
)
router = SemanticRouter(encoder=encoder, routes=[chitchat_route, coding_route], auto_sync="local")

# Handler Functions
def call_groq_fast(prompt: str) -> str:
    """Routes to ultra-fast, lightweight Llama model on Groq."""
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"⚠️ Groq API Error: {e}. Falling back to Gemini.")
        return call_default_fallback(prompt)

def call_gemini_advanced(prompt: str) -> str:
    """Routes high-complexity tasks to Gemini 1.5 Flash."""
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error executing Gemini request: {e}"

def call_default_fallback(prompt: str) -> str:
    """General query fallback route."""
    return call_gemini_advanced(prompt)

def execute_routed_query(prompt: str) -> dict:
    """Evaluates user intent and dispatches to optimal LLM provider."""
    route_decision = router(prompt)
    route_name = route_decision.name or "default"
    
    if route_name == "chitchat":
        response = call_groq_fast(prompt)
        provider = "Groq (llama-3.1-8b-instant)"
    elif route_name == "coding":
        response = call_gemini_advanced(prompt)
        provider = "Google Gemini (gemini-1.5-flash)"
    else:
        response = call_default_fallback(prompt)
        provider = "Google Gemini [Fallback]"

    return {
        "prompt": prompt,
        "route": route_name,
        "provider": provider,
        "response": response
    }