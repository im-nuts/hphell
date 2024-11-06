import requests
import json

def hdlookup(keyword):
    # Define the endpoint URL
    url = "https://apionline.homedepot.com/federation-gateway/graphql?opname=searchModel"

    # Load headers from headers.txt
    with open("headers.txt", "r") as file:
        headers = json.load(file)

    # Define variables directly in the script, using the provided keyword
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
        "keyword": keyword,  # Use the user-provided keyword
        "navParam": None,
        "orderBy": {
            "field": "BEST_MATCH",
            "order": "ASC"
        },
        "pageSize": 10,
        "startIndex": 0,
        "storeId": "2511"
    }

    # Load the GraphQL query from the file
    with open("info.graphql", "r") as file:
        graphql_query = file.read()

    # Define the payload with the loaded query and variables
    payload = {
        "operationName": "searchModel",
        "variables": variables,
        "query": graphql_query
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Attempt to prettify the JSON response and extract product details
    try:
        # Parse JSON response
        response_json = response.json()
        
        # Navigate to the 'products' array
        products = response_json.get("data", {}).get("searchModel", {}).get("products", [])

        # List to store extracted product details
        extracted_details = []

        # Extract required fields for each product
        for product in products:
            identifiers = product.get("identifiers", {})
            pricing = product.get("pricing", {})

            # Get required fields
            product_details = {
                "storeSkuNumber": identifiers.get("storeSkuNumber"),
                "canonicalUrl": identifiers.get("canonicalUrl"),
                "itemId": identifiers.get("itemId"),
                "productLabel": identifiers.get("productLabel"),
                "modelNumber": identifiers.get("modelNumber"),
                "priceValue": pricing.get("value")
            }

            # Add to the extracted details list
            extracted_details.append(product_details)

        # Define the final output file
        output_file = "extracted_product_details.txt"

        # Write extracted details to the output file
        with open(output_file, "w") as out_file:
            json.dump(extracted_details, out_file, indent=4)

        print(f"Product details successfully extracted to '{output_file}'.")

    except json.JSONDecodeError:
        print("Error: The response is not valid JSON.")
    except FileNotFoundError as e:
        print(f"Error: The file '{e.filename}' does not exist.")

# Example usage
if __name__ == "__main__":
    keyword_input = input("Enter the search keyword: ")
    hdlookup(keyword_input)
