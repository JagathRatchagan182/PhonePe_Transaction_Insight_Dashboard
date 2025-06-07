import pandas as pd

# ------------------ Data Fetching Functions ------------------ #

def get_years(engine):
    return pd.read_sql("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year", engine)['year'].tolist()

def get_states(engine):
    return pd.read_sql("SELECT DISTINCT state FROM aggregated_transaction ORDER BY state", engine)['state'].tolist()

def get_transaction_dynamics(engine, year: int, quarter: int):
    query = f"""
        SELECT state, SUM(amount) AS total_amount
        FROM aggregated_transaction
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY state
    """
    return pd.read_sql(query, engine)

def get_user_engagement(engine, year: int, quarter: int, state: str = None):
    if state and state != "All":
        query = f"""
            SELECT quarter, SUM("registeredUsers") AS total_users
            FROM top_user
            WHERE year = {year} AND state = '{state}'
            GROUP BY quarter
            ORDER BY quarter
        """
    else:
        query = f"""
            SELECT state, SUM("registeredUsers") AS total_users
            FROM top_user
            WHERE year = {year} AND quarter = {quarter}
            GROUP BY state
            ORDER BY total_users DESC
        """
    return pd.read_sql(query, engine)

def get_insurance_penetration(engine, year: int, quarter: int):
    query = f"""
        SELECT state, SUM(amount) AS insurance_value
        FROM aggregated_insurance
        WHERE year = {year} AND quarter = {quarter}
        GROUP BY state
    """
    return pd.read_sql(query, engine)

def get_market_expansion(engine):
    query = """
        SELECT state, SUM(amount) AS total_amount
        FROM aggregated_transaction
        GROUP BY state
        ORDER BY total_amount DESC 
        LIMIT 10
    """
    return pd.read_sql(query, engine)

def get_insurance_engagement_trend(engine):
    query = """
        SELECT year, quarter, AVG(amount) AS avg_insurance_amount
        FROM aggregated_insurance
        GROUP BY year, quarter
        ORDER BY year, quarter
    """
    return pd.read_sql(query, engine)

# ------------------ Recommendation Functions ------------------ #

def get_recommendation_for_transaction_dynamics(df: pd.DataFrame) -> str:
    mean_amount = df['total_amount'].mean()
    high_states = df[df['total_amount'] > mean_amount]['state'].tolist()
    low_states = df[df['total_amount'] <= mean_amount]['state'].tolist()

    return (
        f"📈 High-performing states with above-average transaction amounts: {', '.join(map(str,high_states))}.\n"
        f"⚠️ States with below-average transaction amounts that require strategic focus: {', '.join(map(str,low_states))}.\n"
        "👉 Consider targeted promotions or service improvements in low-performing states to boost transactions."
    )

def get_recommendation_for_user_engagement(df: pd.DataFrame, all_states: bool = True) -> str:
    if all_states:
        mean_users = df['total_users'].mean()
        strong_states = df[df['total_users'] > mean_users]['state'].tolist()
        weak_states = df[df['total_users'] <= mean_users]['state'].tolist()

        return (
            f"⚡ States with strong registered user bases: {', '.join(map(str,strong_states))}.\n"
            f"⚠️ States with lower user engagement: {', '.join(map(str,weak_states))}.\n"
            "👉 Focus on marketing and app feature optimization in lower engagement states."
        )
    else:
        trend = df['total_users'].diff().mean()
        if trend > 0:
            return "📶 User engagement shows a positive growth trend. Continue enhancing user experience."
        else:
            return "⚠️ User engagement is declining. Investigate causes like app issues or competition and act accordingly."

def get_recommendation_for_insurance_penetration(df: pd.DataFrame) -> str:
    mean_insurance_value = df['insurance_value'].mean()
    high_penetration = df[df['insurance_value'] > mean_insurance_value]['state'].tolist()
    low_penetration = df[df['insurance_value'] <= mean_insurance_value]['state'].tolist()

    return (
        f"✅ States with strong insurance transaction values: {', '.join(map(str,high_penetration))}.\n"
        f"🚩 States with lower insurance uptake: {', '.join(map(str,low_penetration))}.\n"
        "👉 Prioritize marketing campaigns and insurer partnerships in low-penetration states to boost adoption."
    )

def get_recommendation_for_market_expansion(df: pd.DataFrame) -> str:
    top_states = df.sort_values(by='total_amount', ascending=False).head(5)['state'].tolist()

    return (
        f"🏆 Top 5 states by transaction value: {', '.join(map(str,top_states))}.\n"
        "🌟 Explore deeper market penetration and tailor services for these states.\n"
        "🔍 Investigate states outside top 10 for potential growth opportunities."
    )

def get_recommendation_for_insurance_engagement_trend(df: pd.DataFrame) -> str:
    trend_by_year = df.groupby('year')['avg_insurance_amount'].mean().reset_index()
    
    if len(trend_by_year) < 2:
        return "ℹ️ Not enough data to determine insurance trend over years."

    recent_trend = trend_by_year.iloc[-1]['avg_insurance_amount'] - trend_by_year.iloc[-2]['avg_insurance_amount']

    if recent_trend > 0:
        return "📈 Insurance average transaction amounts are increasing year-over-year. Maintain momentum with new insurance products."
    else:
        return "⚠️ Recent decline in average insurance transaction amounts detected. Assess product offerings and user feedback to improve."
