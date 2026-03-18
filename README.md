 # 🔍 Multi-Source Research Agent

> Research anything — instantly. Google + Bing + Reddit, analyzed in parallel and synthesized into one clean answer.

---

## What Is This?

A **LangGraph-powered AI research agent** that runs three searches simultaneously, pulls real Reddit discussions, and combines everything into one comprehensive answer — all through a clean dark web UI.

Ask it *"Is Rust worth learning in 2025?"* and it will search Google, crawl Bing, dive into Reddit threads, analyze all of it, and hand you back a synthesized answer in one shot.

---

## ✨ Features

↪ Parallel search across **Google**, **Bing**, and **Reddit** at the same time  
↪ Automatically picks the most relevant Reddit threads and fetches full comment sections  
↪ Each source is analyzed independently, then **synthesized** into one final answer  
↪ Beautiful **dark web UI** with live stage indicators and smooth animations  
↪ Powered by **Gemini 2.5 Flash** via LangChain  
↪ Data sourced through **BrightData SERP & Dataset APIs**  
↪ Flask backend connects `app.py` → `templates/index.html` seamlessly  
↪ No conversation memory — every query is a clean, focused research session  

---

## 🗂️ File Structure

| File | Role |
|------|------|
| `app.py` | Flask server — receives questions from the UI, runs the agent, returns the answer |
| `main.py` | Core LangGraph agent — defines all nodes, state, and the full research graph |
| `prompts.py` | All LLM prompt templates for Google analysis, Bing analysis, Reddit analysis, and synthesis |
| `web_operations.py` | BrightData API calls — SERP search (Google/Bing) and Reddit search + post retrieval |
| `snapshot_operations.py` | Polls BrightData snapshot jobs until ready, then downloads the result |
| `templates/index.html` | Full frontend — dark UI chat page served by Flask |
| `.env` | Your API keys — `GEMINI_API_KEY` and `BRIGHTDATA_API_KEY` |

---

## 🧠 How It Works

```
User Question
     │
     ├──▶ Google Search ──▶ ┐
     ├──▶ Bing Search   ──▶ ├──▶ Pick Best Reddit URLs ──▶ Fetch Reddit Posts
     └──▶ Reddit Search ──▶ ┘
                                        │
                          ┌─────────────┼─────────────┐
                          ▼             ▼             ▼
                   Analyze Google  Analyze Bing  Analyze Reddit
                          └─────────────┼─────────────┘
                                        ▼
                                  Synthesize All
                                        │
                                   Final Answer
```

---

## ⚙️ Setup

**1. Clone and install**
```bash
git clone https://github.com/yourname/research-agent.git
cd research-agent
pip install flask langgraph langchain langchain-google-genai python-dotenv requests
```

**2. Add your keys**
```env
# .env
GEMINI_API_KEY=your_gemini_key_here
BRIGHTDATA_API_KEY=your_brightdata_key_here
```

**3. Run**
```bash
python app.py
```
Open **http://localhost:5000** — that's it.

---

## 💬 Example Queries

```
↪ "What are the best Python libraries for data science in 2025?"
↪ "Is the M4 MacBook Pro worth buying?"
↪ "How does LangGraph differ from LangChain?"
↪ "What do developers actually think about Rust?"
↪ "Best free alternatives to Notion?"
```

---

## 🔌 UI ↔ Backend Connection

```
Browser (index.html)
   └── POST /research  { "question": "..." }
           │
        app.py  (Flask)
           └── graph.invoke(state)
                   │
                main.py  (LangGraph)
                   └── returns { "final_answer": "..." }
           │
   Browser receives JSON and renders the answer
```

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | Gemini 2.5 Flash via LangChain |
| Agent Framework | LangGraph |
| Web Data | BrightData SERP + Dataset API |
| Backend | Flask |
| Frontend | Vanilla HTML / CSS / JS |

---

## 📁 Required Project Structure

```
research_agent/
├── app.py
├── main.py
├── prompts.py
├── web_operations.py
├── snapshot_operations.py
├── .env
└── templates/
    └── index.html
```

> ⚠️ `index.html` **must** live inside the `templates/` folder — Flask's `render_template()` requires it.

---<img width="1076" height="789" alt="Screenshot 2026-03-18 102418" src="https://github.com/user-attachments/assets/64fa66f5-52fc-4bd8-b905-3134177ecebd" />


