# 📺 Frontend Interface Visual Guide

## Main Layout

```
┌──────────────────────────────────────────────────────────────────────────┐
│  🎓 Alumni Data Extractor                                  🔄 Refresh    │
│  Extract, validate, and structure LinkedIn alumni data automatically    │
└──────────────────────────────────────────────────────────────────────────┘

┌─ SIDEBAR ──────────────┐  ┌─────────────────────────────────────────────┐
│ ⚙️ Configuration      │  │                TAB NAVIGATION                │
│                        │  ├─────────────────────────────────────────────┤
│ College Name:         │  │ 🚀 Extraction | 📊 Results | 📈 Analytics  │
│ [Your College______] │  │ ℹ️ About                                    │
│                        │  ├─────────────────────────────────────────────┤
│ Batch Year:          │  │                                               │
│ [2020▼]              │  │   ACTIVE TAB CONTENT                          │
│                        │  │   (Changes based on selected tab)            │
│ Search Pages:        │  │                                               │
│ [====5====]          │  │                                               │
│                        │  │                                               │
│ Request Delay:       │  │                                               │
│ [==2 sec==]          │  │                                               │
│                        │  │                                               │
├────────────────────────┤  │                                               │
│ API Status:          │  │                                               │
│ ✓ SerpAPI            │  │                                               │
│ ✓ OpenAI             │  │                                               │
│ ✓ LinkedIn           │  │                                               │
│                        │  │                                               │
│ [🔄 Refresh Config] │  │                                               │
└────────────────────────┘  └─────────────────────────────────────────────┘
```

---

## TAB 1: 🚀 Extraction Tab

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Start Alumni Data Extraction                                      │  x  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ This tool will:                                                         │
│ 1. Search LinkedIn profiles using Google                               │
│ 2. Scrape profile information with Playwright                          │
│ 3. Extract structured data from profiles                               │
│ 4. Validate data using AI (OpenAI/Gemini)                              │
│ 5. Clean and deduplicate records                                       │
│ 6. Export to CSV format                                                │
│                                                                           │
│ ⏱️  Estimated time: 5-30 minutes depending on profile count            │
│                                                                           │
│ Extraction Mode: [Demo (Sample Data)▼]                                 │
│ Max Profiles:    [100▼]                                                │
│                                                                           │
│ ┌─────────────────┐  ┌───────────────────────────────────────┐         │
│ │ ▶️ START        │  │ Status:                               │         │
│ │ EXTRACTION      │  │ Extraction Status:        Ready        │         │
│ │                 │  │ Last Run:                 Never        │         │
│ └─────────────────┘  │ Total Profiles:          0             │         │
│                      │ Success Rate:            0%            │         │
│                      └───────────────────────────────────────┘         │
│                                                                           │
│ [After click, shows progress:]                                         │
│                                                                           │
│ 📍 Searching LinkedIn profiles...                                      │
│ ████░░░░░░░░░░░░░░░░░░░░░░░░░░ 15%                                    │
│                                                                           │
│ Preview of Extracted Data                                             │
│ ┌─────────────────────────────────────────────────────────────┐         │
│ │ Name         │ Company  │ Position             │ University  │         │
│ ├─────────────────────────────────────────────────────────────┤         │
│ │ John Doe     │ Google   │ Software Engineer    │ MIT         │         │
│ │ Jane Smith   │ Microsoft│ Senior Engineer      │ Stanford    │         │
│ │ Robert J.    │ Amazon   │ Engineering Manager  │ Harvard     │         │
│ └─────────────────────────────────────────────────────────────┘         │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## TAB 2: 📊 Results Tab

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Extraction Results                                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  145            15          8            92.3                           │
│  Total Profiles Unique Cos Unique Unis  Avg Quality                    │
│                                                                           │
│ Filtering Options:                                                      │
│ ┌────────────────────────────────────────────────────────────────────┐   │
│ │ Min Quality Score: [━━━━━━━━━━━━━━━o━━━━━━━━]  0                  │   │
│ │ Filter by Company: [Select companies ▼]                           │   │
│ │                    ☐ Google  ☐ Microsoft  ☐ Amazon               │   │
│ │ Filter by Univ:    [Select universities ▼]                       │   │
│ │                    ☐ MIT  ☐ Stanford  ☐ Harvard                  │   │
│ └────────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│ Showing 145 of 145 profiles                                            │
│ ┌─────────────────────────────────────────────────────────────────────┐  │
│ │ name          url                  company     position              │  │
│ ├─────────────────────────────────────────────────────────────────────┤  │
│ │ John Doe      linkedin.com/in/j... Google      Software Engineer    │  │
│ │ Jane Smith    linkedin.com/in/j... Microsoft   Tech Lead            │  │
│ │ Robert Jo...  linkedin.com/in/r... Amazon      Manager              │  │
│ │ Sarah Miller  linkedin.com/in/s... Apple       Senior Engineer      │  │
│ │ [More rows...]                                                       │  │
│ └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│ [📥 Download CSV] [📥 Download JSON] [🔄 Clear Results]               │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## TAB 3: 📈 Analytics Tab

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Alumni Analytics                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ ┌────────────────────────────┐  ┌────────────────────────────┐          │
│ │ Top Companies              │  │ Top Universities           │          │
│ ├────────────────────────────┤  ├────────────────────────────┤          │
│ │ Google       ███████  28   │  │ MIT        ██████████████  30       │
│ │ Microsoft    ██████   24   │  │ Stanford   ███████████     23       │
│ │ Amazon       █████    21   │  │ Harvard    ██████████      20       │
│ │ Apple        ████     17   │  │ Berkeley   █████████       19       │
│ │ Meta         ███      14   │  │ Caltech    ████████        15       │
│ │ Tesla        ██       11   │  │ Duke       ███████         10       │
│ └────────────────────────────┘  └────────────────────────────┘          │
│                                                                           │
│ Graduation Year Distribution                                           │
│ ┌─────────────────────────────────────────────────────────────────────┐  │
│ │         35│                    ╱╲                                    │  │
│ │           │                   ╱  ╲                                   │  │
│ │         30│                  ╱    ╲                                  │  │
│ │           │                 ╱      ╲                                 │  │
│ │    Count  │                ╱        ╲        ╱╲                      │  │
│ │         25│               ╱          ╲      ╱  ╲                     │  │
│ │           │              ╱            ╲    ╱    ╲                    │  │
│ │         20│             ╱              ╲  ╱      ╲                   │  │
│ │           └──────────────────────────────╱────────╲──────────────────│  │
│ │            2010   2015   2020   2025                                 │  │
│ │                  Year                                                │  │
│ └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│ Quality Score Distribution                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐  │
│ │ Count  │     ╭╮                                                      │  │
│ │   40   │     ││                                                      │  │
│ │        │   ╱═╣╠═╲                                                    │  │
│ │   30   │   │ ║║ │                                                    │  │
│ │        │ ╭─░▓░─╮                                                     │  │
│ │   20   │ │░▓▓▓░│                                                     │  │
│ │        │▄░░▓▓░░░▄                                                    │  │
│ │   10   │░░░░▓░░░░░                                                   │  │
│ │        └────────────────────────────────────────────┘                │  │
│ │        0-20  20-40  40-60  60-80  80-100                            │  │
│ │             Quality Score (%)                                        │  │
│ └─────────────────────────────────────────────────────────────────────┘  │
│                                                                           │
│ Average Quality Score:    92.3/100    Data Completeness:    96.4%      │
│ Median Quality Score:     94.0/100    Profiles with Company:    142    │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## TAB 4: ℹ️ About Tab

```
┌─────────────────────────────────────────────────────────────────────────┐
│ About Alumni Data Extractor                                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│ An intelligent automation system for collecting, validating, and       │
│ structuring alumni data from LinkedIn profiles.                        │
│                                                                           │
│ Features                                                               │
│ ✅ Automated Discovery - Find LinkedIn profiles using Google Search    │
│ ✅ Web Scraping - Extract profile data with Playwright automation     │
│ ✅ AI Validation - Validate and correct data using OpenAI/Gemini      │
│ ✅ Data Cleaning - Remove duplicates and standardize formats          │
│ ✅ CSV Export - Generate clean, analysis-ready datasets               │
│ ✅ Analytics - Visualize alumni distribution and trends               │
│                                                                           │
│ Technology Stack                                                        │
│ • Backend: Python, Playwright, Beautiful Soup                         │
│ • Search: SerpAPI (Google Search)                                     │
│ • AI: OpenAI GPT / Google Gemini                                       │
│ • Data: Pandas, SQLAlchemy                                            │
│ • Frontend: Streamlit                                                 │
│                                                                           │
│             ┌────────────────────────────┐                             │
│             │ Project Info               │                             │
│             ├────────────────────────────┤                             │
│             │ Name: Alumni Data...       │                             │
│             │ Version: 1.0.0             │                             │
│             │ Status: Active Dev.        │                             │
│             │ Python: 3.9+               │                             │
│             │ License: MIT               │                             │
│             │ Created: March 2026        │                             │
│             └────────────────────────────┘                             │
│                                                                           │
│ Quick Links                                                             │
│ 📖 Full Documentation                                                  │
│ 🐙 GitHub Repository                                                   │
│ 🐛 Report Issues                                                       │
│ 💡 Suggest Features                                                    │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Using the Interface - Step by Step

### Step 1: Launch Application
```bash
# Windows
run_ui.bat

# macOS/Linux
./run_ui.sh

# Or
streamlit run ui/app.py
```

**Result**: Browser opens at `http://localhost:8501`

---

### Step 2: Configure Settings
```
In Sidebar:
1. Enter College Name (e.g., "MIT")
2. Select Batch Year (e.g., 2020)
3. Set Search Pages (e.g., 5)
4. Set Request Delay (e.g., 2 seconds)
5. Verify API Status shows green checkmarks
```

---

### Step 3: Start Extraction
```
In 🚀 Extraction Tab:
1. Click ▶️ START EXTRACTION
2. Watch progress bar advance through phases
3. See sample results preview when complete
```

---

### Step 4: View Results
```
In 📊 Results Tab:
1. See total profile count
2. Apply filters as needed
3. Review data in table
4. Download in preferred format
```

---

### Step 5: Analyze Data
```
In 📈 Analytics Tab:
1. View company distribution
2. See university breakdown
3. Check graduation timeline
4. Review quality metrics
```

---

## Responsive Design

### Desktop View (1920x1080+)
```
┌─────────────┬────────────────────────────────────┐
│  Sidebar    │  Main Content (2+ columns)          │
│   200px     │  1700px                             │
└─────────────┴────────────────────────────────────┘
```

### Tablet View (768x1024)
```
┌─────────────┬──────────────────────┐
│  Sidebar    │  Main Content        │
│   150px     │  620px               │
└─────────────┴──────────────────────┘
```

### Mobile View (375x667)
```
┌──────────────────────────────┐
│  Sidebar (Collapsible)       │
├──────────────────────────────┤
│  Main Content (Full Width)   │
└──────────────────────────────┘
```

---

## Color Scheme

### Primary Colors
- 🟣 **Primary**: #667eea (Purple)
- 🔵 **Gradient**: #667eea → #764ba2
- ⚫ **Text**: #262730 (Dark grey)
- ⚪ **Background**: #f0f2f6 (Light grey)
- ⚪ **Secondary BG**: #ffffff (White)

### Status Indicators
- 🟢 **Success**: #4caf50 (Green)
- 🔴 **Error**: #f44336 (Red)
- 🟡 **Warning**: #ff9800 (Orange)
- 🔵 **Info**: #2196f3 (Blue)

### Chart Colors
- 🟪 Primary: Purple gradient
- 🟦 Secondary: Blue palette
- 📊 Defaults: Streamlit auto-colors

---

## Future UI Enhancements

### Short Term (Phase 8)
- [ ] Dark mode toggle
- [ ] Custom color theme selector
- [ ] Real-time error logging dashboard
- [ ] Search functionality in results table
- [ ] Advanced filter combinations
- [ ] Scheduled extraction calendar

### Medium Term (Phase 9)
- [ ] User authentication
- [ ] Multi-user roles
- [ ] Saved search queries
- [ ] Email report scheduling
- [ ] Database integration UI
- [ ] API key management panel

### Long Term (Phase 10)
- [ ] Mobile app version
- [ ] PWA (Progressive Web App)
- [ ] Desktop application (Electron)
- [ ] Real-time collaboration
- [ ] Advanced data visualization
- [ ] Custom report builder

---

## Performance Metrics

| Action | Time |
|--------|------|
| Page Load | < 1s |
| Tab Switch | < 500ms |
| Filter Application | < 200ms |
| CSV Download (100 rows) | < 1s |
| Chart Rendering | < 500ms |
| Data Table Sort | < 100ms |

---

## Accessibility Features

- ✅ Semantic HTML structure
- ✅ Color-independent status indicators
- ✅ Readable font sizes (min 14px)
- ✅ High contrast text/background
- ✅ Keyboard navigable
- ✅ Descriptive button labels
- ✅ Hover tooltips
- ✅ Alt text for images

---

## Browser Support

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| Mobile Safari | 14+ | ✅ Good |
| Chrome Mobile | 90+ | ✅ Good |

---

**Last Updated**: March 23, 2026  
**UI Version**: 1.0.0  
**Framework**: Streamlit 1.28.0+
