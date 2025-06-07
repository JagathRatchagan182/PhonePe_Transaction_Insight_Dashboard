# extract_data.py

import pandas as pd
from db_connect import engine

df = pd.read_csv("aggregated_transaction.csv")
df.to_sql('aggregated_transaction', engine, index=False, if_exists='replace')
df = pd.read_csv("aggregated_insurance.csv")
df.to_sql('aggregated_insurance', engine, index=False, if_exists='replace')
df = pd.read_csv("aggregated_user.csv")
df.to_sql('aggregated_user', engine, index=False, if_exists='replace')
df = pd.read_csv("map_insurance.csv")
df.to_sql('map_insurance', engine, index=False, if_exists='replace')
df = pd.read_csv("map_transaction.csv")
df.to_sql('map_transaction', engine, index=False, if_exists='replace')
df = pd.read_csv("map_user.csv")
df.to_sql('map_user', engine, index=False, if_exists='replace')
df = pd.read_csv("top_transaction.csv")
df.to_sql('top_transaction', engine, index=False, if_exists='replace')
df = pd.read_csv("top_insurance.csv")
df.to_sql('top_insurance', engine, index=False, if_exists='replace')
df = pd.read_csv("top_user.csv")
df.to_sql('top_user', engine, index=False, if_exists='replace')
print("Data loaded to PostgreSQL ✅")
