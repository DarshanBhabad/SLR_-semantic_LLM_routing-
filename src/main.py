from src.config import GEMINI_API_KEY, GROQ_API_KEY
from src.router import execute_routed_query

def run_demo():
    test_prompts = [
        "Hey buddy! What's up? Can you tell me a quick pun?",
        "Can you write an optimized recursive function in Python for Fibonacci?",
        "What is the capital city of France?"
    ]

    for idx, prompt in enumerate(test_prompts, start=1):
        print(f"\n--- Test {idx} ---")
        result = execute_routed_query(prompt)
        print(f"User Prompt : {result['prompt']}")
        print(f"Route Selected: {result['route']}")
        print(f"Provider Used : {result['provider']}")
        print(f"AI Response  : {result['response']}\n")

if __name__ == "__main__":
    run_demo()