import json
import pandas as pd 

def parse_raw_content(raw_content_str):
    "parse str to Dict"

    if pd.isna(raw_content_str):
        return {}
    
    try:
        return json.loads(raw_content_str.replace("'", "\""))    
    except(json.JSONDecodeError, TypeError):
        return {}
    
def extract_unique_from_raw_content(df, key):
    "extract unique values from raw_content by specific key"

    all_values = []
    parsed_content = df["raw_content"].apply(parse_raw_content)

    for item in parsed_content:
        value = item.get(key)
        
        if value:
            if isinstance(value, list):
                all_values.extend(value)
            else:
                all_values.append(value)
    return pd.Series(all_values).drop_duplicates().tolist()