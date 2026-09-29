# Uses hasheous and IGDB to collect text-based metadata for local storage
import requests
import os # for accessing .env
import rom_dataclasses as rdc

def hasheousSearch(Rom: rdc.Rom):

    # post SHA-1 hash to hasheous API for lookup
    payload = {
        "shA1": Rom.game.sha1
    }

    response = requests.post(url="https://hasheous.org/api/v1/Lookup/ByHash", json=payload)

    # validate reponse
    if response.status_code != 200:
        print(f"ERROR: Failed to post SHA-1 hash to Hasheous. STATUS CODE: {response.status_code}")
        return -1 # TODO: Proper failure handling

    data = response.json()

    for entry in data:
        print(entry)

    #print(f"ID: {data['id']}") #don't need
    #print("-------------------------------------------")
    #print(f"name: {data['name']}") # available in signature
    #print("-------------------------------------------")
    #print(f"PLATFORM: {data['platform']}") # available in signature
    #print("-------------------------------------------")
    #print(f"PUBLISHER: {data['publisher']}") # available in signature
    #print("-------------------------------------------")
    print(f"SIGNATURE: {data['signature']}")
    #print("-------------------------------------------")
    #print(f"METADATA: {data['metadata']}") #dont need
    #print("-------------------------------------------")
    print(f"ATTRIBUTES: {data['attributes']}") # Contains Game Descriptions

    # all the desired data can be extracted from Signature and Attributes