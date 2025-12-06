# Elfactory

Multi-agent Christmas gift workshop powered by Datapizza-AI.

Sistema multi-agente natalizio: 28 elfi AI lavorano come veri artigiani per costruire regali richiesti via email. Include generazione immagini AI del prodotto finito e approvazione finale di Babbo Natale.

**Challenge:** #madewithdatapizzaai - Datapizza Community Christmas Challenge

## Quick Start

```bash
git clone <repo-url>
cd Elfactory
cp .env.example .env
```

Edit `.env` and add your `OPENAI_API_KEY`

```bash
uv sync
uv run python scripts/run_workshop.py
```

## Architecture

- **28 AI Agents** organized in 4 tiers
- **Tier 0:** Santa Claus (Final Approver)
- **Tier 1:** 5 Manager Elves (Reception, Design, Production, Quality, Logistics)
- **Tier 2:** 22 Artisan Elves (Material workers, Assembly team, Finishing artists, Specialists)
- **Tier 3:** 3 Support Agents (Online Shopper, Image Generator, Response Composer)

## Tech Stack

- **Framework:** Datapizza-AI v0.0.9
- **LLM:** OpenAI GPT-4
- **Image Generation:** TBD (Gemini/Banana Pro)
- **Monitoring:** OpenTelemetry + ContextTracing

## Project Status

🚧 Work in Progress
