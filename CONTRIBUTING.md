# Contributing to Automatejobs.ia

Thank you for your interest in contributing! This platform aims to democratize access to automation intelligence for everyone.

## How to Contribute

### Reporting Issues
- Use GitHub Issues for bug reports and feature requests
- Include steps to reproduce for bugs
- For feature requests, describe the use case and value

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly (backend: `pytest`, frontend: `yarn test`)
5. Open a PR with a clear description

### Areas Where Help is Needed

**Data Quality:**
- Adding new occupations to `backend/database/seed_data/`
- Updating automation scores based on latest AI capabilities
- Expanding to new industries

**Regulatory Updates:**
- Adding new jurisdictions (Australia, UK, Singapore, etc.)
- Updating existing regulations as they evolve
- Adding compliance rules for new automation types

**Frontend:**
- New visualizations and charts
- Accessibility improvements (WCAG 2.1 AA)
- Mobile responsiveness
- Performance optimization

**Translations:**
- French (Quebec market)
- Spanish (Latin America)
- German (EU market)

### Development Setup

See [README.md](README.md) for setup instructions.

### Code Standards

**Backend (Python):**
- PEP 8 style (enforced by `black` + `flake8`)
- Type hints on all public functions
- Docstrings for all endpoints
- Tests for new endpoints

**Frontend (React):**
- Functional components only
- Custom hooks for data fetching
- Tailwind CSS for styling
- Radix UI for accessibility

### Commit Message Format
```
type(scope): short description

Examples:
feat(backend): add GDPR compliance check for email automation
fix(frontend): fix occupation search not filtering by industry
docs: update API reference for /roi/calculate endpoint
data: add 5 new Healthcare occupations with automation scores
```

## Data Format

To add new occupations, see `backend/database/seed_data/README.md` for the data format and submission process.

## Questions?

Open a GitHub Discussion or reach out via the Issues page.
