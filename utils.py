import pandas as pd
import json


def export_csv(data, filename="products.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def export_json(data, filename="products.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
