import pandas as pd
from pathlib import Path

DATASET_PATH = Path(__file__).resolve().parent.parent / "dataset" / "retail_sales.csv"

def demand_forecast():

    df = pd.read_csv(DATASET_PATH)

    result = []

    for index,row in df.iterrows():

        sales = row["sales"]

        if sales > 120:
            demand = "Very High"
        elif sales > 80:
            demand = "High"
        elif sales > 50:
            demand = "Medium"
        else:
            demand = "Low"

        result.append({
            "product": row["product_name"],
            "sales": int(row["sales"]),
            "price": int(row["price"]),
            "forecast": demand
        })

    return result
