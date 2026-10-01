# Uses hasheous and IGDB to collect text-based metadata for local storage
import requests
#import os # for accessing .env if API key is needed

def hasheousSearch(sha1_hash: str) -> dict:

    # post SHA-1 hash to hasheous API for lookup
    payload = {
        "shA1": sha1_hash
    }

    response = requests.post(url="https://hasheous.org/api/v1/Lookup/ByHash", json=payload)

    # validate reponse
    if response.status_code != 200:
        print(f"WARNING: Failed to POST {sha1_hash} hash to Hasheous, possibly an unofficial ROM hack? STATUS CODE: {response.status_code}")
        #return control command that tells importer to skip this entry
        return None
    
        #TODO: more elegant handling, redirect to a function that checks if it is a ROM hack or a broken entry
        
    else:
        data = response.json()

        #prepare response data
        #TODO: handling for blank metadata. Dataclass defaults?
        game = data['signature']['game']
        metadata = {
            'name': game['name'],
            'publisher': game['publisher'],
            'release_year': game['year']
        }

    return metadata