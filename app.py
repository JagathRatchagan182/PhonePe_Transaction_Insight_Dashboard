# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import analysis
import requests

# DB Connection
engine = create_engine('postgresql://postgres:Admin@localhost:5432/phonepe_db1')

# GeoJSON URL
geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
india_states = requests.get(geojson_url).json()



# Streamlit UI Config
st.set_page_config(layout="wide", page_title="PhonePe Dashboard")
st.title("📱 PhonePe Transaction Insights Dashboard")
st.markdown("#### 👨‍💻 Designed & Developed by Jagath Ratchagan")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
years = analysis.get_years(engine)
states = ["All"] + analysis.get_states(engine)
quarters = [1, 2, 3, 4]

year = st.sidebar.selectbox("Year", years)
quarter = st.sidebar.selectbox("Quarter", quarters)
state_filter = st.sidebar.selectbox("State (for user/device views)", states)

# Use Case Selector
option = st.sidebar.radio("Select Business Use Case", (
    "Welcome Page",
    "Transaction Dynamics",
    "User Engagement Growth",
    "Insurance Penetration",
    "Market Expansion",
    "Insurance Engagement Trend"
))

# ========== WELCOME PAGE ==========
if option == "Welcome Page":
    st.markdown("""
        <style>
            .welcome-box {
                background-color: #f0f4ff;
                border-radius: 12px;
                padding: 30px;
                text-align: center;
                box-shadow: 0 4px 10px rgba(108, 99, 255, 0.2);
                animation: fadeIn 1.2s ease-in-out;
            }
            .welcome-title {
                color: #6c63ff;
                font-size: 48px;
                font-weight: 800;
                margin-bottom: 10px;
            }
            .welcome-author {
                font-size: 22px;
                font-weight: 600;
                color: #4b4b4b;
                margin-bottom: 10px;
            }
            .welcome-subtitle {
                font-size: 18px;
                color: #333;
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(-10px);}
                to {opacity: 1; transform: translateY(0);}
            }
        </style>
        <div class="welcome-box">
            <div class="welcome-title">📊 PhonePe Transaction Insights</div>
            <div class="welcome-subtitle">Explore the dynamics of PhonePe transactions, insurance growth, market expansion, and user engagement across India!</div>
        </div>
    """, unsafe_allow_html=True)


# ========== CASE STUDY 1: Transaction Dynamics ==========
elif option == "Transaction Dynamics":
    df = analysis.get_transaction_dynamics(engine, year, quarter)
    df['state'] = df['state'].map({
    "andaman-&-nicobar-islands": "andaman-&-nicobar-islands",
    "andhra-pradesh": "andhra-pradesh",
    "arunachal-pradesh": "arunachal-pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
    "delhi": "Delhi",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal-pradesh": "Himachal Pradesh",
    "jammu-&-kashmir": "Jammu & Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "ladakh": "Ladakh",
    "madhya-pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "puducherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil-nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttarakhand": "Uttarakhand",
    "uttar-pradesh": "Uttar Pradesh",
    "west-bengal": "West Bengal"
    })
    df['state'] = df['state'].str.strip().str.title()
    if df.empty:
        st.warning("⚠️ There is no specific data in this time period.")
    else:

        fig_map = px.choropleth(df, geojson=india_states, featureidkey='properties.ST_NM',
                                locations='state', color='total_amount',
                                color_continuous_scale='Reds',
                                title=f"Transactions by State - {year} Q{quarter}")
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)

        if state_filter == "All":
            fig = px.bar(df, x='state', y='total_amount', title="Transaction Volume by State")
        else:   
            fig = px.pie(df, names='state', values='total_amount',
                         title=f"Transaction Volume in {state_filter}")

        st.plotly_chart(fig, use_container_width=True)
        st.write(df)
        st.markdown("### 📊 Recommendations")
        rec = analysis.get_recommendation_for_transaction_dynamics(df)
        st.success(rec)

# ========== CASE STUDY 2: User Engagement Growth ==========
elif option == "User Engagement Growth":
    df = analysis.get_user_engagement(engine, year, quarter, state_filter)
    if df.empty:
        st.warning("⚠️ There is no specific data in this time period.")
    else:
        if state_filter == "All":
            fig_bar = px.bar(df, x='state', y='total_users', color='state',
                             title=f"Registered Users by State - {year} Q{quarter}")
            st.plotly_chart(fig_bar, use_container_width=True)

            fig_line = px.line(df.sort_values("total_users", ascending=False),
                               x='state', y='total_users', markers=True,
                               title="User Engagement Line Chart")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            fig_line = px.line(df, x='quarter', y='total_users', markers=True,
                               title=f"User Growth Trend - {state_filter}, {year}")
            st.plotly_chart(fig_line, use_container_width=True)

            fig_bar = px.bar(df, x='quarter', y='total_users', title="Quarterly User Growth")
            st.plotly_chart(fig_bar, use_container_width=True)
        st.write(df)
        st.markdown("### 📊 Recommendations")
        is_all = state_filter == "All"
        rec = analysis.get_recommendation_for_user_engagement(df, all_states=is_all)
        st.success(rec)

# ========== CASE STUDY 3: Insurance Penetration ==========
elif option == "Insurance Penetration":
    df = analysis.get_insurance_penetration(engine, year, quarter)
    df['state'] = df['state'].map({
    "Andaman-&-Nicobar-Islands": "Andaman & Nicobar",
    "Andhra-Pradesh": "Andhra Pradesh",
    "Arunachal-Pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    "dadra-&-nagar-haveli-&-daman-&-diu": "Dadra and Nagar Haveli and Daman and Diu",
    "delhi": "Delhi",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal-pradesh": "Himachal Pradesh",
    "jammu-&-kashmir": "Jammu & Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "ladakh": "Ladakh",
    "madhya-pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "puducherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil-nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttarakhand": "Uttarakhand",
    "uttar-pradesh": "Uttar Pradesh",
    "west-bengal": "West Bengal"
    })
    df['state'] = df['state'].str.strip().str.title()
    
    if df.empty:
        st.warning("⚠️ There is no specific data in this time period.")
    else:
        fig_map = px.choropleth(df,
                                geojson=india_states,
                                featureidkey='properties.ST_NM',
                                locations='state',
                                color='insurance_value',
                                color_continuous_scale='Greens',
                                title=f"Insurance Value by State - {year} Q{quarter}")
        fig_map.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_map, use_container_width=True)

        fig_bar = px.bar(df.sort_values("insurance_value", ascending=False),
                         x='state', y='insurance_value', title="Insurance Value by State")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.write(df)
        st.markdown("### 📊 Recommendations")
        rec = analysis.get_recommendation_for_insurance_penetration(df)
        st.success(rec)

# ========== CASE STUDY 4: Market Expansion ==========
elif option == "Market Expansion":
    df = analysis.get_market_expansion(engine)
    if df.empty:
        st.warning("⚠️ There is no specific data in this time period.")
    else:
        fig_pie = px.pie(df.nlargest(10, 'total_amount'), names='state', values='total_amount',
                         title="Top 10 States by Transaction Value")
        st.plotly_chart(fig_pie, use_container_width=True)

        fig_bar = px.bar(df.sort_values("total_amount", ascending=False),
                         x='state', y='total_amount', title="Market Share by State")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.write(df)
        st.markdown("### 📊 Recommendations")
        rec = analysis.get_recommendation_for_market_expansion(df)
        st.success(rec)

# ========== CASE STUDY 5: Insurance Engagement Trend ==========
elif option == "Insurance Engagement Trend":
    df = analysis.get_insurance_engagement_trend(engine)
    if df.empty:
        st.warning("⚠️ There is no specific data in this time period.")
    else:
        fig_line = px.line(df, x='quarter', y='avg_insurance_amount', color='year',
                           markers=True, title="Average Insurance Amount Over Time")
        st.plotly_chart(fig_line, use_container_width=True)

        fig_bar = px.bar(df, x='quarter', y='avg_insurance_amount', color='year',
                         title="Average Insurance by Quarter & Year")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.write(df)
        st.markdown("### 📊 Recommendations")
        rec = analysis.get_recommendation_for_insurance_engagement_trend(df)
        st.success(rec)
