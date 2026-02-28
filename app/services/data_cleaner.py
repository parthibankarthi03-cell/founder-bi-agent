# app/services/data_cleaner.py

import pandas as pd

def clean_data(raw_data, trace):
    trace.add("Cleaning Data", {})

    if raw_data is None:
        return pd.DataFrame()
    
    # Convert dict/list-of-dict to DataFrame
    if isinstance(raw_data, dict):
        raw_data = [raw_data]  # wrap single dict in a list

    cleaned_df = pd.DataFrame(raw_data)
    
    # Optional cleaning steps
    if "revenue" in cleaned_df.columns:
        cleaned_df["revenue"] = pd.to_numeric(cleaned_df["revenue"], errors="coerce").fillna(0)
    
    # Here you can add more cleaning steps:
    # - Handle nulls
    # - Normalize revenue
    # - Standardize sector names
    # - Parse dates

    trace.add("Data Cleaned", {"rows": len(cleaned_df)})
    return cleaned_df