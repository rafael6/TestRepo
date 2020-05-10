#!/usr/bin/env python

# TODO: chmod +x test.py
# TODO: remove get_o365_change_history() fuction

'''
print(IPv4Address('192.0.3.6') in IPv4Network('192.0.2.0/28'))
True/False
ipaddress.AddressValueError:

        aws_ip = '54.250.251.1'
        azure_gov_ip = '52.127.26.97'
        azure_public_ip = '40.79.178.97'
'''

import argparse
import ipaddress
import json
import requests
import uuid
from ipaddress import IPv4Address, IPv4Network

# Get client UUID
client_request_id = str(uuid.uuid4())

# Get publication date for URIs in functions
uri = 'https://www.microsoft.com/en-us/download/details.aspx?id=57063'
resp = requests.get(uri)
substring_begining = resp.text.find('ServiceTags_AzureGovernment_2')
substring_end = substring_begining + 28
publication_date = resp.text[substring_end: substring_end + 8]

def get_json(cloud, prefix_list):
    assert (type(prefix_list is list)), 'prefix_list must be a list object'
    try:
        print(json.dumps({cloud: prefix_list}, indent=4))
    except ValueError as e:
        print(e)
    except AssertionError as e:
        print(e)

def aws(ip):
    assert (type(ip) is str), 'IP must be an str object.'
    try:
        cloud = 'AWS'
        ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes'] # type list
        #all_prefixes_json = json.dumps(ip_ranges, indent=4) # type string
        filtered_list = [i for i in ip_ranges if IPv4Address(ip) in IPv4Network(i['ip_prefix'])]
        get_json(cloud, filtered_list)
    except ValueError as e:
        print(e)
    except AssertionError as e:
        print(e)

def azure_public(ip):
    assert (type(ip) is str), 'IP must be an str object.'
    try:
        az_public = requests.get(f'https://download.microsoft.com/download' \
        f'/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_' \
            f'{publication_date}.json').json()
        cloud = 'AzurePublic'
        properties_list = [i['properties'] for i in az_public['values']]
        filtered_list = [
            {
                'addressPrefixes': j,
                'systemService': i['systemService'],
                'region': i['region']
                } 
                for i in properties_list
                for j in i['addressPrefixes']
                if IPv4Address(ip) in IPv4Network(j)
                ]
        get_json(cloud, filtered_list)
    except ValueError as e:
        print(e)
    except AssertionError as e:
        print(e)

def azure_gov(ip):
    assert (type(ip) is str), 'IP must be an str object.'
    try:
        az_gov = requests.get('https://download.microsoft.com/download/6/4/D/' \
            f'64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_' \
            f'{publication_date}.json').json()
        cloud = 'AzureGov'
        properties_list = [i['properties'] for i in az_gov['values']]
        filtered_list = [
            {
                'addressPrefixes': j,
                'systemService': i['systemService'],
                'region': i['region']
                }
                for i in properties_list
                for j in i['addressPrefixes']
                if IPv4Address(ip) in IPv4Network(j)
                ]
        get_json(cloud, filtered_list)
    except ValueError as e:
        print(e)
    except AssertionError as e:
        print(e)

def get_o365_change_history():
    try:
        instance = 'USGOVGCCHigh' # Worldwide|China|Germany|USGovDoD|USGovGCCHigh
        uri = f'https://endpoints.office.com/changes/{instance}/0000000000?' \
            f'ClientRequestId={client_request_id}'
        responce = requests.get(uri).text # for type dict use .json()
        print(responce)
    except ValueError as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description='Find cloud provider for IP.')
    parser.add_argument('ip',
                        type=str,
                        help='IPv4 address in question')
    args = parser.parse_args()
    ip = args.ip
    aws(ip)
    azure_gov(ip)
    azure_public(ip )



if __name__ == "__main__":
    main()
