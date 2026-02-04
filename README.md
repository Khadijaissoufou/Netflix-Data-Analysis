# 🎬 Netflix Content Analysis - Data Visualization & Interactive Dashboard

## 📌 Project Overview

This project provides a **comprehensive data analysis** of Netflix's film and series catalog, exploring content distribution, temporal trends, genres, production countries, and viewing classifications. It combines **static exploratory analysis** with an **interactive Streamlit dashboard** for dynamic insights.

**Key Question:** How has Netflix evolved from a DVD rental service to a global content production powerhouse?

---

## 🎯 Objectives

- Analyze the distribution of **movies vs. TV shows** in Netflix's catalog
- Track the **evolution of content additions** over time (2015-2020+)
- Identify the **most popular genres, ratings, and production countries**
- Examine **film duration patterns** and standardization trends
- Create an **interactive dashboard** for exploring genre popularity trends

---

## 🛠️ Technologies & Tools

**Data Analysis & Visualization:**
- Python 3.x
- Pandas (data manipulation)
- Matplotlib, Seaborn (static visualizations)
- Plotly (interactive charts)

**Interactive Dashboard:**
- **Streamlit** (web app for dynamic genre analysis)

**Presentation:**
- PowerPoint (executive summary and key findings)

---

## 🧹 Data Cleaning & Preprocessing

The analysis includes comprehensive data cleaning steps:

1. **Date Processing**:
   - Converted `date_added` to datetime format
   - Extracted year and month for temporal analysis

2. **Duration Standardization**:
   - Separated `duration` into two columns:
     - `duration_min` for movies (in minutes)
     - `duration_seasons` for TV shows (number of seasons)

3. **Missing Values Handling**:
   - Categorical columns (`director`, `cast`, `country`, `rating`): Filled with "Unknown"
   - Numeric columns: Handled based on type (mean/mode imputation)

4. **List Columns Preparation**:
   - Transformed comma-separated values into lists for:
     - Genres (`genres_list`)
     - Countries (`countries_list`)
     - Cast (`cast_list`)
     - Directors (`director_list`)

5. **Feature Engineering**:
   - Created `decade` column for production era analysis
   - Filtered clean dataset for temporal analyses

---

## 📊 Key Findings

### 1. **Catalog Composition**
- Distribution between movies and TV series
- Evolution from DVD rental to original content production

### 2. **Hyper-Growth Strategy (2015-2019)**
- **+2,600% increase** in content production
- Shift from licensing to original productions

### 3. **Content Standardization**
- Average film duration: **~99 minutes** (optimized Netflix format)
- Strategic focus on binge-watchable content

### 4. **Global Expansion**
- **30% of catalog** dedicated to international content
- Top 10 producing countries analyzed

### 5. **Genre & Rating Trends**
- Top 10 most produced genres
- Top 7 content classifications (PG, TV-MA, R, etc.)

---

## 🖥️ Interactive Dashboard

The project includes a **Streamlit application** that allows users to:
- Explore genre popularity evolution over time
- Filter by country, rating, or content type
- Visualize trends with interactive charts

**To run the dashboard:**
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 📁 Project Structure

```
Netflix-Data-Analysis/
│
├── data/
│   └── netflix_titles.csv          # Netflix catalog dataset
│
├── netflix_analysis.py             # Complete EDA script (data cleaning + visualizations)
│
├── app.py                          # Streamlit interactive dashboard
│
├── presentation/
│   └── Netflix_Analysis.pptx       # PowerPoint presentation (French)
│
└── README.md                       # Project documentation
```

**Note:** The main analysis is in `netflix_analysis.py`, which includes:
- Data loading and exploration
- Data cleaning and preprocessing
- 9 comprehensive visualizations
- Statistical summaries

---

## 📈 Visualizations Included

### Static Analysis (Python/Matplotlib/Seaborn)
1. **Pie Chart**: Movies vs. TV Shows distribution
2. **Line Chart**: Evolution of content additions by year
3. **Bar Charts**:
   - Top 15 most popular genres
   - Top 15 producing countries
   - Top 10 most frequent actors
   - Content ratings distribution
   - Production by decade
4. **Line Chart**: Evolution of top 5 genres over time
5. **Comparative Pie Charts**: Film/Series distribution for top 3 countries
6. **Histograms & Boxplots**: 
   - Film duration distribution
   - TV show seasons distribution
7. **Interactive Dashboard**: Genre popularity trends (Streamlit)

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas matplotlib seaborn numpy streamlit
```

### Execute Main Analysis
```bash
python netflix_analysis.py
```

This will:
- Load and clean the dataset
- Generate all 9 visualizations automatically
- Display statistical summaries in the console

### Launch Interactive Dashboard
```bash
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## 💡 Insights & Business Implications

> **"Netflix no longer follows trends — it creates them through data-driven decisions."**

- **Strategic standardization**: 99-minute average optimizes viewer engagement
- **Data-driven content**: Production decisions informed by viewing patterns
- **Global localization**: 30% international content reflects worldwide expansion
- **Industrialization**: From curator to creator in under a decade

---

## 📚 Dataset

**Source:** Netflix Movies and TV Shows  
**Period:** 2008 - 2021  
**Variables:** Title, Type, Director, Cast, Country, Release Year, Rating, Duration, Genres, Description

---

## 🎓 Skills Demonstrated

- Exploratory Data Analysis (EDA)
- Data cleaning and preprocessing
- Statistical visualization (Matplotlib, Seaborn, Plotly)
- Interactive dashboard development (Streamlit)
- Business insights extraction
- Data storytelling and presentation

---

## 👥 Authors

**Khadija MAHAMADOU ISSOUFOU**  
Master's student in Data Science & Applied Economics  
University of Lille

**Ren Yue**  
Collaborator

📧 khadija.mahamadou19@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/khadija-mahamadou-issoufou)  
💻 [GitHub](https://github.com/Khadijaissoufou)

---

## 📝 Academic Context

This project was completed as part of the **Data Science & Applied Economics** program at the University of Lille (2025-2026).

---

## 🙏 Acknowledgments

- Dataset sourced from publicly available Netflix catalog data
- Inspired by the strategic transformation of streaming platforms
- Developed using open-source Python libraries

---

## 📄 License

This project is for educational and academic purposes.

---

## 🔗 Related Projects

Check out my other data analysis projects:
- [NLP Job Market Analysis](https://github.com/Khadijaissoufou/NLP-Job-Market-Analysis)
- [Housing Prices Spatial Analysis](https://github.com/Khadijaissoufou/HousingPrices_SpatialAnalysis)
- [French Stocks Forecasting](https://github.com/Khadijaissoufou/French-stocks-forecasting)
- [Credit Risk Scoring](https://github.com/Khadijaissoufou/credit-risk-scoring-loanclub)
