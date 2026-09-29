# Uses hasheous and IGDB to collect text-based metadata for local storage
import requests
import os # for accessing .env if API is needed

def hasheousSearch(sha1_hash: str) -> dict:

    # post SHA-1 hash to hasheous API for lookup
    payload = {
        "shA1": sha1_hash
    }

    response = requests.post(url="https://hasheous.org/api/v1/Lookup/ByHash", json=payload)

    # validate reponse
    if response.status_code != 200:
        print(f"ERROR: Failed to post SHA-1 hash to Hasheous, possibly an unofficial ROM hack? STATUS CODE: {response.status_code}")
        #return metadata object populated with defaults
        #TODO: more elegant handling, redirect to a function that checks if it is a ROM hack or a broken entry
        metadata = {
            'name': 'Failed to retrieve metadata, posibly an unofficial ROM hack? STATUS_CODE_400',
            'publisher': 'Failed to retrieve metadata, possibly an unofficial ROM hack? STATUS_CODE_400',
            'regions': {'Failed to retrieve metadata, possibly an unofficial ROM hack? STATUS_CODE_400': 'N/A'},
            'AIdescription': 'Failed to retrieve metadata, possibly an unofficial ROM hack? STATUS_CODE_400',
            "release_year": 'Failed to retrieve metadata, possibly an unofficial ROM hack? STATUS_CODE_400'
        }
    else:
        data = response.json()

        #package response data
        #TODO: handling for blank metadata. Dataclass defaults?
        game = data['signature']['game']
        metadata = {
            'name': game['name'],
            'publisher': game['publisher'],
            'regions': game['countries'],
            'AIdescription': 'temp', #TODO: figure out proper index
            'release_year': game['year']
        }

    return metadata