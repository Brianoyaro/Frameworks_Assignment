# CORD-19 Data Analysis Project

## Overview
This project provides a comprehensive analysis of the CORD-19 dataset, focusing on COVID-19 research papers metadata. The analysis includes data exploration, cleaning, visualization, and an interactive Streamlit web application.

## Project Structure

### 📁 Files Created
- `cord19_analysis.ipynb` - Main Jupyter notebook with complete analysis
- `streamlit_app.py` - Interactive web application
- `project_summary.md` - This documentation file

### 📊 Dataset
- **Source**: CORD-19 COVID-19 research papers metadata
- **File**: `metadata.csv` (large file ~1.6GB)
- **Records**: 500,000+ research papers
- **Time Range**: Primarily 2019-2022 (COVID-19 era)

## Analysis Components

### Part 1: Data Loading and Basic Exploration
- ✅ Load CORD-19 metadata into pandas DataFrame
- ✅ Examine dataset dimensions and structure
- ✅ Identify data types and basic statistics
- ✅ Display sample data

### Part 2: Data Cleaning and Preparation
- ✅ Identify missing values in key columns
- ✅ Remove rows with missing titles (essential for analysis)
- ✅ Fill missing abstracts, journals, and authors with defaults
- ✅ Create cleaned dataset for analysis

### Part 3: Feature Engineering
- ✅ Convert publication dates to datetime format
- ✅ Extract publication years for trend analysis
- ✅ Calculate word counts for abstracts and titles
- ✅ Standardize journal names

### Part 4: Publication Trends Analysis
- ✅ Count papers by publication year
- ✅ Focus on COVID-19 era (2019-2022)
- ✅ Calculate growth rates between years
- ✅ Identify peak research periods

### Part 5: Journal and Source Analysis
- ✅ Identify top journals publishing COVID-19 research
- ✅ Analyze journal diversity and concentration
- ✅ Calculate publication distribution across sources

### Part 6: Text Analysis
- ✅ Extract words from paper titles
- ✅ Filter stop words and calculate frequencies
- ✅ Identify most common research terms
- ✅ Analyze COVID-19 specific terminology

### Part 7: Data Visualizations
- ✅ Publications over time (bar charts with trend lines)
- ✅ Top journals (horizontal bar charts)
- ✅ Word frequency analysis (bar charts)
- ✅ Abstract length distribution (histograms)
- ✅ Monthly publication patterns
- ✅ Year comparison (pie charts)
- ✅ Word cloud generation (optional)

### Part 8: Streamlit Application
- ✅ Interactive web interface
- ✅ Year range filters
- ✅ Multiple tabs for different analyses
- ✅ Real-time data filtering
- ✅ Download functionality
- ✅ Responsive design

## Key Findings

### 📈 Publication Trends
- Massive surge in COVID-19 research starting in 2020
- Peak research output during 2020-2021
- Exponential growth in pandemic-related publications

### 📰 Top Research Venues
- Identified leading journals in COVID-19 research
- High concentration in medical and epidemiology journals
- Thousands of unique publication venues

### 📝 Research Focus Areas
- Most common terms: "covid", "coronavirus", "sars", "patients"
- Average abstract length: ~150-200 words
- Strong focus on clinical studies and treatments

## Technical Implementation

### 📚 Libraries Used
- **pandas**: Data manipulation and analysis
- **matplotlib/seaborn**: Data visualization
- **streamlit**: Web application framework
- **numpy**: Numerical computing
- **collections**: Data structures (Counter)
- **re**: Regular expressions for text processing

### 🎨 Visualization Types
- Bar charts for trends and comparisons
- Histograms for distributions
- Horizontal bar charts for rankings
- Pie charts for proportional data
- Word clouds for text visualization
- Line charts for time series

### 🌐 Streamlit Features
- **Interactive Filters**: Year range selection
- **Tabbed Interface**: Organized content sections
- **Real-time Updates**: Dynamic filtering and visualization
- **Download Options**: Export filtered data
- **Responsive Design**: Works on desktop and mobile

## How to Use

### 🔧 Setup
```bash
# Install required packages
# pip install pandas matplotlib seaborn streamlit wordcloud
pip install -r requirements.txt

# Ensure metadata.csv is in the project directory
```

### 📓 Running the Notebook
```bash
# Open Jupyter notebook
jupyter notebook cord19_analysis.ipynb

# Run all cells to see complete analysis
```

### 🚀 Running the Streamlit App
```bash
# Launch the web application
streamlit run streamlit_app.py

# Open browser to http://localhost:8501
```

