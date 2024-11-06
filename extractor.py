import requests
import json

url = "https://apionline.homedepot.com/federation-gateway/graphql?opname=searchModel"

with open("headers.txt", "r") as file:
    headers = json.load(file)

keyword = input("Enter the search keyword: ")

variables = {
    "skipInstallServices": False,
    "skipFavoriteCount": False,
    "storefilter": "ALL",
    "channel": "DESKTOP",
    "skipDiscoveryZones": False,
    "skipBuyitagain": True,
    "additionalSearchParams": {
        "sponsored": False
    },
    "keyword": keyword,  
    "navParam": None,
    "orderBy": {
        "field": "BEST_MATCH",
        "order": "ASC"
    },
    "pageSize": 32,
    "startIndex": 0,
}

with open("info.graphql", "r") as file:
    graphql_query = file.read()

payload = {
    "operationName": "searchModel",
    "variables": variables,
    "query": graphql_query
}

response = requests.post(url, headers=headers, json=payload)

try:
    response_json = response.json()
    
    products = response_json.get("data", {}).get("searchModel", {}).get("products", [])

    extracted_details = []

    for product in products:
        identifiers = product.get("identifiers", {})
        pricing = product.get("pricing", {})

        product_details = {
            "storeSkuNumber": identifiers.get("storeSkuNumber"),
            "canonicalUrl": identifiers.get("canonicalUrl"),
            "itemId": identifiers.get("itemId"),
            "productLabel": identifiers.get("productLabel"),
            "modelNumber": identifiers.get("modelNumber"),
            "priceValue": pricing.get("value")
        }

        extracted_details.append(product_details)

    output_file = "extracted_product_details.txt"

    with open(output_file, "w") as out_file:
        json.dump(extracted_details, out_file, indent=4)

    print(f"Product details successfully extracted to '{output_file}'.")

except json.JSONDecodeError:
    print("Error: The response is not valid JSON.")
except FileNotFoundError as e:
    print(f"Error: The file '{e.filename}' does not exist.")
