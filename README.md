# 🎾 GAME ANALYTICS: UNLOCKING TENNIS DATA WITH SPORTRADAR API  

This repository presents an **end-to-end sports analytics solution** built using **Python, SQL, MySQL, and Streamlit**, leveraging the **SportRadar Tennis API** to extract, analyze, and visualize professional tennis competition data.

The project focuses on transforming **complex nested API data** into a **structured relational database** and delivering **actionable insights** through SQL analytics and an interactive dashboard.

---

# 📊 Tennis Analytics Dashboard  

------------------------------------------------------------------------

📊 **Dashboard Overview**  
The Tennis Analytics Dashboard is an **interactive Streamlit-based analytics application** built on top of professional tennis data sourced from the **SportRadar Tennis API**.

It enables multi-dimensional analysis across:
- Tennis competitions  
- Venues & complexes  
- Player rankings & performance  

Designed for **sports analysts, tournament organizers, data analysts, and tennis enthusiasts**.

------------------------------------------------------------------------

🔹 **Key Features:**  
✅ API-driven real-world sports data integration  
✅ Competition exploration across ATP, WTA, ITF, Challenger, and more  
✅ Parent–child tournament hierarchy analysis (Singles & Doubles)  
✅ Venue & infrastructure insights across countries and timezones  
✅ Competitor ranking, movement, and performance analysis  
✅ Interactive filters and KPI-driven storytelling  

------------------------------------------------------------------------

📌 **Dashboard Sections:**  

| Section | Description |
|-------|------------|
| 🎾 Competition Overview | Tournament distribution by category, type, gender, and level |
| 🌍 Venue & Complex Insights | Venue density, complexes, country & timezone analysis |
| 🏆 Competitor Rankings | Player rankings, points, movement, and country-level insights |

------------------------------------------------------------------------

📊 **Dashboard & Visuals**  

### Streamlit Dashboard Screens  


<img width="960" height="405" alt="Screenshot (5605)" src="https://github.com/user-attachments/assets/695d154f-9493-43f1-8f53-c09f98461438" />


<img width="960" height="405" alt="Screenshot (5606)" src="https://github.com/user-attachments/assets/9286ab94-06f3-48f9-8934-228212bfc980" />


<img width="953" height="410" alt="Screenshot (5607)" src="https://github.com/user-attachments/assets/28340df2-b0f7-4054-9963-8055613a2a9b" />


------------------------------------------------------------------------

🧠 **Key Insights:**  
- **ITF tournaments dominate** global tennis activity, highlighting their role in player development  
- **Singles and Doubles formats** are nearly equally represented across competitions  
- Major complexes like **Melbourne Park and Roland Garros** host significantly higher venue capacity  
- Rankings show **high stability** among top players week-to-week  
- Tennis talent is **globally distributed**, including strong representation from emerging nations  

------------------------------------------------------------------------

## 📁 **Files in this Repository**  

| File | Description |
|------|-------------|
|`apifetch_categories.py`|	Fetches tennis categories (ATP, ITF, WTA, Challenger, etc.) from the SportRadar API |
|`apifetch_competitions.py`|	Extracts detailed competition data including type, gender, level, and hierarchy |
|`apifetch_complexes.py`|	Retrieves tennis complexes and venue-related information |
|`apifetch_doubles_rankings.py`|	Fetches doubles competitor rankings, points, and movement |
|`insert_competitions.py`|	Transforms and inserts competition data into the MySQL database |
|`config.py`|	Stores database connection details and API configuration |
|`dashboard.py`|	Main Streamlit application for interactive tennis analytics dashboard |
|`game_database.sql`|	SQL script to create database schema and tables |
|`game_query.sql`|	SQL queries used for analytics, KPIs, and dashboard visualizations |
|`requirements.txt`|	Python dependencies required to run the project |

------------------------------------------------------------------------

## 🛠 **Technologies Used**  

- 🐍 **Python** – API integration, JSON parsing, data processing  
- 🧮 **MySQL & SQL** – Relational database design & analytics  
- 📊 **Streamlit** – Interactive dashboard development  
- 📈 **Plotly / Matplotlib** – Visual analytics  
- 🔗 **SportRadar API** – Professional tennis data source  

------------------------------------------------------------------------

## 📈 **Analytical Objectives**  

- How are tennis competitions distributed across categories and levels?  
- What is the balance between **Singles vs Doubles** formats?  
- Which countries and complexes host the most tennis infrastructure?  
- How do player rankings relate to points and movement?  
- Which countries show strong top-end tennis performance?  

------------------------------------------------------------------------

## 🚀 **Future Enhancements**  

- Match-level analytics and score-based insights  
- Historical ranking trend analysis  
- Predictive models for player performance  
- Cloud deployment on **Azure**  
- Power BI integration for executive dashboards  

------------------------------------------------------------------------

## 🙌 **Author**

**BIMAL KUMAR SAINI**  
Data Analyst | SQL • Python • Streamlit • Power BI  
📧 **bimalsaini333@gmail.com**  
🔗 [LinkedIn](https://www.linkedin.com/in/bimalsaini333/) | [GitHub](https://github.com/SainiBimal)

![Visitor Count](https://komarev.com/ghpvc/?username=SainiBimal&style=flat-square)  
![Hits](https://hits.sh/github.com/SainiBimal/Tennis-Analytics-Streamlit.svg?style=flat-square)

