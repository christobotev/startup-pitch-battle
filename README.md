# 🚀 Startup Pitch Variations Battle

**Startup Pitch Variations Battle** is an AI-powered project that generates, tests, and refines multiple startup pitch drafts in a _battle-style workflow_.  
The goal: find the strongest pitch variation through structured competition, scoring, and iteration.

---

## 🎯 Project Goals

- Generate multiple pitch variations from a single idea.
- Run "battles" where pitches are compared against one another.
- Score pitches based on clarity, persuasiveness, and investor appeal.
- Refine winning variations iteratively until the best version emerges.

---

## 🛠️ How It Works

1. **Idea Input** → Provide a startup idea or concept.
2. **Variation Generation** → An AI agent creates multiple pitch versions.
3. **Battle Mode** → Other agents compare and score the variations.
4. **Winner Advancement** → The top pitch moves forward for refinement.
5. **Iteration** → Repeat the process until the strongest pitch emerges.

---

## 📂 Project Structure

startup-pitch-battle/
│
├── agents/ # Agent definitions (generator, evaluator, refiner)
├── workflows/ # Battle workflow logic
├── app/ # API/UI code
├── docker-compose.yml # Multi-container setup
├── Dockerfile # Container build instructions
├── requirements.txt # Python dependencies
└── README.md # Project documentation

---

## ⚙️ Tech Stack

- [Python 3.11+](https://www.python.org/)
- [CrewAI](https://github.com/joaomdmoura/crewai) or [OpenAI Agents SDK](https://github.com/openai/openai-python)
- Docker
- OpenAI / Gemini/Chatgpt models for pitch generation and evaluation
- Git
- [Docker Compose](https://docs.docker.com/compose/)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/startup-pitch-battle.git
cd startup-pitch-battle
```

### 2. Create a virtual env

```bash
python3 -m venv venv
source venv/bin/activate   # on Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt    #in the venv
```

### 4. Run the container

```bash
docker compose up --build
```

### 5. Open in browser

Go to http://localhost:5002/

⭐ Why This Project?

Crafting a startup pitch is part art, part science.
This project uses AI tournament dynamics to make it systematic: let your ideas battle it out until only the best survives.
Better results if you use different LLM's per variation.

You can see it running (based on my VPS availablity) at https://sp.botevllc.com
