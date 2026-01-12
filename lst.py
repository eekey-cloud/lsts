import requests
import json

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
                token_info = {
                    'id': token.get('id', 'N/A'),
                    'symbol': token.get('symbol', 'N/A'),
                    'decimals': token.get('decimals', 'N/A'),
                    'circSupply': token.get('circSupply', 'N/A'),
                    'totalSupply': token.get('totalSupply', 'N/A')
                }
                lst_tokens.append(token_info)
        
        return lst_tokens
    
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    lst_tokens = fetch_lst_tokens()
    
    if lst_tokens:
        with open('lst_tokens_output.json', 'w') as f:
            json.dump(lst_tokens, f, indent=2)
        
        print(json.dumps(lst_tokens, indent=2))
    else:
        print("No tokens found or error occurred.")

if __name__ == "__main__":
    main()
