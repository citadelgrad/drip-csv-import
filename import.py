import csv
import json
from itertools import izip_longest

import requests

'''
Imports customer first_name, last_name, and email into getDrip.com. 
The csv must be formatted in that order.

Required configuration:
'''
# Set these three values
drip_site_id = ''
drip_api_access_token = ''
csv_filename = "sample.csv"
''' Optional configuration '''
drip_import_tags = ["your-tag",]

reader = csv.reader(open(csv_filename))

def batch_subscribers(csv_data, tags=[]):
    subscribers = {"subscribers": []}
    for cust in csv_data:
        ''' We must check that a list exists since the grouper 
        will add `None` values when creating the last group.
        '''
        if cust:
            subscribers['subscribers'].append(dict(email=cust[2], 
                custom_fields=dict(first_name=cust[0], last_name=cust[1]),
                tags=tags)
                )
    return subscribers

def send_batch_to_drip(subscribers):
    '''
    Batches API: https://www.getdrip.com/docs/rest-api#subscriber_batches
    '''
    subscribers_batch_uri = "https://api.getdrip.com/v2/{}/subscribers/batches".format(drip_site_id)

    headers = {'content-type': 'application/vnd.api+json', 'Authorization': 'Bearer {}'.format(drip_api_access_token)}
    batches = dict(batches=[subscribers])
    result = requests.post(subscribers_batch_uri, data=json.dumps(batches), headers=headers)
    return result

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

# Groups csv data into 1000 record chunks.
groups = grouper(reader, 1000)

# Iterate over each group.
for group in groups:
    subscribers = batch_subscribers(group, tags=drip_import_tags)	
    response = send_batch_to_drip(subscribers)