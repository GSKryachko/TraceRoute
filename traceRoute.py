import json
import re
import subprocess
import sys

import requests

extractor = re.compile(
    '\s*(\d+).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|Request timed out.)\]?')
ip_pattern = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def get_tracert_table(address):
    try:
        output = subprocess.check_output(["tracert", address]).decode()
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        exit()
    if 'Trace complete.' not in output:
        print("Something gone wrong", file=sys.stderr)
    return output


def complete_tracert_table(table):
    for line in table.split('\n'):
        match_obj = extractor.match(line)
        if match_obj:
            ip = match_obj.group(2)
            if ip_pattern.match(ip):
                yield (match_obj.group(1), ip) + get_AS_info(ip)
            else:
                yield (match_obj.group(1), ip, 'N/A', 'N/A', 'N/A')


def print_tracert_table(table):
    row_format = '{:10} {:20} {:50} {:20} {:20}'
    print(row_format.format('Position', 'IP', 'AS', 'Country', 'ISP'))
    for entry in table:
        print(row_format.format(*entry))


def get_AS_info(ip):
    try:
        response = requests.get('http://ip-api.com/json/{}'.format(ip)).text
        data = json.loads(response)
    
    except (
            json.JSONDecodeError, requests.exceptions.ConnectionError,
            KeyError):
        print('Something went wrong with ip-api.com', file=sys.stderr)
        return 'N/A', 'N/A', 'N/A'
    if data['status'] == 'success':
        return data['as'], data['country'], data['isp']
    else:
        print(data['message'])
        return 'N/A', 'N/A', 'N/A'

#To read about RIPE and ARIN