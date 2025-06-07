import os
import json
import pandas as pd

BASE_PATH = "pulse/data/"

def extract_aggregated_transaction():
    data = []
    path = os.path.join(BASE_PATH, "aggregated/transaction/country/india/state")
    for state in os.listdir(path):
        for year in os.listdir(f"{path}/{state}"):
            for file in os.listdir(f"{path}/{state}/{year}"):
                with open(f"{path}/{state}/{year}/{file}") as f:
                    content = json.load(f)
                    if content['data']['transactionData'] is not None:
                        for tx in content['data']['transactionData']:
                            data.append({
                                'state': state,
                                'year': int(year),
                                'quarter': int(file.strip('.json').split('.')[0]),
                                'type': tx['name'],
                                'count': tx['paymentInstruments'][0]['count'],
                                'amount': tx['paymentInstruments'][0]['amount']
                            })
    pd.DataFrame(data).to_csv("aggregated_transaction.csv", index=False)

def extract_aggregated_user():
    data = []
    path = os.path.join(BASE_PATH, "aggregated/user/country/india/state")
    for state in os.listdir(path):
        for year in os.listdir(f"{path}/{state}"):
            for file in os.listdir(f"{path}/{state}/{year}"):
                with open(f"{path}/{state}/{year}/{file}") as f:
                    content = json.load(f)
                    users = content['data'].get('usersByDevice')
                    if users:
                        for user in users:
                            data.append({
                                'state': state,
                                'year': int(year),
                                'quarter': int(file.strip('.json').split('.')[0]),
                                'brand': user['brand'],
                                'count': user['count'],
                                'percentage': user['percentage']
                            })
    pd.DataFrame(data).to_csv("aggregated_user.csv", index=False)

def extract_aggregated_insurance():
    data = []
    path = os.path.join(BASE_PATH, "aggregated/insurance/country/india/state")
    for state in os.listdir(path):
        for year in os.listdir(f"{path}/{state}"):
            for file in os.listdir(f"{path}/{state}/{year}"):
                with open(f"{path}/{state}/{year}/{file}") as f:
                    content = json.load(f)
                    if content['data']['transactionData'] is not None:
                        for tx in content['data']['transactionData']:
                            data.append({
                                'state': state,
                                'year': int(year),
                                'quarter': int(file.strip('.json').split('.')[0]),
                                'type': tx['name'],
                                'count': tx['paymentInstruments'][0]['count'],
                                'amount': tx['paymentInstruments'][0]['amount']
                            })
    pd.DataFrame(data).to_csv("aggregated_insurance.csv", index=False)

def extract_map(table_name, level):
    data = []
    path = os.path.join(BASE_PATH, f"map/{table_name}/hover/country/india/{level}")
    for state in os.listdir(path):
        for year in os.listdir(f"{path}/{state}"):
            for file in os.listdir(f"{path}/{state}/{year}"):
                with open(f"{path}/{state}/{year}/{file}") as f:
                    content = json.load(f)
                    file_quarter = int(file.strip('.json').split('.')[0])

                    # ✅ For user: hoverData is a dict, not a list
                    if table_name == "user":
                        hover_data = content['data'].get('hoverData') or {}
                        for district, metrics in hover_data.items():
                            data.append({
                                'state': state,
                                'district': district,
                                'year': int(year),
                                'quarter': file_quarter,
                                'registeredUsers': metrics.get('registeredUsers', 0),
                                'appOpens': metrics.get('appOpens', 0)
                            })

                    # ✅ For others: same logic as before (hoverDataList)
                    else:
                        data_list = content['data'].get('hoverDataList') or []
                        for item in data_list:
                            data.append({
                                'state': state,
                                'district': item['name'],
                                'year': int(year),
                                'quarter': file_quarter,
                                'count': item['metric'][0]['count'],
                                'amount': item['metric'][0]['amount']
                            })

    pd.DataFrame(data).to_csv(f"map_{table_name}.csv", index=False)
    print(f"✅ map_{table_name}.csv generated with {len(data)} rows.")


def extract_top(table_name):
    data = []
    path = os.path.join(BASE_PATH, f"top/{table_name}/country/india/state")

    for state in os.listdir(path):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                file_path = os.path.join(path, state, year, file)
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    data_key = None

                    if 'districts' in content['data']:
                        data_key = 'districts'
                    elif 'pincodes' in content['data']:
                        data_key = 'pincodes'
                    elif 'states' in content['data']:
                        data_key = 'states'

                    if data_key:
                        for item in content['data'][data_key]:
                            metric = item.get('metric')
                            if not metric:
                                continue  # Skip if 'metric' key is missing

                            entity = item.get('entityName') or item.get('name') or 'Unknown'
                            data.append({
                                'state': state,
                                'year': int(year),
                                'quarter': int(file.strip('.json').split('.')[0]),
                                'entity_name': entity,
                                'count': metric.get('count', 0),
                                'amount': metric.get('amount', 0.0)
                            })

    df = pd.DataFrame(data)
    df.to_csv(f"top_{table_name}.csv", index=False)
    print(f"✅ top_{table_name}.csv generated with {len(df)} rows.")


# Run all extraction functions
extract_aggregated_transaction()
extract_aggregated_user()
extract_aggregated_insurance()
extract_map("transaction", "state")
extract_map("user", "state")
extract_map("insurance", "state")
extract_top("transaction")
extract_top("user")
extract_top("insurance")

print("✅ All CSV files have been generated.")
