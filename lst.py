import requests
import json
import csv
import io
import os

def fetch_lst_tokens():
    """
    Fetch tokens with 'lst' tag from Jupiter API and extract specific fields
    """
    url = "https://lite-api.jup.ag/tokens/v2/tag?query=lst"

    try:
        response = requests.get(url)
        response.raise_for_status()
        tokens = response.json()

        lst_tokens = []

        for token in tokens:
            if 'tags' in token and 'lst' in token.get('tags', []):
                mcap = token.get('mcap', 0)
                token_info = {
                    'address': token.get('id', 'N/A'),
                    'symbol': token.get('symbol', 'N/A'),
                    'mcap': mcap if mcap else 0
                }
                lst_tokens.append(token_info)

        # Sort by market cap descending and return top 150
        lst_tokens.sort(key=lambda x: x['mcap'], reverse=True)
        top_150 = lst_tokens[:150]

        # Remove mcap from final output
        for token in top_150:
            del token['mcap']

        return top_150

    except Exception as e:
        print(f"Error fetching tokens: {e}")
        return []

def convert_to_csv(lst_tokens):
    """
    Convert list of tokens to CSV format string
    """
    if not lst_tokens:
        return None

    output = io.StringIO()
    fieldnames = ['address', 'symbol']
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for token in lst_tokens:
        writer.writerow(token)

    csv_data = output.getvalue()
    output.close()

    return csv_data

def upload_to_dune(csv_data, api_key):
    """
    Upload CSV data to Dune Analytics
    """
    url = "https://api.dune.com/api/v1/uploads/csv"

    payload = {
        "data": csv_data,
        "description": "LST tokens data from Jupiter API",
        "table_name": "lst_tokens",
        "is_private": False
    }

    headers = {
        "X-DUNE-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print("Successfully uploaded to Dune!")
        print(response.text)
        return True
    except Exception as e:
        print(f"Error uploading to Dune: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def main():
    # Fetch tokens
    lst_tokens = fetch_lst_tokens()

    if not lst_tokens:
        print("No tokens found or error occurred.")
        return

    # Save as JSON for reference
    with open('lst_tokens_output.json', 'w') as f:
        json.dump(lst_tokens, f, indent=2)

    print(f"Found {len(lst_tokens)} LST tokens")
    print(json.dumps(lst_tokens, indent=2))

    # Convert to CSV
    csv_data = convert_to_csv(lst_tokens)

    if csv_data:
        # Save CSV locally for reference
        with open('lst_tokens_output.csv', 'w') as f:
            f.write(csv_data)
        print("\nCSV file created successfully")

        # Upload to Dune
        api_key = 'l2izTVbLIk5N5QRS4UQRNC0UdvmXDXTh'
        upload_to_dune(csv_data, api_key)

if __name__ == "__main__":
    main()
