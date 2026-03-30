# 🎓 AI Alumni Data Extractor

An intelligent automation system for collecting, validating, and structuring alumni data from LinkedIn profiles.

## ⚡ Quick Start

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your API keys
```

### 4. Launch Web UI (Recommended)

```bash
# Windows
run_ui.bat

# macOS/Linux
./run_ui.sh

# Or manually:
streamlit run ui/app.py
```

The web interface will open at: **http://localhost:8501**

### 5. (Optional) Run Command-Line Setup Test

```bash
python src/main.py
```

## Project Structure

```
alumni-extractor/
├── config/              # Configuration management
├── src/                 # Source code
│   ├── search/         # Google search integration
│   ├── scraper/        # LinkedIn scraper
│   ├── ai/             # AI validation
│   ├── data/           # Data processing
│   ├── export/         # CSV export
│   ├── utils/          # Utilities
│   └── main.py         # Entry point
├── tests/              # Unit tests
├── output/             # Generated CSV files
├── logs/               # Application logs
└── requirements.txt    # Dependencies
```

## API Keys Needed

1. **SerpAPI** - Google search automation
2. **OpenAI** - Data validation using GPT
3. **LinkedIn** - Email and password for authentication

## Documentation

See `AI_Alumni_Data_Extractor.md` for complete documentation.

## Development Phases

- [x] Phase 1: Environment Setup ✓
- [ ] Phase 2: Google Search Integration
- [ ] Phase 3: LinkedIn Scraper (Playwright)
- [ ] Phase 4: Profile Data Extraction
- [ ] Phase 5: AI Data Structuring
- [ ] Phase 6: Data Cleaning & Deduplication
- [ ] Phase 7: CSV Export
- [ ] Phase 8: Optional Enhancements

## License

MIT License
