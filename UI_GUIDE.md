# Alumni Data Extractor - Web UI Guide

## Quick Start

### Option 1: Using the Launcher Script (Easiest)

#### Windows:
```bash
run_ui.bat
```

#### macOS/Linux:
```bash
chmod +x run_ui.sh
./run_ui.sh
```

### Option 2: Manual Launch

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Launch Streamlit
streamlit run ui/app.py
```

The web interface will open at: **http://localhost:8501**

---

## Features

### 🚀 Extraction Tab
- Configure search parameters (college, batch year)
- Set extraction options (pages, delays)
- Start automated data extraction
- Monitor progress in real-time
- View sample results preview

### 📊 Results Tab
- View all extracted profiles in a table
- Filter by:
  - Quality score
  - Company name
  - University
- Download data in multiple formats:
  - CSV (Excel-compatible)
  - JSON (structured)
  - Excel (with formatting)
- Summary statistics

### 📈 Analytics Tab
- **Top Companies** - Bar chart of most represented companies
- **Top Universities** - Bar chart of most represented universities
- **Graduation Distribution** - Timeline of when graduates completed their degrees
- **Quality Score Distribution** - Histogram showing data quality across profiles
- **Detailed Statistics** - Comprehensive metrics about the dataset

### ℹ️ About Tab
- Project overview and features
- Technology stack details
- How the system works (step-by-step)
- Getting started guide
- Quick links to documentation

---

## Configuration

### Via Sidebar (Web UI)
- College Name
- Batch Year
- Search Pages (1-10)
- Request Delay (1-10 seconds)
- API Status Indicators

### Via .env File
Edit `.env` file to configure:

```env
# API Keys
SERPAPI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Credentials
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password

# Extraction Settings
COLLEGE_NAME=Your College
BATCH_YEAR=2020
SEARCH_PAGES=5
REQUEST_DELAY=2
AI_MODEL=openai
```

---

## Using the Interface

### Step 1: Configure Settings
1. Go to the **Extraction** tab
2. Set college name and batch year in the sidebar
3. Adjust search pages and delays if needed
4. Verify all API keys are configured (green checkmarks)

### Step 2: Start Extraction
1. Click **▶️ START EXTRACTION** button
2. Watch the progress bar track each phase:
   - Searching LinkedIn profiles
   - Scraping profile data
   - Extracting information
   - Validating with AI
   - Cleaning duplicates
   - Exporting to CSV

### Step 3: View Results
1. Go to the **Results** tab
2. Use filters to find profiles:
   - By quality score
   - By company
   - By university
3. View statistics and total record count
4. Download data in your preferred format

### Step 4: Analyze Data
1. Go to the **Analytics** tab
2. View charts and distributions:
   - Company representation
   - University distribution
   - Graduation timeline
   - Quality metrics

---

## Troubleshooting

### "Streamlit is not installed"
```bash
pip install streamlit
```

### Port 8501 Already in Use
```bash
# Use a different port
streamlit run ui/app.py --server.port=8502
```

### Slow Performance
- Reduce the number of search pages
- Increase REQUEST_DELAY to avoid rate limiting
- Check your internet connection
- Ensure API keys have sufficient quota

### Missing API Keys
- Edit `.env` file with actual API keys
- Verify keys have appropriate permissions
- Check for expired or revoked credentials

### No Data Loading
- Ensure extraction has completed
- Check that `output/alumni_data.csv` exists
- Verify CSV file is not corrupted
- Try clearing results and running extraction again

---

## Data Export Formats

### CSV (Comma-Separated Values)
- **Best for**: Excel, Google Sheets, data analysis
- **Columns**: Name, URL, Company, Position, University, Degree, Year, Quality Score
- **Use**: Import directly into spreadsheet applications

### JSON (JavaScript Object Notation)
- **Best for**: API integration, flexible data structures
- **Format**: Array of profile objects with all fields
- **Use**: Process with programming languages or APIs

### Excel (.xlsx)
- **Best for**: Professional reports, formatted tables
- **Format**: Formatted spreadsheet with headers
- **Use**: Distribution to non-technical users

---

## Analytics Insights

### Company Distribution
- Identifies which companies employ most alumni
- Helpful for:
  - Job placement tracking
  - Employer partnerships
  - Career outcome analysis

### University Distribution
- Shows multiple degree holders
- Helpful for:
  - Alumni who studied at multiple institutions
  - Advanced degree tracking
  - Education background analysis

### Graduation Timeline
- Visualizes when graduates completed studies
- Helpful for:
  - Cohort analysis
  - Career progression over time
  - Trend identification

### Quality Scores
- Indicates data completeness and accuracy
- Scores 0-100 based on:
  - Name completeness
  - Company information
  - University information
  - Graduation year presence
  - AI validation confidence

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `r` | Rerun the app |
| `c` | Open settings menu |
| `k` | Open command palette |

---

## Performance Tips

1. **Start small** - Use 5-10 search pages initially
2. **Increase delays** - Use 3-5 second delays to avoid rate limiting
3. **Filter results** - Load only needed data with quality filters
4. **Clear cache** - Delete old results if performance degrades
5. **Monitor quotas** - Check API usage regularly to avoid overage charges

---

## Advanced Usage

### Batch Processing
Process multiple colleges in sequence:
1. Extract data for College A
2. Download results
3. Change college name in sidebar
4. Repeat extraction for College B
5. Combine results externally

### Custom Filtering
Python script to work with exported CSV:
```python
import pandas as pd

# Load data
df = pd.read_csv('alumni_data.csv')

# Filter to Google employees only
google_alumni = df[df['current_company'] == 'Google']

# Export filtered results
google_alumni.to_csv('google_alumni.csv', index=False)

print(f"Found {len(google_alumni)} Google employees")
```

### Integration with Other Systems
- Use CSV export to import into CRM systems
- Process JSON export with custom Python scripts
- Import into databases for advanced querying
- Visualize in BI tools (Tableau, Power BI, Looker)

---

## Support

For issues or questions:
1. Check the **About** tab for documentation links
2. Review error messages in the browser console
3. Check logs in the `logs/` directory
4. Verify `.env` configuration
5. Ensure all dependencies are installed

---

## Security Notes

- ⚠️ Never commit `.env` file to version control
- ⚠️ Protect your API keys and credentials
- ⚠️ Use IP whitelisting for API keys when possible
- ⚠️ Regularly rotate credentials
- ⚠️ Monitor API usage for unusual activity

---

## License

MIT License - See LICENSE file for details

---

**Last Updated**: March 23, 2026  
**Version**: 1.0.0
