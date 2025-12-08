```
     _____ _  __            _
    | ____| |/ _| __ _  ___| |_ ___  _ __ _   _
    |  _| | | |_ / _` |/ __| __/ _ \| '__| | | |
    | |___| |  _| (_| | (__| || (_) | |  | |_| |
    |_____|_|_|  \__,_|\___|\__\___/|_|   \__, |
                                          |___/
          🎄 AI-Powered Gift Workshop 🎅
```

Multi-agent Christmas gift workshop powered with Datapizza-AI.

26 AI elves work autonomously to manufacture gifts requested via email, with AI-generated images and Santa's final approval.

**Challenge:** #madewithdatapizzaai - Datapizza Community Christmas Challenge

## Setup

### 1. Install

```bash
git clone <repo-url>
cd Elfactory
uv sync
```

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env`:
```bash
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-5-mini
```

### 3. Test (Recommended)

Test the workflow without Gmail:

```bash
# Optional: customize test email
export TEST_RECIPIENT_EMAIL="your-email@gmail.com"
export TEST_EMAIL_CONTENT="Caro Babbo Natale, vorrei un drone..."

# Run test
uv run python scripts/test_workflow.py
```

The test will:
- Process the gift request through all 26 agents
- Create components and manufacturing log
- Generate AI image of the finished gift
- Send response email (if `TEST_RECIPIENT_EMAIL` is set)
- Verify workflow completion

Expected result: `TEST RESULT: ✓ PASSED`

### 4. Production (Optional - Gmail Integration)

For automatic email monitoring:

1. **Setup Gmail API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create project → Enable Gmail API → Create OAuth2 credentials (Desktop app)
   - Download `credentials.json` to project root

2. **Authenticate:**
   ```bash
   uv run python scripts/setup_gmail.py
   ```

3. **Start monitor:**
   ```bash
   uv run python scripts/monitor_emails.py
   ```

4. **Send test email** with subject containing "letterina"

## How It Works

**26 AI Agents** collaborate autonomously to process gift requests:

1. **Reception Manager** → extracts child info
2. **Design Manager** → decides manufacture vs. online purchase
3. **Production Manager** → delegates to 19 artisan elves (3D printer, woodworker, electronics, etc.)
4. **Quality Manager** → safety inspection
5. **Logistics Manager** → packaging
6. **Image Prompt Generator** → creates DALL-E prompt
7. **Santa Claus** → final approval
8. **Response Composer** → sends email with gift image

## Output

Each workflow generates:
- `logs/elfactory_YYYYMMDD_HHMMSS.log` - Detailed agent logs
- `logs/images/{GIFT_ID}.png` - AI-generated gift image (DALL-E 3)
- `logs/reports/{GIFT_ID}_report.md` - Manufacturing report

## Tech Stack

- **Framework:** Datapizza-AI
- **LLM:** OpenAI GPT-4o-mini
- **Image:** DALL-E 3
- **Email:** Gmail API (optional)

