#!/usr/bin/env python

import ipaddress
import json
import requests
from ipaddress import IPv4Address, IPv4Network

#print(IPv4Address('192.0.3.6') in IPv4Network('192.0.2.0/28'))
# True/False
# ipaddress.AddressValueError:

def aws():
    ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes'] # type list
    #all_prefixes_json = json.dumps(ip_ranges, indent=4) # type string
    ip = '54.250.251.1'
    filtered_list = [i for i in ip_ranges if IPv4Address(ip) in IPv4Network(i['ip_prefix'])]
    filtered_json = json.dumps(filtered_list, indent=4)
    print(filtered_json)


def azure():
    az_public = requests.get('https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20200121.json').json()
    #az_cloud = az_public['cloud']
    #values = az_public['values']
    #properties_list = [i['properties'] for i in values]
    #print(az_cloud)
    properties_list = [i['properties'] for i in az_public['values']]
    ip = '40.79.178.97'
    filtered_list = [{'addressPrefixes': j, 'systemService': i['systemService'], 'region': i['region']} for i in properties_list for j in i['addressPrefixes'] if IPv4Address(ip) in IPv4Network(j)]
    filtered_json = json.dumps(filtered_list, indent=4)
    print(filtered_json)

def main():
    aws()
    azure()

if __name__ == "__main__":
    main()
