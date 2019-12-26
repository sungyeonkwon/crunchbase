# Crunchbase API:
# https://data.crunchbase.com/docs/using-the-api
# https://data.crunchbase.com/reference

import csv
import itertools
import json
import requests
import sys

base = 'https://api.crunchbase.com/v3.1'
user_key = '7c49ff3ff79a2be9685cb2ecbfb65764'

def get_collection(endpoint):
    """
    Function to get collection from endpoints available.

    Parameter: 'organizations' || 'people' || 'categories' || 'locations'
    Returns: collection (JSON) || None
    """

    res = requests.get(f'{base}/{endpoint}?user_key={user_key}')
    if res:
        json_data = res.json()
        return json_data['data']['items']
    else:
        print('Response Failed in get_collection: ', res)
        return None

def get_detail_collection(id_collection, endpoint, properties):
    """
    Function to get detail collection from endpoints available.

    Parameters:
        id_collection (list of strings): list of ids
        endpoint (string) : 'organizations' || 'people' || 'funding-rounds'
            || 'acquisitions' || 'ipos' || 'funds'
        properties (list of strings): list of properties
    Returns: collection (JSON) || None
    """

    custom_collection = {}
    for id in id_collection:
        custom_collection[id] = {}
        res = requests.get(f'{base}/{endpoint}/{id}?user_key={user_key}')
        if res:
            json_data = res.json()
            for prop in properties:
                custom_collection[id][prop] = json_data['data']['properties'][prop]
        else:
            print('Response Failed in get_detail_collection: ', res)
    return custom_collection

# Currently all uuids don't have funding-rounds detail data.
# Insert dropbox's uuid as an example that has funding-rounds detail data.
dropbox_uuid = 'b2294fd993614bf489f29d0d5bb98269'
organizations = get_collection('organizations')
uuids = [dropbox_uuid] + [organization['uuid'] for organization in organizations]

# This is for 'funding-rounds' detail endpoint.
# Edit the list of properties according to the available properties.
properties = [
    'closed_on',
    'money_raised_usd'
]
custom_collection = get_detail_collection(uuids, 'funding-rounds', properties)

# Optional: Save data as csv file.
with open('crunchbase.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, ['id'] + properties)
    writer.writeheader()
    for key, val in sorted(custom_collection.items()):
        row = {'id': key}
        row.update(val)
        writer.writerow(row)

# Optional: Save data as json file.
# with open('crunchbase.json', 'w') as json_file:
#     json.dump(custom_collection, json_file)
