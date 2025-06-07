import os
import json
import pandas as pd

BASE_PATH = "pulse/data/"

def extract_top_user():
    data = []
    path = os.path.join(BASE_PATH, "top/user/country/india/state")

    for state in os.listdir(path):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                file_path = os.path.join(path, state, year, file)
                with open(file_path, 'r') as f:
                    content = json.load(f)
                    year_int = int(year)
                    quarter = int(file.strip('.json').split('.')[0])

                    # Handle districts
                    districts = content['data'].get('districts', [])
                    for item in districts:
                        data.append({
                            'state': state,
                            'year': year_int,
                            'quarter': quarter,
                            'level': 'district',
                            'name': item['name'],
                            'registeredUsers': item['registeredUsers']
                        })

                    # Handle pincodes
                    pincodes = content['data'].get('pincodes', [])
                    for item in pincodes:
                        data.append({
                            'state': state,
                            'year': year_int,
                            'quarter': quarter,
                            'level': 'pincode',
                            'name': item['name'],
                            'registeredUsers': item['registeredUsers']
                        })

    df = pd.DataFrame(data)
    df.to_csv("top_user.csv", index=False)
    print(f"✅ top_user.csv generated with {len(df)} rows.")



extract_top_user()