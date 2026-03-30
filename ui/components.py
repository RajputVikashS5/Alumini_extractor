"""
UI Components for Alumni Data Extractor Streamlit App
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path


def render_metric_card(title, value, icon=""):
    """Render a metric card"""
    st.metric(label=f"{icon} {title}", value=value)


def render_config_section():
    """Render the configuration sidebar section"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        try:
            from config.settings import config
            has_config = True
        except:
            has_config = False
        
        college_name = st.text_input(
            "College Name",
            value=config.COLLEGE_NAME if has_config else "MIT",
        )
        
        batch_year = st.number_input(
            "Batch Year",
            min_value=1950,
            max_value=2030,
            value=config.BATCH_YEAR if has_config else 2020,
        )
        
        search_pages = st.slider(
            "Search Pages",
            min_value=1,
            max_value=10,
            value=config.SEARCH_PAGES if has_config else 5,
        )
        
        return {
            "college_name": college_name,
            "batch_year": batch_year,
            "search_pages": search_pages
        }


def render_api_status():
    """Render API status indicators"""
    try:
        from config.settings import config
        
        col1, col2, col3 = st.columns(3)
        
        has_serpapi = bool(config.SERPAPI_API_KEY and 
                          config.SERPAPI_API_KEY != "your_serpapi_key_here")
        has_openai = bool(config.OPENAI_API_KEY and 
                         config.OPENAI_API_KEY != "your_openai_api_key_here")
        has_linkedin = bool(config.LINKEDIN_EMAIL and 
                           config.LINKEDIN_EMAIL != "your_linkedin_email@example.com")
        
        with col1:
            if has_serpapi:
                st.success("✓ SerpAPI")
            else:
                st.error("✗ SerpAPI")
        
        with col2:
            if has_openai:
                st.success("✓ OpenAI")
            else:
                st.error("✗ OpenAI")
        
        with col3:
            if has_linkedin:
                st.success("✓ LinkedIn")
            else:
                st.error("✗ LinkedIn")
    
    except Exception as e:
        st.warning(f"Could not check API status: {str(e)}")


def load_results_csv(filepath="output/alumni_data.csv"):
    """Load and return CSV data"""
    try:
        path = Path(filepath)
        if path.exists():
            return pd.read_csv(filepath)
        return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def display_results_table(df, max_rows=100):
    """Display results in a formatted table"""
    if df is None or len(df) == 0:
        st.info("No data available")
        return
    
    # Create columns for filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_quality = st.slider("Min Quality Score", 0, 100, 0)
    
    with col2:
        company_filter = st.multiselect(
            "Filter by Company",
            options=sorted(df['current_company'].unique()) if 'current_company' in df.columns else []
        )
    
    with col3:
        university_filter = st.multiselect(
            "Filter by University",
            options=sorted(df['university'].unique()) if 'university' in df.columns else []
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if 'quality_score' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['quality_score'] >= min_quality]
    
    if company_filter and 'current_company' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['current_company'].isin(company_filter)]
    
    if university_filter and 'university' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['university'].isin(university_filter)]
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} profiles**")
    st.dataframe(filtered_df, use_container_width=True, height=400, hide_index=True)
    
    return filtered_df


def create_download_buttons(df):
    """Create download buttons for different formats"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        json_data = df.to_json(orient="records", indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        excel_buffer = df.to_excel(index=False, engine='openpyxl')
        st.download_button(
            label="📥 Download Excel",
            data=excel_buffer,
            file_name=f"alumni_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


def render_statistics(df):
    """Render statistics metrics"""
    if df is None or len(df) == 0:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Profiles", len(df))
    
    with col2:
        unique_companies = df['current_company'].nunique() if 'current_company' in df.columns else 0
        st.metric("Unique Companies", unique_companies)
    
    with col3:
        unique_unis = df['university'].nunique() if 'university' in df.columns else 0
        st.metric("Unique Universities", unique_unis)
    
    with col4:
        avg_quality = df['quality_score'].mean() if 'quality_score' in df.columns else 0
        st.metric("Avg Quality Score", f"{avg_quality:.1f}/100")


def render_charts(df):
    """Render analytics charts"""
    if df is None or len(df) == 0:
        st.info("No data available for charts")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'current_company' in df.columns:
            st.markdown("### Top Companies")
            company_counts = df['current_company'].value_counts().head(10)
            st.bar_chart(company_counts)
    
    with col2:
        if 'university' in df.columns:
            st.markdown("### Top Universities")
            university_counts = df['university'].value_counts().head(10)
            st.bar_chart(university_counts)
    
    if 'graduation_year' in df.columns:
        st.markdown("### Graduation Year Distribution")
        year_counts = df['graduation_year'].value_counts().sort_index()
        st.line_chart(year_counts)
    
    if 'quality_score' in df.columns:
        st.markdown("### Quality Score Distribution")
        st.histogram(df['quality_score'], bins=20, use_container_width=True)
