
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re

# Configure Streamlit page
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the CORD-19 dataset"""
    try:
        df = pd.read_csv('metadata.csv', low_memory=False)
        # Basic cleaning
        df = df.dropna(subset=['title'])
        df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        df['publication_year'] = df['publish_time'].dt.year
        df['journal'] = df['journal'].fillna('Unknown')
        df['abstract'] = df['abstract'].fillna('')
        df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()) if x else 0)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.markdown("### Interactive exploration of COVID-19 research papers")

    # Load data
    with st.spinner("Loading CORD-19 dataset... This may take a moment."):
        df = load_data()

    if df is None:
        st.error("Failed to load data. Please ensure metadata.csv is available.")
        return

    # Sidebar filters
    st.sidebar.header("Filters & Options")

    # Year range filter
    min_year = int(df['publication_year'].min()) if not df['publication_year'].isna().all() else 2000
    max_year = int(df['publication_year'].max()) if not df['publication_year'].isna().all() else 2024

    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(2019, 2022),
        step=1
    )

    # Filter data by year
    filtered_df = df[
        (df['publication_year'] >= year_range[0]) & 
        (df['publication_year'] <= year_range[1])
    ].copy()

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Papers", f"{len(filtered_df):,}")

    with col2:
        unique_journals = filtered_df['journal'].nunique()
        st.metric("Unique Journals", f"{unique_journals:,}")

    with col3:
        avg_abstract_length = filtered_df['abstract_word_count'].mean()
        st.metric("Avg Abstract Length", f"{avg_abstract_length:.0f} words")

    with col4:
        year_span = year_range[1] - year_range[0] + 1
        st.metric("Years Covered", f"{year_span}")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Journals", "Text Analysis", "Data Sample"])

    with tab1:
        st.header("Publication Trends Over Time")

        # Publications by year
        yearly_counts = filtered_df['publication_year'].value_counts().sort_index()

        col1, col2 = st.columns(2)

        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(yearly_counts.index, yearly_counts.values, color='steelblue', alpha=0.7)
            ax.set_title('Publications by Year')
            ax.set_xlabel('Year')
            ax.set_ylabel('Number of Papers')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            st.pyplot(fig)

        with col2:
            # Monthly distribution for selected years
            if len(filtered_df) > 0:
                monthly_data = filtered_df.copy()
                monthly_data['month'] = monthly_data['publish_time'].dt.month
                monthly_counts = monthly_data['month'].value_counts().sort_index()

                fig, ax = plt.subplots(figsize=(10, 6))
                month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                ax.bar(monthly_counts.index, monthly_counts.values, color='orange', alpha=0.7)
                ax.set_title('Publications by Month')
                ax.set_xlabel('Month')
                ax.set_ylabel('Number of Papers')
                ax.set_xticks(range(1, 13))
                ax.set_xticklabels(month_names)
                plt.grid(True, alpha=0.3)
                st.pyplot(fig)

    with tab2:
        st.header("Journal Analysis")

        # Top journals
        top_journals = filtered_df['journal'].value_counts().head(15)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top Publishing Journals")
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.barh(range(len(top_journals)), top_journals.values, color='forestgreen', alpha=0.7)
            ax.set_yticks(range(len(top_journals)))
            ax.set_yticklabels([j[:30] + '...' if len(j) > 30 else j for j in top_journals.index])
            ax.set_xlabel('Number of Papers')
            ax.set_title('Top 15 Journals')
            plt.grid(True, alpha=0.3)
            st.pyplot(fig)

        with col2:
            st.subheader("Journal Statistics")
            st.write(f"**Total unique journals:** {filtered_df['journal'].nunique():,}")
            st.write(f"**Journals with only 1 paper:** {(filtered_df['journal'].value_counts() == 1).sum():,}")
            st.write(f"**Journals with >10 papers:** {(filtered_df['journal'].value_counts() > 10).sum():,}")

            # Show top journals table
            st.subheader("Top 10 Journals Table")
            top_10 = filtered_df['journal'].value_counts().head(10).reset_index()
            top_10.columns = ['Journal', 'Papers']
            top_10['Percentage'] = (top_10['Papers'] / len(filtered_df) * 100).round(1)
            st.dataframe(top_10, use_container_width=True)

    with tab3:
        st.header("Text Analysis")

        # Word frequency analysis
        if len(filtered_df) > 0:
            # Extract words from titles
            all_titles = ' '.join(filtered_df['title'].dropna().astype(str))
            words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())

            # Filter stop words
            stop_words = {'the', 'and', 'for', 'are', 'with', 'from', 'this', 'that', 
                         'study', 'analysis', 'research', 'using', 'based', 'new'}
            filtered_words = [word for word in words if word not in stop_words]

            word_counts = Counter(filtered_words)
            top_words = dict(word_counts.most_common(20))

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Most Frequent Words in Titles")
                fig, ax = plt.subplots(figsize=(10, 8))
                words_list = list(top_words.keys())[:15]
                counts_list = list(top_words.values())[:15]

                ax.barh(range(len(words_list)), counts_list, color='coral', alpha=0.7)
                ax.set_yticks(range(len(words_list)))
                ax.set_yticklabels(words_list)
                ax.set_xlabel('Frequency')
                ax.set_title('Top 15 Words in Titles')
                plt.grid(True, alpha=0.3)
                st.pyplot(fig)

            with col2:
                st.subheader("Abstract Length Distribution")
                fig, ax = plt.subplots(figsize=(10, 6))
                word_counts = filtered_df[filtered_df['abstract_word_count'] <= 500]['abstract_word_count']
                ax.hist(word_counts, bins=30, color='purple', alpha=0.7, edgecolor='black')
                ax.axvline(word_counts.mean(), color='red', linestyle='--', linewidth=2,
                          label=f'Mean: {word_counts.mean():.0f} words')
                ax.set_xlabel('Number of Words')
                ax.set_ylabel('Number of Papers')
                ax.set_title('Abstract Length Distribution')
                ax.legend()
                plt.grid(True, alpha=0.3)
                st.pyplot(fig)

    with tab4:
        st.header("Data Sample")

        # Display options
        sample_size = st.slider("Sample size to display", 5, 50, 10)

        # Show random sample
        if len(filtered_df) > 0:
            sample_df = filtered_df.sample(n=min(sample_size, len(filtered_df)))
            display_columns = ['title', 'journal', 'publication_year', 'abstract_word_count']
            available_columns = [col for col in display_columns if col in sample_df.columns]

            st.subheader(f"Random Sample of {len(sample_df)} Papers")
            st.dataframe(sample_df[available_columns], use_container_width=True)

            # Download option
            csv = sample_df.to_csv(index=False)
            st.download_button(
                label="Download Sample as CSV",
                data=csv,
                file_name=f"cord19_sample_{sample_size}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
