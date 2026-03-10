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
- **14 regulatory jurisdictions** forecasted through 2030 (EU AI Act, Quebec Law 25, CNESST)
- **85+ API endpoints** for all intelligence data
- **AI Builder Studio** — guided 7-step wizard to generate full automation blueprints

Anyone — from indie hackers to Fortune 500 enterprises — can build compliant, production-ready AI automations without knowing anything about the target industry.

---

## Platform Sections

### Intelligence Dashboard (Explore)
| Page | Description |
|------|-------------|
| Executive Dashboard | C-suite KPIs, disruption forecasts, quick wins |
| Occupation Explorer | Search 29 occupations, browse 39 tasks with automation scores |
| Skills Intelligence | Skills decay table, reskilling ROI, workforce impact |
| Regulatory Compliance | Timeline 2026-2030, 14 jurisdictions, EU blocked tasks |
| Industry Intelligence | 20 industries ranked by automation maturity |
| ROI Calculator | Interactive calculator + 39 pre-built task ROI analyses |
| Vendor Intelligence | AI tools catalog, TCO analysis, failure rates, tech radar |
| Labor Arbitrage | Automate-now urgency scores, adoption velocity |

### AI Builder Studio (Build)
| Page | Description |
|------|-------------|
| Start Building | Hero page with quick-win cards and industry browser |
| AI Wizard | 7-step guided flow: Industry -> Tasks -> Compliance -> Tools -> ROI -> Blueprint |
| My Blueprints | Saved automation blueprints (localStorage) |
| AI Assistant | Conversational AI for automation questions |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+ with Yarn

### Development

```bash
git clone https://github.com/your-org/automatejobs.ia
cd automatejobs.ia

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
docker-compose up --build
# Frontend: http://localhost
# Backend API: http://localhost:8001
# API Docs: http://localhost:8001/docs
```

---

## Cloud Deployment

### Render.com (One-Click)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/your-org/automatejobs.ia)

Click the button above to deploy both frontend and backend to Render's free tier.

### Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/...)

### Manual Cloud Deploy

The app has two services to deploy:

**Backend (Python/FastAPI):**
- Runtime: Python 3.11
- Install: `pip install -r requirements.txt`
- Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- Health check: `GET /api/`
- No database setup required (SQLite, auto-seeded)

**Frontend (React/Static):**
- Build: `yarn build`
- Serve: any static file server (nginx, Vercel, Netlify, S3+CloudFront)
- Set env var: `REACT_APP_BACKEND_URL=https://your-backend-url.com`
- SPA routing: serve `index.html` for all 404s

---

## API Reference

85+ REST endpoints. Interactive docs available at `/docs` when running.

### Key Endpoint Categories

| Category | Prefix | Description |
|----------|--------|-------------|
| Core Data | `/api/occupations` | Search occupations, tasks, compliance |
| ROI | `/api/roi/` | Salary benchmarks, ROI calculator |
| Tier 1 Intelligence | `/api/intelligence/` | 15 data categories |
| Builder | `/api/ai/` | AI chat, blueprint generation |

### Example Requests

```bash
# Get all occupations
curl http://localhost:8001/api/occupations?limit=10

# Get automation score for a task
curl http://localhost:8001/api/tasks/high-automation?min_score=80

# Executive dashboard
curl http://localhost:8001/api/intelligence/executive-dashboard

# Calculate ROI
curl -X POST http://localhost:8001/api/roi/calculate \
  -H "Content-Type: application/json" \
  -d '{"annual_salary": 55000, "automation_percentage": 0.75, "implementation_cost": 8000, "ongoing_annual_cost": 2400, "jurisdiction": "USA-Federal"}'
```

---

## Automation Scoring Methodology

Scores are **deterministic** — no LLM randomness. The formula combines:

1. **Digital Feasibility** (0-100) — Is the task digital? Structured? Repetitive?
2. **Cognitive Routine Index** (0-100) — How predictable is the task?
3. **Compliance Penalty** (0-1) — Jurisdiction-specific risk multiplier
4. **Final Score** = (digital x 0.5) + (cognitive x 0.3) + (prior_art x 0.2) x compliance_penalty

**Score Tiers:**
- 86-100: Full automation (implement now)
- 61-85: High potential (strong ROI)
- 31-60: Partial / HITL required
- 0-30: Cannot automate (human required)

---

## Compliance Coverage

| Jurisdiction | Framework | Status |
|-------------|-----------|--------|
| USA Federal | EEOC, FCRA, State AI laws | Full coverage |
| Canada Federal | PIPEDA, AIDA | Full coverage |
| European Union | EU AI Act (2024), GDPR | Full coverage |
| Quebec | Law 25, CNESST | Full coverage |

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

**Areas where help is needed:**
- Adding new occupations and tasks
- Updating regulatory information as laws evolve
- Adding new jurisdiction compliance rules
- UI improvements and new visualizations
- Translations (French, Spanish, German)
- Tests and documentation

---

## Architecture

```
automatejobs.ia/
├── backend/              # FastAPI + SQLAlchemy
│   ├── server.py         # 85+ API endpoints
│   ├── database/         # SQLite/PostgreSQL models + seed data
│   │   ├── models.py     # Star schema ORM models
│   │   ├── db_manager.py # Connection + migrations
│   │   ├── queries.py    # Core data queries
│   │   ├── tier1_queries.py # Intelligence queries
│   │   └── proprietary_queries.py # Scoring + ROI
│   └── requirements.txt
├── frontend/             # React 19 + Tailwind + Radix UI
│   ├── src/
│   │   ├── pages/        # 12 dashboard pages
│   │   ├── components/   # Layout + shared + Radix UI
│   │   └── lib/api.js    # Centralized API client
│   └── package.json
├── docker-compose.yml    # Full stack deployment
├── render.yaml           # Render.com one-click deploy
└── .env.example          # Environment variables
```

---

## License

MIT License — free to use, modify, and distribute.

See [LICENSE](LICENSE) for full text.

---

## Acknowledgments

Data sources:
- **O*NET** — US Occupational Information Network (US DOL)
- **NOC 2026** — National Occupational Classification (Employment and Social Development Canada)
- **ESCO** — European Skills, Competences, Qualifications and Occupations (EU Commission)
- **Frey & Osborne (2013)** — "The Future of Employment" automation probability research
- **EU AI Act** — Regulation (EU) 2024/1689
