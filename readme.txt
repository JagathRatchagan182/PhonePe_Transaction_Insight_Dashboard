PhonePe Transaction Insights Dashboard

Data-Driven Dashboard for Exploring PhonePe Transactions, User Engagement, Insurance, and Market Trends Across India


Project Overview

This interactive web dashboard visualizes and analyzes transaction and user engagement data from PhonePe, one of India's leading digital payment platforms. The tool is designed for business intelligence, regional analysis, and data-driven decision making, targeting fintech analysts, policy researchers, and data science learners.

Developed using Streamlit, PostgreSQL, Plotly, and Python, this project covers state- and district-level trends across different time periods and categories.


Features

? **Welcome Page** – Modern and animated welcome section  
? **Dynamic Filters** – Select `Year`, `Quarter`, `State`, `District`  
? **5 Business Use-Cases**:
1. Transaction Dynamics – Total amount of transactions across India
2. Device Dominance & User Engagement – Registered users by brand and region
3. Insurance Penetration – Total insured user base over time
4. Market Expansion Trends – Transaction categories and value analysis
5. District-Level Insurance Engagement – Understand insurance uptake at a micro level

? Geographical Visualization – Using custom Indian GeoJSON maps  
? Interactive Visuals – Built with **Plotly** (Bar Charts, Line Charts)  
? Smart Recommendations – AI-powered business suggestions after each analysis  
? Modular Design – Separate files for queries (`analysis.py`) and frontend (`app.py`)  
Technologies Used

| Tool            | Description                             |
|-----------------|-----------------------------------------|
| Python            | Core programming language               |
| Streamlit         | For interactive frontend UI             |
| PostgreSQL     | Backend relational database             |
| SQLAlchemy   | For database connection and execution   |
| Pandas             | Data handling and preprocessing         |
| Plotly                | Visualization library                   |
| GeoJSON          | Indian state boundaries for maps        |

---

Project Structure
?? Project Folder
?
??? ?? app.py # Streamlit UI logic
??? ?? analysis.py # SQL query functions
??? ?? extract.py # Data fetching from path
??? ?? top_user_extract.py # fetching top_user data
??? ?? db_connect.py # Connection to the postgreSql server
??? ?? db_table.py # updating csv data to the database
??? ?? Pulse/ # Data of Phonepe Transaction, Insurance , User
??? ?? requirements.txt # Required Python packages
??? ?? README.md # Project overview







---

How Each Feature Works

1. Transaction Dynamics
- Aggregates transaction value across India
- Filters by `year`, `quarter`, `state`
- Dynamic bar chart comparing states

2.  Device Dominance & User Engagement
- Shows total registered users by state
- Highlights trends in mobile usage and engagement
- Dynamic bar and line charts based on user filters

 3. Insurance Penetration
- Displays total insured users by region
- Useful for assessing insurance awareness and adoption
- Recommendations suggest target areas for expansion

 4. Market Expansion
- Category-wise transaction trends over time
- Helps identify high-growth service categories
- Time series analysis per region or quarter

#5. District-Level Insurance Engagement
- Fine-grained view of insurance coverage per district
- Identifies underpenetrated zones
- Useful for targeting government schemes or campaigns

---

## Smart Recommendation Engine

At the end of each visualization, evaluates the data and generates insights.

##  How to Run the Project
 ? Prerequisites
- Python 3.10+
- PostgreSQL with PhonePe datasets imported
- GeoJSON file for map "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
















Developer Info
 Developer: Jagath Ratchagan
 Email: jagathratchagank182@gmail.com
 GitHub: github.com/JagathRatchagan182

