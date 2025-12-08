# Elfactory

Multi-agent Christmas gift workshop powered with Datapizza-AI.

Sistema multi-agente natalizio: 26 elfi AI lavorano come veri artigiani per costruire regali richiesti via email. Include generazione immagini AI del prodotto finito e approvazione finale di Babbo Natale.

**Challenge:** #madewithdatapizzaai - Datapizza Community Christmas Challenge

## Quick Start

### 1. Setup Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth2 credentials (Desktop app)
5. Download `credentials.json` to project root

### 2. Install and Configure

```bash
git clone <repo-url>
cd Elfactory
cp .env.example .env
```

Edit `.env` and add:
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL=gpt-4o-mini` - Or gpt-4
- Other settings as needed

### 3. Install Dependencies

```bash
uv sync
```

### 4. Authenticate Gmail

```bash
uv run python scripts/setup_gmail.py
```

This opens your browser to authenticate with Gmail. Authorize the app to read and modify emails.

### 5. Start Email Monitor

```bash
uv run python scripts/monitor_emails.py
```

The monitor will:
- Check for unread emails every 60 seconds
- Process emails with "letterina" in the subject
- Trigger the autonomous multi-agent workflow
- Mark processed emails as read

### 6. Send a Test Email

Send an email to your Gmail account with:
- **Subject:** Must contain "letterina"
- **Body:** A gift request from a child (name, age, what they want)

Example:
```
Ciao Babbo Natale, mi chiamo Marco, ho 8 anni.
Per Natale vorrei una macchinina telecomandata rossa.
```

## Architecture

### Agent Hierarchy (26 AI Agents)

**Tier 0: Final Approver**
- Santa Claus - Reviews and blesses all gifts

**Tier 1: Manager Elves (5)**
- Reception Manager - Receives and processes gift requests
- Design Manager - Analyzes feasibility and creates blueprints
- Production Manager - Coordinates artisan elves
- Quality Manager - Inspects safety and quality
- Logistics Manager - Handles packaging and gift cards

**Tier 2: Artisan Elves (19)**
- Material Workers: 3D Printer, Woodworker, Blacksmith, Fabric, Leather, Glass, Ceramics
- Assembly Team: Mechanic, Electronics, Battery, Welding
- Finishing Artists: Painter, Airbrush, Engraver, Polish, Decal
- Specialists: Sound Engineer, Light Designer, Software, Librarian

**Tier 3: Support Agents (3)**
- Online Shopper - Finds products that can't be manufactured
- Image Prompt Generator - Creates prompts for gift visualization
- Response Composer - Writes final email to child

### Autonomous Workflow

The workflow is fully autonomous using Datapizza-AI's `can_call()` delegation:

1. **Reception Manager** extracts child info → calls **Design Manager**
2. **Design Manager** decides feasibility → calls **Production Manager** or **Online Shopper**
3. **Production Manager** delegates to artisan elves → calls **Quality Manager**
4. **Quality Manager** inspects gift → calls **Logistics Manager**
5. **Logistics Manager** prepares packaging → calls **Image Prompt Generator**
6. **Image Prompt Generator** creates visualization prompt → calls **Santa Claus**
7. **Santa Claus** reviews and approves → calls **Response Composer**
8. **Response Composer** writes final email to child

## Tech Stack

- **Framework:** Datapizza-AI v0.0.9
- **LLM:** OpenAI GPT-4o-mini / GPT-4
- **Email:** Gmail API with OAuth2
- **Image Generation:** TBD (Gemini/Banana Pro) - prompt generation implemented
- **Monitoring:** OpenTelemetry + ContextTracing
- **State Management:** Pydantic models with ContextVar for thread-safety

## Features

- ✅ Autonomous multi-agent workflow
- ✅ Gmail API integration with email monitoring
- ✅ Structured state management
- ✅ OpenTelemetry tracing with token usage tracking
- ✅ Safety and quality checks
- ✅ Age-appropriate gift decisions
- ✅ Online shopping fallback for impossible gifts
- ✅ AI image generation with DALL-E 3
- ✅ Automatic email response delivery
- ✅ File logging system
- ✅ Manufacturing report generation

## Testing

Test the complete workflow end-to-end:

```bash
uv run python scripts/test_workflow.py
```

This will:
- Process a sample gift request (toy car for an 8-year-old)
- Execute the complete autonomous workflow
- Verify all stages complete successfully
- Show detailed output including components, manufacturing log, and final status

Expected output:
- Gift processed through all workflow stages
- Components created by artisan elves
- Quality inspection passed
- Santa's approval received
- Final response composed


## Output Files

The system generates the following outputs for each gift:

- **Logs:** `logs/elfactory_YYYYMMDD_HHMMSS.log` - Detailed workflow logs including agent interactions
- **Images:** `logs/images/{GIFT_ID}.png` - AI-generated gift visualization
- **Reports:** `logs/reports/{GIFT_ID}_report.md` - Complete manufacturing report with components and agents

