# ApplyPilot AI — Streamlit Job Assistant 🚀

> **AI assistant for smarter job applications using Streamlit**

![ApplyPilot AI Demo](Screenshot%202026-07-10%20111732.png)

ApplyPilot AI is an intelligent job application assistant that reads your CV and a job description, then automatically performs a skills gap analysis, writes a tailored cover letter, generates interview prep questions, and tracks every application you save — all from a clean Streamlit UI.

---

## Features

| Feature | Description |
|---|---|
| 📄 **CV Upload** | Upload your CV as a PDF — text is extracted automatically and persists across the session |
| 🎯 **Skills Gap Analysis** | Matching skills, missing skills, and a hire-ability recommendation |
| ✉️ **Cover Letter Generator** | Professional, role-tailored cover letter (300–400 words) |
| 🎤 **Interview Prep** | 10 questions (technical + behavioural + gap-focused) with answer hints |
| 💾 **Application Tracker** | SQLite-backed tracker storing skills analysis, cover letter, and interview questions per application |
| 🔁 **Provider-Agnostic LLM** | Switch between Anthropic Claude and OpenAI GPT via a single env variable |

---

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — UI framework
- **[LangChain](https://python.langchain.com/)** — Agent orchestration & tool calling
- **[Anthropic Claude](https://www.anthropic.com/) / [OpenAI GPT](https://openai.com/)** — LLM backend
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** — PDF text extraction
- **SQLite** (stdlib `sqlite3`) — Local application tracking
- **python-dotenv** — Environment variable management

---

## Project Structure

```
ApplyPilot-ai-streamlit/
├── app.py                        # Main page — analysis & save form
├── config.py                     # LLM provider factory
├── requirements.txt
├── .env.example                  # Environment variable template
├── .streamlit/
│   └── config.toml               # Streamlit theme & upload settings
├── agent/
│   └── job_agent.py              # LangChain AgentExecutor
├── db/
│   └── database.py               # SQLite schema & CRUD
├── tools/
│   ├── pdf_extractor.py          # PDF → plain text
│   ├── skill_analyzer.py         # analyze_skills tool
│   ├── cover_letter.py           # generate_cover_letter tool
│   └── interview_questions.py    # create_interview_questions tool
└── pages/
    └── 2_My_Applications.py      # Application tracker page
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/Applypilot-ai-streamlit.git
cd Applypilot-ai-streamlit
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.example .env
```

```env
LLM_PROVIDER=anthropic        # or openai

ANTHROPIC_API_KEY=sk-ant-...  # required when LLM_PROVIDER=anthropic
OPENAI_API_KEY=sk-...         # required when LLM_PROVIDER=openai
```

The app will show a clear error on startup if the required API key is missing.

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## How to Use

1. **Upload your CV** — click *Browse files* in the sidebar and select your PDF. The CV stays loaded for the whole session; use the *Clear CV* button to swap it out.
2. **Paste a job description** — copy the full posting into the text area.
3. **Click "Analyze & Generate"** — the agent calls all three tools and returns:
   - Skills gap analysis (matching skills, gaps, recommendation)
   - Tailored cover letter
   - 10 interview questions with answer hints
4. **Save the application** — fill in the job title, company, URL, deadline, and status, then click *Save Application*. All three outputs are saved separately.
5. **Track applications** — navigate to **My Applications** in the sidebar to view, update status, or delete saved entries. Each entry shows the stored skills analysis, cover letter, and interview questions.

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `LLM_PROVIDER` | No | `anthropic` | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | If using Anthropic | — | Your Anthropic API key |
| `OPENAI_API_KEY` | If using OpenAI | — | Your OpenAI API key |

---

## License

MIT
