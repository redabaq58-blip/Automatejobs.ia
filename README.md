# Automatejobs.ia

**Enterprise-grade platform for building compliant AI agents and automations with deep industry knowledge — no experience required.**

Built for indie hackers, developers, and non-technical people who want to automate jobs and workflows with AI, with full compliance for USA, Canada, and Europe.

---

## What Is This?

Automatejobs.ia democratizes the creation of enterprise AI agents and automations. It combines:

- **29 occupations** across 20 industries with full cross-mapping (O*NET + NOC 2026 + ESCO)
- **39 atomic tasks** with deterministic automation scores (no hallucination — pure formulas)
- **156 automation scores** across 4 jurisdictions (USA, Canada, EU, Quebec)
- **35 skills** tracked with decay predictions and 22 reskilling pathways
- **15 regulatory jurisdictions** forecasted through 2030 (EU AI Act, Quebec Law 25, CNESST, California, Singapore + more)
- **15 AI tools** in the vendor intelligence database
- **15 labor arbitrage opportunities** with urgency scores and wage trends
- **8 first-mover automation windows** with competitive advantage data
- **85+ API endpoints** for all intelligence data
- **AI Builder Studio** — guided 7-step wizard to generate full automation blueprints

Anyone — from indie hackers to Fortune 500 enterprises — can build compliant, production-ready AI automations without knowing anything about the target industry.

---

## How to Use the Platform

### Step 1 — Explore the Intelligence Dashboard

The left sidebar has 8 intelligence pages. Start here to understand what's automatable in your industry.

| Page | What to do |
|------|-----------|
| **Executive Dashboard** | Get a top-level view — jobs at risk, most disrupted industries, quick wins, first-mover windows closing soon |
| **Occupation Explorer** | Search for a job role (e.g. "Accountant", "Nurse"). Click a row to see all its tasks, automation scores, and compliance status |
| **Skills Intelligence** | See which skills are decaying fastest (Data Entry has a 2-year half-life). Browse 22 reskilling pathways with ROI |
| **Regulatory Compliance** | Check what's blocked or restricted in your jurisdiction. EU AI Act blocks some tasks entirely — know before you build |
| **Industry Intelligence** | See how automated your industry already is. Financial Services leads at 72/100 maturity |
| **ROI Calculator** | Enter a salary + automation % → get exact payback months, Year 1 ROI %, and Year 3 savings |
| **Vendor Intelligence** | Browse 15 AI tools by category (RPA, LLM, Document AI). Compare TCO, failure rates, and tech radar status |
| **Labor Arbitrage** | Find which occupations have the highest urgency to automate now before wage costs outpace ROI |

### Step 2 — Build an Automation with the AI Wizard

Click **"Build"** in the sidebar to open the AI Builder Studio.

1. **Start Building** — Pick a quick-win card or browse by industry
2. **AI Wizard (7 steps)**:
   - Step 1: Choose your **Industry** (e.g. Finance, Healthcare, Manufacturing)
   - Step 2: Select **Tasks** to automate (e.g. Invoice Processing, Data Entry)
   - Step 3: Review **Compliance** constraints for your jurisdiction
   - Step 4: Choose **AI Tools** from the vendor recommendations
   - Step 5: Review **ROI** projections and payback timeline
   - Step 6: Get a full **Automation Blueprint** (copy/download)
   - Step 7: Save to **My Blueprints**

3. **AI Assistant** — Ask any automation question in plain English. Examples:
   - *"What can I automate in my accounting firm?"*
   - *"Is resume screening legal in the EU?"*
   - *"What's the ROI for automating invoice processing?"*

> **Tip:** To enable the AI Assistant with real LLM responses, add an `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` to your `.env` file. Without a key it uses smart keyword-based responses.

### Step 3 — Use the API Directly

All intelligence data is available via REST API. Browse the full interactive docs at `http://localhost:8001/docs`.

```bash
# Search occupations
curl "http://localhost:8001/api/occupations?query=accountant"

# Get automation scores for a task
curl "http://localhost:8001/api/tasks/high-automation?min_score=80"

# Get all 20 industries ranked by maturity
curl "http://localhost:8001/api/intelligence/all-industries"

# Get first-mover windows (urgent automations)
curl "http://localhost:8001/api/intelligence/first-mover-windows"

# Calculate custom ROI
curl -X POST "http://localhost:8001/api/roi/calculate" \
  -H "Content-Type: application/json" \
  -d '{"annual_salary": 55000, "automation_percentage": 0.75, "implementation_cost": 8000, "ongoing_annual_cost": 2400, "jurisdiction": "USA-Federal"}'
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+ with Yarn

### Development

```bash
git clone https://github.com/redabaq58-blip/Automatejobs.ia
cd Automatejobs.ia

# Start backend (auto-seeds database on first run)
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
# API docs: http://localhost:8001/docs

# Start frontend (new terminal)
cd frontend
yarn install
REACT_APP_BACKEND_URL=http://localhost:8001 yarn start
# App: http://localhost:3000
```

### Docker (Recommended)

```bash
cp .env.example .env
# Edit .env and set REACT_APP_BACKEND_URL if needed
docker-compose up --build
# Frontend: http://localhost
# Backend API: http://localhost:8001/docs
```

### Environment Variables (Optional)

```bash
# .env
REACT_APP_BACKEND_URL=http://localhost:8001

# Enable AI Assistant with real LLM (optional — falls back to deterministic)
ANTHROPIC_API_KEY=sk-ant-...       # Claude Haiku (recommended)
OPENAI_API_KEY=sk-...              # GPT-4o-mini (alternative)
```

---

## How to Merge Pending Changes

The branch `claude/clone-automateJobs-repo-VJABF` is **3 commits ahead of `main`**:

| Commit | What it adds |
|--------|-------------|
| `e5d2e14` | ROI Calculator, Vendor Intelligence, Labor Arbitrage pages |
| `1f888f8` | `.gitignore` (excludes pycache, node_modules, build artifacts) |
| `d74c87e` | Full platform data reflected in dashboard KPIs + AI assistant |

### Option A — Merge via GitHub (Recommended)

1. Go to your repo on GitHub: **redabaq58-blip/Automatejobs.ia**
2. You'll see a banner: **"claude/clone-automateJobs-repo-VJABF had recent pushes"**
3. Click **"Compare & pull request"**
4. Set base: `main`, compare: `claude/clone-automateJobs-repo-VJABF`
5. Title: `Complete platform — ROI, Vendors, Arbitrage pages + full data coverage`
6. Click **"Create pull request"** → then **"Merge pull request"**

### Option B — Merge via Git CLI

```bash
git checkout main
git pull origin main
git merge claude/clone-automateJobs-repo-VJABF
git push origin main
```

After merging, `main` will have the complete platform with all 8 Intelligence pages and all data correctly represented.

---

## Platform Sections

### Intelligence Dashboard (Explore)
| Page | Route | Description |
|------|-------|-------------|
| Executive Dashboard | `/` | KPIs, industry disruption chart, first-mover windows |
| Occupation Explorer | `/occupations` | Search 29 occupations, browse tasks with automation scores |
| Skills Intelligence | `/skills` | Skills decay, 22 reskilling pathways, workforce impact |
| Regulatory Compliance | `/regulatory` | Timeline 2026-2030, 15 jurisdictions, EU blocked tasks |
| Industry Intelligence | `/industries` | 20 industries ranked by automation maturity |
| ROI Calculator | `/roi` | Interactive calculator + 39 pre-built task ROI analyses |
| Vendor Intelligence | `/vendors` | 15 AI tools, TCO analysis, failure rates, tech radar |
| Labor Arbitrage | `/arbitrage` | Urgency scores, adoption velocity by company size |

### AI Builder Studio (Build)
| Page | Route | Description |
|------|-------|-------------|
| Start Building | `/build` | Quick-win cards and industry browser |
| AI Wizard | `/build/wizard` | 7-step guided flow: Industry → Tasks → Compliance → Tools → ROI → Blueprint |
| My Blueprints | `/build/blueprints` | Saved automation blueprints |
| AI Assistant | `/build/assistant` | Conversational AI for automation questions |

---

## Automation Scoring Methodology

Scores are **deterministic** — no LLM randomness. The formula combines:

1. **Digital Feasibility** (0-100) — Is the task digital? Structured? Repetitive?
2. **Cognitive Routine Index** (0-100) — How predictable is the task?
3. **Compliance Penalty** (0-1) — Jurisdiction-specific risk multiplier
4. **Final Score** = (digital × 0.5) + (cognitive × 0.3) + (prior_art × 0.2) × compliance_penalty

**Score Tiers:**
| Score | Tier | Action |
|-------|------|--------|
| 86-100 | Full automation | Implement now |
| 61-85 | High potential | Strong ROI — prioritize |
| 31-60 | Partial / HITL | Human-in-the-loop required |
| 0-30 | Cannot automate | Human required |

---

## Compliance Coverage

| Jurisdiction | Framework | Coverage |
|-------------|-----------|----------|
| USA Federal | EEOC, CFPB, FTC, State AI laws | Full |
| Canada Federal | PIPEDA, AIDA | Full |
| European Union | EU AI Act (2024), GDPR | Full |
| Quebec | Law 25, CNESST, OIQ, Barreau | Full |
| California | CPRA, AB 2013 | Forecasted 2026-2028 |
| New York | Local Law 144, SHIELD Act | Forecasted |
| Singapore, Australia, Japan, UK, Brazil, India, China | National AI frameworks | Forecasted through 2030 |

---

## API Reference

85+ REST endpoints. Interactive docs: `http://localhost:8001/docs`

| Category | Prefix | Examples |
|----------|--------|---------|
| Occupations & Tasks | `/api/occupations`, `/api/tasks` | Search, filter, automation scores |
| Intelligence | `/api/intelligence/` | Industries, skills, labor arbitrage, first-mover windows |
| Regulatory | `/api/regulatory/` | Timeline, jurisdictions, blocked tasks |
| ROI & TCO | `/api/roi/` | Calculator, benchmarks, pre-built analyses |
| Vendors | `/api/vendors/` | AI tools, TCO, failure rates, tech radar |
| AI Builder | `/api/ai/` | Chat, blueprints, wizard steps |

---

## Architecture

```
Automatejobs.ia/
├── backend/                   # FastAPI + SQLAlchemy
│   ├── server.py              # 85+ API endpoints
│   ├── database/
│   │   ├── models.py          # Star schema ORM models
│   │   ├── db_manager.py      # Connection + seeding
│   │   ├── seed_data.py       # 12 occupations, 17 tasks
│   │   ├── seed_data_extended.py  # 17 more occupations, 22 tasks
│   │   ├── tier1_intelligence.py  # 9 industries, skills decay, ROI intel
│   │   ├── tier1_expansion.py     # 12 more industries, 25 skills, TCO
│   │   ├── proprietary_data.py    # 15 AI tools, salary benchmarks
│   │   ├── tier1_queries.py       # Intelligence query functions
│   │   └── proprietary_queries.py # ROI + vendor query functions
│   └── requirements.txt
├── frontend/                  # React 19 + Tailwind + Radix UI
│   ├── src/
│   │   ├── pages/             # 12 dashboard pages (8 intelligence + 4 builder)
│   │   ├── components/        # Layout, shared components, 47 Radix UI primitives
│   │   └── lib/api.js         # Centralized Axios API client
│   └── package.json
├── docker-compose.yml         # Full-stack deployment
├── .env.example               # Environment variables template
└── README.md
```

---

## Cloud Deployment

**Backend (Python/FastAPI):**
- Runtime: Python 3.11
- Install: `pip install -r requirements.txt`
- Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- Health check: `GET /api/`
- No database setup needed (SQLite auto-seeded on first run)

**Frontend (React/Static):**
- Build: `yarn build`
- Serve: nginx, Vercel, Netlify, or any static host
- Required env: `REACT_APP_BACKEND_URL=https://your-backend-url.com`
- SPA routing: serve `index.html` for all 404s

---

## License

MIT License — free to use, modify, and distribute.

---

## Data Sources & Acknowledgments

- **O*NET v30.2** — US Occupational Information Network (US Department of Labor)
- **NOC 2026.1** — National Occupational Classification (Employment and Social Development Canada)
- **ESCO 1.2** — European Skills, Competences, Qualifications and Occupations (EU Commission)
- **Frey & Osborne (2013)** — "The Future of Employment" automation probability research
- **EU AI Act** — Regulation (EU) 2024/1689
