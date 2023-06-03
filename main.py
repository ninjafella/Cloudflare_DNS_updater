import requests
import os
import json
import sys
import logging
from typing import Union

# Log config

LOGS : bool = True # Where to log to file or print out to the console
LOGS_FILE : str = 'CloudflareDNS.log' # Where to save the log file
LOGGING_LEVEL : int = logging.DEBUG # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Main config
IP_FILE : str = 'ipaddr.txt' # File to save the current IP address to
DOMAIN : str = '<example.com>' # Domain to update
PROXIED : bool = True # Whether the DNS record is proxied through Cloudflare or not
CF_EMAIL : str = 'john@<example>.com' # Email address used to login to Cloudflare
CF_API_KEY : str = '<API key>' # Global API key from Cloudflare
ZONE_ID : str = '<Zone ID>' # Zone ID from Cloudflare
RECORD_ID : Union[str, list] = '<record ID>' # or ['<record ID 1>', '<record ID 2>', ...]   # DNS record ID from Cloudflare.
# Either a string to just update the root domain record or a list of two strings to update both the root domain and subdomains,
# or a list of three strings to update the root domain, subdomains and www subdomain


if LOGS:
    logging.basicConfig(filename=LOGS_FILE, level=LOGGING_LEVEL, format='%(asctime)s %(message)s')
    print = logging.info
    print_debug = logging.debug
else:
    print = print
    print_debug = print


def getIP() -> str:
    return requests.get('https://api.ipify.org/').text


def updateCloudflareDNS(ip: str) -> None:
    if type(RECORD_ID) == list:
        try:
            cloudFlareDNSAPI(f'{DOMAIN}', ip, RECORD_ID[0])
            cloudFlareDNSAPI(f'*.{DOMAIN}', ip, RECORD_ID[1])
            cloudFlareDNSAPI(f'www.{DOMAIN}', ip, RECORD_ID[2])
        except Exception:
            pass
    else:
        cloudFlareDNSAPI(f'{DOMAIN}', ip, RECORD_ID)


def cloudFlareDNSAPI(domain: str, ip: str, record_id: str) -> None:
    resp = requests.put(
        f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}',
        json={
            'type': 'A',
            'name': f'{domain}',
            'content': ip,
            'proxied': PROXIED
        },
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL,
            'Content-Type': 'application/json'
        })
    print_debug(resp.json())



if not RECORD_ID:
    print_debug("RECORD_ID is blank loading DNS records")
    resp = requests.get(
        f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records',
        headers={
            'X-Auth-Email': CF_EMAIL,
            'X-Auth-Key': CF_API_KEY,
            'Content-Type': 'application/json'
        })
    print(json.dumps(resp.json()["result"], indent=4, sort_keys=True))
    print('Please find the DNS record ID you would like to update and entry the value into the script')
    sys.exit(0)


if os.path.isfile(IP_FILE):
    print_debug('IP file exists')
    with open(IP_FILE, 'r') as ip_file:
        ip = ip_file.read()

    if ip != getIP():
        ip = getIP()
        with open(IP_FILE, 'w') as ip_file:
            ip_file.write(ip)
        updateCloudflareDNS(ip)
        print('IP address changed to: ' + ip)
    else:
        print('IP address has not changed')
else:
    ip = getIP()
    with open(IP_FILE, 'w') as ip_file:
        ip_file.write(ip)