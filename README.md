# ⚡ Semantic LLM Router

An intelligent, low-latency LLM routing engine built with **Semantic Router**, **Google Gemini**, and **Groq**.

This project evaluates prompt intent at runtime using semantic vector embeddings, routing lightweight queries to ultra-fast models and complex reasoning/coding prompts to heavier models.

---

## 🎯 Key Features

* **Intent-Based Routing:** Uses cosine similarity on prompt embeddings to route requests without extra LLM overhead.
* **Cost & Latency Optimization:** Directs simple queries to fast models (Groq / Llama 3) and complex queries to larger models (Gemini 1.5 Flash).
* **Automatic Fallback:** Includes error handling to default back to primary LLMs if a service call fails.

---

## 🛠️ Architecture Overview

```
                    ┌──────────────────┐
                    │   User Prompt     │
                    └────────┬──────────┘
                             │
                             ▼
                 ┌───────────────────────┐
                 │ Semantic Route Layer  │
                 │ (GoogleGeckoEncoder)  │
                 └──────────┬────────────┘
                             │
    ┌────────────────────────┼───────────────────────┐
    │ [Intent: Chitchat]     │ [Intent: Coding]       │ [Intent: Fallback]
    ▼                        ▼                        ▼
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│  Groq API    │        │  Gemini API  │        │  Gemini API  │
│ (Llama-3.1)  │        │ (1.5-Flash)  │        │ (Fallback)   │
└──────────────┘        └──────────────┘        └──────────────┘
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/DarshanBhabad/SLR_-semantic_LLM_routing-.git
cd semantic-llm-router
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure API Keys
Copy `.env.example` to `.env` and add your free tier API keys:
```bash
cp .env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY="your_gemini_api_key_here"
GROQ_API_KEY="your_groq_api_key_here"
```

You can get free API keys here:
- Gemini: https://aistudio.google.com/apikey
- Groq: https://console.groq.com/keys

### 4. Run the Demo
```bash
python -m src.main
```

---

## 🧪 Example Output

```
--- Test 1 ---
User Prompt   : Hey buddy! What's up? Can you tell me a quick pun?
Route Selected: chitchat
Provider Used : Groq (llama-3.1-8b-instant)
AI Response   : Why don't scientists trust atoms? Because they make up everything!

--- Test 2 ---
User Prompt   : Can you write an optimized recursive function in Python for Fibonacci?
Route Selected: coding
Provider Used : Google Gemini (gemini-1.5-flash)
AI Response   : Here is an optimized Fibonacci function using memoization...
```

---

## 📂 Project Structure

```
semantic-llm-router/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
    ├── config.py
    ├── router.py
    └── main.py
```

---

## 📜 License

MIT
