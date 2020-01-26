#!/usr/bin/env python

'''
print(IPv4Address('192.0.3.6') in IPv4Network('192.0.2.0/28'))
True/False
ipaddress.AddressValueError:
'''

import ipaddress
import json
import requests
from ipaddress import IPv4Address, IPv4Network

def get_json(cloud, prefix_list):
    try:
        print(json.dumps({cloud: prefix_list}, indent=4))
    except ValueError as e:
        print(e)


def aws(ip):
    # [] if no match
    try:
        cloud = 'AWS'
        ip_ranges = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json').json()['prefixes'] # type list
        #all_prefixes_json = json.dumps(ip_ranges, indent=4) # type string
        filtered_list = [i for i in ip_ranges if IPv4Address(ip) in IPv4Network(i['ip_prefix'])]
        get_json(cloud, filtered_list)
    except ipaddress.AddressValueError as e:
        print(e)


def azure_public(ip):
    # [] if no match
    try:
        az_public = requests.get('https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20200121.json').json()
        cloud = 'AzurePublic'
        properties_list = [i['properties'] for i in az_public['values']]
        filtered_list = [{'addressPrefixes': j, 'systemService': i['systemService'], 'region': i['region']} for i in properties_list for j in i['addressPrefixes'] if IPv4Address(ip) in IPv4Network(j)]
        get_json(cloud, filtered_list)
    except ipaddress.AddressValueError as e:
        print(e)


def azure_gov(ip):
    # [] if no match
    try:
        #az_public = requests.get('https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20200121.json').json()
        az_gov = requests.get('https://download.microsoft.com/download/6/4/D/64DB03BF-895B-4173-A8B1-BA4AD5D4DF22/ServiceTags_AzureGovernment_20200121.json').json()
        cloud = 'AzureGov'
        properties_list = [i['properties'] for i in az_gov['values']]
        filtered_list = [{'addressPrefixes': j, 'systemService': i['systemService'], 'region': i['region']} for i in properties_list for j in i['addressPrefixes'] if IPv4Address(ip) in IPv4Network(j)]
        get_json(cloud, filtered_list)
    except ipaddress.AddressValueError as e:
        print(e)


def main():
    ip = '54.250.251.1'
    #aws_ip = '54.250.251.1'
    #azure_gov_ip = '52.127.26.97'
    #azure_public_ip = '40.79.178.97'
    aws(ip)
    azure_gov(ip)
    azure_public(ip)

if __name__ == "__main__":
    main()
