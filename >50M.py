import requests
import json
import csv
import io

def fetch_verified_tokens():
    """
    Fetch verified tokens from Jupiter API and filter by mcap > 50M
    """
    url = "https://lite-api.jup.ag/tokens/v2/tag?query=verified"

    try:
        response = requests.get(url)
        response.raise_for_status()
        tokens = response.json()

        tokens_50m = []

        for token in tokens:
            mcap = token.get('mcap', 0)

            # Filter tokens with market cap > 50 million
            if mcap and mcap > 50000000:
                token_info = {
                    'address': token.get('id', 'N/A'),
                    'symbol': token.get('symbol', 'N/A'),
                    'mcap': int(mcap) if isinstance(mcap, (int, float)) else 0
                }
                tokens_50m.append(token_info)
                print(f"Found: {token_info['symbol']} - ${mcap:,.0f}")

        # Sort by market cap descending
        tokens_50m.sort(key=lambda x: x['mcap'], reverse=True)

        return tokens_50m

    except Exception as e:
        print(f"Error fetching tokens: {e}")
        return []

def convert_to_csv(tokens_data):
    """
    Convert list of tokens to CSV format string
    """
    if not tokens_data:
        return None

    output = io.StringIO()
    fieldnames = ['address', 'symbol', 'mcap']
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for token in tokens_data:
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
        "description": "Verified tokens with >50M market cap from Jupiter API",
        "table_name": "tokens_50m",
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
    # Fetch verified tokens with mcap > 50M
    tokens_data = fetch_verified_tokens()

    if not tokens_data:
        print("No tokens found with mcap > 50M.")
        return

    # Save as JSON for reference
    with open('tokens_50m_output.json', 'w') as f:
        json.dump(tokens_data, f, indent=2)

    print(f"\nFound {len(tokens_data)} verified tokens with >$50M market cap")

    # Convert to CSV
    csv_data = convert_to_csv(tokens_data)

    if csv_data:
        # Save CSV locally for reference
        with open('tokens_50m_output.csv', 'w') as f:
            f.write(csv_data)
        print("CSV file created successfully")

        # Upload to Dune
        api_key = 'l2izTVbLIk5N5QRS4UQRNC0UdvmXDXTh'
        upload_to_dune(csv_data, api_key)

if __name__ == "__main__":
    main()
