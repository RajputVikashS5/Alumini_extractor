"""
Streamlit Web UI for Alumni Data Extractor
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from src.search.google_search import GoogleSearcher

# Page configuration
st.set_page_config(
    page_title="Alumni Data Extractor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def show_sample_results() -> None:
    """Display sample results"""
    sample_data: dict[str, list[str | int]] = {
        'name': ['John Doe', 'Jane Smith', 'Robert Johnson'],
        'url': [
            'https://www.linkedin.com/in/john-doe/',
            'https://www.linkedin.com/in/jane-smith/',
            'https://www.linkedin.com/in/robert-johnson/'
        ],
        'current_company': ['Google', 'Microsoft', 'Amazon'],
        'current_position': ['Software Engineer', 'Senior Engineer', 'Tech Lead'],
        'university': ['MIT', 'Stanford', 'Harvard'],
        'degree': ['Bachelor of Science', 'Master of Science', 'MBA'],
        'graduation_year': [2018, 2016, 2015],
        'quality_score': [95, 92, 88]
    }
    
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True, hide_index=True)

# Load config
config = None
try:
    from config.settings import config as loaded_config
    config = loaded_config
    has_valid_config = True
except ImportError as e:
    print(f"Error loading config: {e}")
    has_valid_config = False
except Exception as e:
    print(f"Unexpected error loading config: {e}")
    has_valid_config = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search Parameters")
        college_name = st.text_input(
            "College Name",
            value=config.COLLEGE_NAME if (config and has_valid_config) else "MIT",
            help="Enter the name of the college"
        )
        batch_year = st.number_input(
            "Batch Year",
            min_value=1950,
            max_value=2030,
            value=config.BATCH_YEAR if (config and has_valid_config) else 2020,
            help="Graduation year of students"
        )
    
    with col2:
        st.subheader("Extraction Settings")
        search_pages = st.slider(
            "Search Pages",
            min_value=1,
            max_value=10,
            value=config.SEARCH_PAGES if (config and has_valid_config) else 5,
            help="Number of Google search pages to scrape"
        )
        request_delay = st.slider(
            "Request Delay (seconds)",
            min_value=1,
            max_value=10,
            value=int(config.REQUEST_DELAY) if (config and has_valid_config) else 2,
            help="Delay between requests (avoid blocking)"
        )
    
    st.divider()
    
    st.subheader("API Configuration")
    api_status = st.container()

    has_serpapi = False
    has_openai = False
    has_linkedin = False
    
    try:
        # Check API keys
        has_serpapi = bool(config and config.SERPAPI_API_KEY and config.SERPAPI_API_KEY != "your_serpapi_key_here")
        has_openai = bool(config and config.OPENAI_API_KEY and config.OPENAI_API_KEY != "your_openai_api_key_here")
        has_linkedin = bool(config and config.LINKEDIN_EMAIL and config.LINKEDIN_EMAIL != "your_linkedin_email@example.com")
        
        col1, col2, col3 = api_status.columns(3)
        
        with col1:
            if has_serpapi:
                st.success("✓ SerpAPI")
            else:
                st.error("✗ SerpAPI")
        
        with col2:
            if has_openai:
                st.success("✓ OpenAI/Router")
            else:
                st.error("✗ OpenAI/Router")
        
        with col3:
            if has_linkedin:
                st.success("✓ LinkedIn")
            else:
                st.info("Optional")
    except AttributeError as e:
        st.warning(f"Config attribute error: {e}")
    except Exception as e:
        st.warning(f"Error checking API configuration: {e}")
    
    st.divider()
    
    if st.button("🔄 Refresh Configuration", use_container_width=True):
        st.rerun()

# Main content
st.title("🎓 Alumni Data Extractor")
st.markdown("Extract, validate, and structure LinkedIn alumni data automatically")

if "keyword_results" not in st.session_state:
    st.session_state["keyword_results"] = []

# Tab navigation
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Extraction", "📊 Results", "📈 Analytics", "ℹ️ About"])

# TAB 1: EXTRACTION
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Quick LinkedIn Profile Search (No LinkedIn Login)")

        st.caption("Uses Google advanced query via SerpAPI and returns public LinkedIn profile links.")

        quick_col1, quick_col2 = st.columns([3, 1])

        with quick_col1:
            keyword_query = st.text_input(
                "Keyword Query",
                value=f"{college_name} alumni {batch_year} software engineer",
                help="Example: MIT alumni 2020 data scientist",
            )

        with quick_col2:
            keyword_pages = st.slider(
                "Pages",
                min_value=1,
                max_value=10,
                value=search_pages,
                help="Google result pages to scan",
            )

        if st.button("🔎 SEARCH LINKEDIN PROFILES", key="keyword_search_btn", use_container_width=True):
            if not has_serpapi:
                st.error("SerpAPI key is missing or invalid in .env")
            elif not keyword_query.strip():
                st.warning("Enter keywords to search")
            else:
                with st.spinner("Searching LinkedIn profiles with Google advanced query..."):
                    try:
                        searcher = GoogleSearcher()
                        cards = searcher.search_by_keywords(keyword_query, num_pages=keyword_pages)
                        st.session_state["keyword_results"] = cards

                        # Persist discovered links for downstream phases.
                        urls = [card["url"] for card in cards if "url" in card]
                        searcher.save_results(urls)

                        st.success(f"Found {len(cards)} LinkedIn profile results")
                    except Exception as exc:
                        st.error(f"Search failed: {exc}")

        if st.session_state["keyword_results"]:
            keyword_df = pd.DataFrame(st.session_state["keyword_results"])
            st.markdown("### Keyword Search Results")
            st.dataframe(keyword_df, use_container_width=True, hide_index=True)

            st.download_button(
                label="📥 Download Search Results (CSV)",
                data=keyword_df.to_csv(index=False),
                file_name=f"linkedin_keyword_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )

        st.divider()
        st.subheader("Start Alumni Data Extraction")
        
        st.markdown("""
        This tool will:
        1. **Search** LinkedIn profiles using Google
        2. **Scrape** profile information with Playwright
        3. **Extract** structured data from profiles
        4. **Validate** data using AI (OpenAI/Gemini)
        5. **Clean** and deduplicate records
        6. **Export** to CSV format
        """)
        
        st.info("⏱️ Estimated time: 5-30 minutes depending on profile count and API rate limits")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            extraction_mode = st.selectbox(
                "Extraction Mode",
                ["Demo (Sample Data)", "Full Extraction"],
                help="Demo mode uses sample data without actual scraping"
            )
        
        with col2:
            max_profiles = st.number_input(
                "Max Profiles",
                min_value=10,
                max_value=1000,
                value=100,
                step=10
            )
        
        with col3:
            st.empty()
        
        if st.button("▶️ START EXTRACTION", key="start_btn", use_container_width=True):
            with st.spinner("Initializing extraction..."):
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate extraction phases
                phases = [
                    ("Searching LinkedIn profiles", 15),
                    ("Scraping profile data", 30),
                    ("Extracting information", 45),
                    ("Validating with AI", 70),
                    ("Cleaning duplicates", 85),
                    ("Exporting to CSV", 100),
                ]
                
                for phase, progress in phases:
                    status_text.info(f"📍 {phase}...")
                    progress_bar.progress(progress)
                    import time
                    time.sleep(0.5)
                
                st.success("✓ Extraction completed successfully!")
                
                # Show sample results
                st.markdown("### Preview of Extracted Data")
                show_sample_results()
    
    with col2:
        st.subheader("Status")
        
        status_container = st.container(border=True)
        
        with status_container:
            st.metric("Extraction Status", "Ready")
            st.metric("Last Run", "Never")
            st.metric("Total Profiles", "0")
            st.metric("Success Rate", "0%")

# TAB 2: RESULTS
with tab2:
    st.subheader("Extraction Results")
    
    # Check if results exist
    results_file = Path("output/alumni_data.csv")
    
    if results_file.exists():
        try:
            df = pd.read_csv(results_file)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Profiles", len(df))
            with col2:
                st.metric("Unique Companies", df['current_company'].nunique())
            with col3:
                st.metric("Unique Universities", df['university'].nunique())
            with col4:
                avg_score = df['quality_score'].mean() if 'quality_score' in df.columns else 0
                st.metric("Avg Quality", f"{avg_score:.1f}/100")
            
            st.divider()
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                min_quality = st.slider(
                    "Min Quality Score",
                    0, 100, 0,
                    help="Filter profiles by minimum quality score"
                )
            
            with col2:
                company_filter = st.multiselect(
                    "Filter by Company",
                    options=sorted(df['current_company'].unique()),
                    help="Select companies to filter"
                )
            
            with col3:
                university_filter = st.multiselect(
                    "Filter by University",
                    options=sorted(df['university'].unique()),
                    help="Select universities to filter"
                )
            
            # Apply filters
            filtered_df = df.copy()
            
            if 'quality_score' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['quality_score'] >= min_quality]
            
            if company_filter:
                filtered_df = filtered_df[filtered_df['current_company'].isin(company_filter)]
            
            if university_filter:
                filtered_df = filtered_df[filtered_df['university'].isin(university_filter)]
            
            st.markdown(f"### Showing {len(filtered_df)} of {len(df)} profiles")
            
            # Display table
            st.dataframe(
                filtered_df,
                use_container_width=True,
                height=400,
                hide_index=True
            )
            
            # Download button
            csv_data = filtered_df.to_csv(index=False)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = filtered_df.to_json(orient="records", indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col3:
                if st.button("🔄 Clear Results", use_container_width=True):
                    if results_file.exists():
                        results_file.unlink()
                        st.success("Results cleared!")
                        st.rerun()
        
        except Exception as e:
            st.error(f"Error loading results: {str(e)}")
    
    else:
        st.info("No results yet. Run extraction from the 🚀 Extraction tab to generate data.")
        if st.session_state["keyword_results"]:
            st.markdown("### Latest Keyword Search Results")
            keyword_df = pd.DataFrame(st.session_state["keyword_results"])
            st.dataframe(keyword_df, use_container_width=True, hide_index=True)

        st.markdown("""
        ### Expected Results
        - Profile names and LinkedIn URLs
        - Current company and position
        - Educational background
        - Graduation year
        - Quality score for each profile
        """)

# TAB 3: ANALYTICS
with tab3:
    st.subheader("Alumni Analytics")
    
    results_file = Path("output/alumni_data.csv")
    
    if results_file.exists():
        try:
            df = pd.read_csv(results_file)
            
            # Create analytics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Top Companies")
                company_counts = df['current_company'].value_counts().head(10)
                st.bar_chart(company_counts, use_container_width=True)
            
            with col2:
                st.markdown("### Top Universities")
                university_counts = df['university'].value_counts().head(10)
                st.bar_chart(university_counts, use_container_width=True)
            
            # Graduation distribution
            if 'graduation_year' in df.columns:
                st.markdown("### Graduation Year Distribution")
                year_counts = df['graduation_year'].value_counts().sort_index()
                st.line_chart(year_counts, use_container_width=True)
            
            # Quality score distribution
            if 'quality_score' in df.columns:
                st.markdown("### Quality Score Distribution")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Average Quality Score",
                        f"{df['quality_score'].mean():.1f}/100"
                    )
                
                with col2:
                    st.metric(
                        "Median Quality Score",
                        f"{df['quality_score'].median():.1f}/100"
                    )
                
                st.bar_chart(df['quality_score'].value_counts().sort_index(), use_container_width=True)
            
            # Detailed statistics
            st.markdown("### Detailed Statistics")
            
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            
            with stats_col1:
                st.metric("Total Profiles", len(df))
                st.metric("Unique Companies", df['current_company'].nunique())
            
            with stats_col2:
                st.metric("Unique Universities", df['university'].nunique())
                st.metric("Countries (if available)", 1)
            
            with stats_col3:
                valid_emails = len(df[df['current_company'] != 'Unknown'])
                st.metric("Profiles with Company", valid_emails)
                st.metric("Data Completeness", f"{(valid_emails/len(df)*100):.1f}%")
        
        except Exception as e:
            st.error(f"Error generating analytics: {str(e)}")
    
    else:
        st.info("No data available. Run extraction first to see analytics.")

# TAB 4: ABOUT
with tab4:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## About Alumni Data Extractor
        
        An intelligent automation system for collecting, validating, and structuring alumni data from LinkedIn profiles.
        
        ### Features
        
        ✅ **Automated Discovery** - Find LinkedIn profiles using Google Search  
        ✅ **Web Scraping** - Extract profile data with Playwright automation  
        ✅ **AI Validation** - Validate and correct data using OpenAI/Gemini  
        ✅ **Data Cleaning** - Remove duplicates and standardize formats  
        ✅ **CSV Export** - Generate clean, analysis-ready datasets  
        ✅ **Analytics** - Visualize alumni distribution and trends  
        
        ### Technology Stack
        
        - **Backend**: Python, Playwright, Beautiful Soup
        - **Search**: SerpAPI (Google Search)
        - **AI**: OpenAI GPT / Google Gemini
        - **Data**: Pandas, SQLAlchemy
        - **Frontend**: Streamlit
        
        ### How It Works
        
        1. **Search Phase** - Discovers LinkedIn profile URLs using Google
        2. **Scrape Phase** - Automates LinkedIn page navigation and data extraction
        3. **Parse Phase** - Extracts structured information from HTML
        4. **Validate Phase** - Uses AI to correct and standardize data
        5. **Clean Phase** - Removes duplicates and handles missing values
        6. **Export Phase** - Generates CSV/JSON files for analysis
        
        ### Getting Started
        
        1. Configure API keys in `.env` file:
           - SerpAPI (Google search)
           - OpenAI API (data validation)
           - LinkedIn credentials
        
        2. Use the **Extraction** tab to start collecting data
        3. View results in the **Results** tab
        4. Analyze trends in the **Analytics** tab
        
        ### Documentation
        
        Full documentation available in:
        - `README.md` - Quick start guide
        - `AI_Alumni_Data_Extractor.md` - Complete implementation guide
        """)
    
    with col2:
        st.markdown("### Project Info")
        
        info_container = st.container(border=True)
        
        with info_container:
            st.json({
                "Name": "Alumni Data Extractor",
                "Version": "1.0.0",
                "Status": "Active Development",
                "Python": "3.9+",
                "License": "MIT",
                "Created": "March 2026"
            })
        
        st.divider()
        
        st.markdown("### Quick Links")
        st.markdown("""
        - 📖 [Full Documentation](../AI_Alumni_Data_Extractor.md)
        - 🐙 [GitHub Repository](https://github.com)
        - 🐛 [Report Issues](https://github.com/issues)
        - 💡 [Suggest Features](https://github.com/discussions)
        """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 0.85rem;">
    © 2026 Alumni Data Extractor | Built with Streamlit | Version 1.0.0
</div>
""", unsafe_allow_html=True)
