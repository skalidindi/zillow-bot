import httpx
import os

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# import json

params = {
    "location": "north carolina",
    "status_type": "ForSale",
    "home_type": "Houses, Multi-family",
    "sort": "Newest",
    "minPrice": "300000",
    "maxPrice": "600000",
    "rentMinPrice": "2000",
}


def fetch_properties():
    print("Fetching properties...")
    data = fetch_api()
    properties = data["props"] if "props" in data else []

    if data["totalPages"] > 1:
        lastPage = min(data["totalPages"], 5)
        for page in range(2, lastPage + 1):
            params["page"] = page
            more_data = fetch_api()
            properties += more_data["props"] if "props" in more_data else []

    # Optional: Save props to a file to debug
    # with open("data.json", "w", encoding="utf-8") as f:
    #     json.dump(data, f, indent=4)

    return data["props"]


def fetch_api():
    api_url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com",
    }

    response = httpx.get(api_url, headers=headers, params=params)
    remaining_requests = response.headers["x-ratelimit-requests-remaining"]

    print(f"Remaining requests: {remaining_requests}")

    return response.json()
