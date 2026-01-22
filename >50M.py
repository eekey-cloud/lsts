import requests
import json
import csv
import io

# Tokens with >50M market cap
TOKENS_50M = [
    {'address': 'pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn', 'symbol': 'PUMP'},
    {'address': '27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4', 'symbol': 'JLP'},
    {'address': '6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN', 'symbol': 'TRUMP'},
    {'address': 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263', 'symbol': 'BONK'},
    {'address': '2zMMhcVQEXDtdE6vsFS7S7D5oUodfJHE8vd1gnBouauv', 'symbol': 'PENGU'},
    {'address': 'JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN', 'symbol': 'JUP'},
    {'address': 'J6pQQ3FAcJQeWPPGppWRb4nM8jU3wLyYbRrLh7feMfvd', 'symbol': '2Z'},
    {'address': 'Dfh5DzRgSvvCFDoYc2ciTkMrbDfRKybA4SoFbPmApump', 'symbol': 'PIPPIN'},
    {'address': 'EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm', 'symbol': 'WIF'},
    {'address': 'HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3', 'symbol': 'PYTH'},
    {'address': '9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump', 'symbol': 'FARTCOIN'},
    {'address': 'ZBCNpuD7YMXzTHB2fhGkGi78MNsHGLRXUhRewNRm9RU', 'symbol': 'ZBCN'},
    {'address': '4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R', 'symbol': 'RAY'},
    {'address': 'SKRbvo6Gf7GondiT3BbTfuRDPqLWei4j2Qy2NPGZhW3', 'symbol': 'SKR'},
    {'address': 'hntyVP6YFm1Hg25TN9WGLqM12b8TQmcknKrdu1oxWux', 'symbol': 'HNT'},
    {'address': '8fr7WGTVFszfyNWRMXj6fRjZZAnDwmXwEpCrtzmUkdih', 'symbol': 'wYLDS'},
    {'address': 'KMNo3nJsBXfcpJTVhZcXLW7RmTwTt4GVFE7suUBo9sS', 'symbol': 'KMNO'},
    {'address': '2FPyTwcZLUg1MDrwsyoP4D6s1tM7hAkHYRjkNb5w6Pxk', 'symbol': 'SolletETH'},
    {'address': 'jtojtomepa8beP8AuQc6eXt5FriJwfFMwQx2v2f9mCL', 'symbol': 'JTO'},
    {'address': 'FUAfBo2jgks6gB4Z4LfZkqSZgzNucisEHqnNebaRxM1P', 'symbol': 'MELANIA'},
    {'address': '59obFNBzyTBGowrkif5uK7ojS58vsuWz3ZCvg6tfZAGw', 'symbol': 'PST'},
    {'address': 'METvsvVRapdj9cFLzq4Tr43xK4tAjQfwX76z3n6mWQL', 'symbol': 'MET'},
    {'address': 'Grass7B4RdKfBCjTKgSqnXkqjwiGvQyFbuSCUJr3XXjs', 'symbol': 'GRASS'},
    {'address': 'J1Wpmugrooj1yMyQKrdZ2vwRXG5rhfx3vTnYE39gpump', 'symbol': 'WOULD'},
    {'address': 'rndrizKT3MK1iimdxRdWabcF7Zg7AR5T4nud4EkHBof', 'symbol': 'RENDER'},
    {'address': '5XZw2LKTyrfvfiskJ78AMpackRjPcyCif1WhUsPDuVqQ', 'symbol': 'WBTC'},
    {'address': '3NZ9JMVBmGAqocybic2c7LQCJScmgsAZ6vQqTDzcqmJh', 'symbol': 'WBTC(Wormhole)'},
    {'address': 'cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij', 'symbol': 'cbBTC'},
    {'address': '5oVNBeEEQvYi1cX3ir8Dx5n1P7pdxydbGF2X4TxVusJm', 'symbol': 'INF'},
    {'address': '85VBFQZC9TZkfaptBWjvUw7YbZjy52A6mjtPGjstQAmQ', 'symbol': 'W'},
    {'address': '6wQDzAZT17HYABu7rNXBDUSgNzDeGUUUzY2cS8wpEGAc', 'symbol': 'ECOR'},
    {'address': '7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs', 'symbol': 'ETH(Wormhole)'},
    {'address': 'MEFNBXixkEbait3xn9bkm8WsJzXtVsaJEn4c8Sam21u', 'symbol': 'ME'},
    {'address': 'METAwkXcqyXKy1AtsSgJ8JiUHwGCafnZL38n3vYmeta', 'symbol': 'METADAO'},
    {'address': 'METADDFL6wWMWEoKTFJwcThTbUmtarRJZjRpzUvkxhr', 'symbol': 'META'},
    {'address': 'HUMA1821qVDKta3u2ovmfDQeW2fSQouSKE8fkF44wvGw', 'symbol': 'HUMA'},
    {'address': 'LBTCgU4b3wsFKsPwBn1rRZDx5DoFutM6RPiEt1TPDsY', 'symbol': 'LBTC'},
    {'address': 'SonicxvLud67EceaEzCLRnMTBqzYUUYNr93DBkBdDES', 'symbol': 'SONIC'},
    {'address': 'WETZjtprkDMCcUxPi9PfWnowMRZkiGGHDb9rABuRZ2U', 'symbol': 'WET'},
    {'address': 'HNg5PYJmtqcmzXrv6S9zP1CDKk5BgDuyFBxbvNApump', 'symbol': 'ALCH'},
    {'address': 'FkiJSGKDMjRip1MFKa4bxVUtZBA2hkpBHdTfEW8E4iQj', 'symbol': 'ANB'},
    {'address': 'BZLbGTNCSFfoth2GYDtwr7e4imWzpR5jqcUuGEwr646K', 'symbol': 'IO'},
    {'address': '5Y8NV33Vv7WbnLfq3zBcKSdYPrk7g2KoiQoe7M2tcxp5', 'symbol': 'ONyc'},
    {'address': 'SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt', 'symbol': 'SRM'},
    {'address': 'GAehkgN1ZDNvavX81FmzCcwRnzekKMkSyUNq8WkMsjX1', 'symbol': 'SWOP'},
    {'address': '3bSGpKYPut6RXDxp41nvb2GM7eR4kEmJExFFHoYkW3w2', 'symbol': 'LUX'},
    {'address': 'DriFtupJYLTosbwoN8koMbEYSx54aFAVLddWsbksjwg7', 'symbol': 'DRIFT'},
    {'address': 'MEW1gQWJ3nEXg2qgERiKu7FAFj79PHvQVREQUzScPP5', 'symbol': 'MEW'},
    {'address': 'FWGWrsrvgcz1w6LjSSnuHB5y6KyWXhUKjLWhvDSJ48hE', 'symbol': 'FROG'},
    {'address': 'DBRiDgJAMsM95moTzJs7M9LnkGErpbv9v6CUR1DXnUu5', 'symbol': 'DBR'},
    {'address': '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr', 'symbol': 'POPCAT'},
    {'address': 'Dz9mQ9NzkBcCsuGPFJ3r1bS4wgqKMHBPiVuniW8Mbonk', 'symbol': 'USELESS'},
    {'address': '9PR7nCP9DpcUotnDPVLUBUZKu5WAYkwrCUx9wDnSpump', 'symbol': 'Ban'},
    {'address': 'Hg8bKz4mvs8KNj9zew1cEF9tDw1x2GViB4RFZjVEmfrD', 'symbol': 'TDCCP'},
    {'address': '2qEHjDLDLbuBgRYvsxhc5D6uDWAivNFZGan56P1tpump', 'symbol': 'PNUT'},
    {'address': 'BCNT4t3rv5Hva8RnUtJUJLnxzeFAabcYp8CghC1SmWin', 'symbol': 'BC'},
    {'address': '61V8vBaqAGMpgDQi4JcAwo1dmBGHsyhzodcPqnEVpump', 'symbol': 'ARC'},
    {'address': 'ED5nyyWEzpPPiWimP8vYm7sD7TD3LAt3Q3gRTWHzPJBY', 'symbol': 'MOODENG'},
    {'address': 'J3umBWqhSjd13sag1E1aUojViWvPYA5dFNyqpKuX3WXj', 'symbol': 'HOME'},
    {'address': 'orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE', 'symbol': 'ORCA'},
    {'address': 'FeR8VBqNRSUD5NtXAj2n3j1dAHkZHfyDktKuLXD4pump', 'symbol': 'jellyjelly'},
    {'address': '2Wu1g2ft7qZHfTpfzP3wLdfPeV1is4EwQ3CXBfRYAciD', 'symbol': 'GOHOME'},
    {'address': 'a3W4qutoEJA4232T2gwZUfgYJTetr96pU4SJMwppump', 'symbol': 'WhiteWhale'},
    {'address': 'ZEXy1pqteRu3n13kdyh4LwPQknkFk3GzmMYMuNadWPo', 'symbol': 'ZETA'},
    {'address': 'z3dn17yLaGMKffVogeFHQ9zWVcXgqgf3PQnDsNs2g6M', 'symbol': 'OXY'},
]

def get_tokens_50m_data():
    """
    Return the hardcoded >50M tokens list
    """
    return TOKENS_50M

def convert_to_csv(tokens_data):
    """
    Convert list of tokens to CSV format string
    """
    if not tokens_data:
        return None

    output = io.StringIO()
    fieldnames = ['address', 'symbol']
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
        "description": "Tokens with >50M market cap",
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
    # Get tokens data
    tokens_data = get_tokens_50m_data()

    if not tokens_data:
        print("No tokens data found.")
        return

    # Save as JSON for reference
    with open('tokens_50m_output.json', 'w') as f:
        json.dump(tokens_data, f, indent=2)

    print(f"Found {len(tokens_data)} tokens with >50M market cap")
    print(json.dumps(tokens_data, indent=2))

    # Convert to CSV
    csv_data = convert_to_csv(tokens_data)

    if csv_data:
        # Save CSV locally for reference
        with open('tokens_50m_output.csv', 'w') as f:
            f.write(csv_data)
        print("\nCSV file created successfully")

        # Upload to Dune
        api_key = 'l2izTVbLIk5N5QRS4UQRNC0UdvmXDXTh'
        upload_to_dune(csv_data, api_key)

if __name__ == "__main__":
    main()
