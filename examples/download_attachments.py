#!/usr/bin/env python3

from __future__ import print_function
import argparse
import rspace_client
import sys

# Parse command line parameters
parser = argparse.ArgumentParser()
parser.add_argument("server", help="RSpace server URL (for example, https://community.researchspace.com)", type=str)
parser.add_argument("apiKey", help="RSpace API key can be found on 'My Profile'", type=str)
args = parser.parse_args()

client = rspace_client.Client(args.server, args.apiKey)

print('Document ID to search for (for example, numeric id 123 or global ID SD123)?')
document_id = sys.stdin.readline().strip()

try:
    response = client.get_document(doc_id=document_id)

    file_found = False
    for field in response['fields']:
        for file in field['files']:
            download_metadata_link = client.get_link_contents(file, 'self')
            filename = '/tmp/' + download_metadata_link['name']
            print('Downloading to file', filename)
            client.download_link_to_file(client.get_link(download_metadata_link, 'enclosure'), filename)
            file_found = True

    if not file_found:
        print('There are no attached files.')
except ValueError as e:
    print(e)
except rspace_client.Client.ApiError as e:
    print(e)
