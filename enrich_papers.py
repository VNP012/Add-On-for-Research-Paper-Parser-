import pandas as pd
import requests
import time

API_KEY = "YOUR_API_KEY"   # replace with your Semantic Scholar API key
HEADERS = {"x-api-key": API_KEY}
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def enrich_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    enriched = []

    for _, row in df.iterrows():
        query = row["Title"]
        params = {"query": query, "limit": 1, "fields": "title,year,venue,doi,url"}
        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code == 200:
            data = response.json().get("data", [])
            if data:
                paper = data[0]
                enriched.append({
                    "Title": paper.get("title"),
                    "Year": paper.get("year"),
                    "Venue": paper.get("venue"),
                    "DOI": paper.get("doi"),
                    "URL": paper.get("url")
                })
        else:
            enriched.append({
                "Title": row["Title"],
                "Year": row["Year"],
                "Venue": row["Venue"],
                "DOI": None,
                "URL": None
            })
        time.sleep(1)  # respect API rate limits

    pd.DataFrame(enriched).to_csv(output_csv, index=False)
    print(f"✅ Done! Enriched file saved as {output_csv}")

if __name__ == "__main__":
    input_csv = input("Enter path to input CSV: ")
    output_csv = "enriched_" + input_csv.split("/")[-1]
    enrich_csv(input_csv, output_csv)
