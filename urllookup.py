

# Author.....: Kevin Tigges
# Script Name: scimgroups.py
# Desc.......: Script to query URL's and provide category and other information via Netskope API
# 
#
# Last Updates: 9/9/2024
# v001
#

import requests
import json
import argparse
import urllib3
from common import *

urllib3.disable_warnings()



def main(tenant, url_list):

   apitoken = get_api()
   nstenant = tenant.strip()

   # Pull in Netskope User Data
   
   apiurl = f'https://{nstenant}.goskope.com/api/v2/nsiq/urllookup'
   header = { 'Netskope-Api-Token' : f'{apitoken}'}
   payload = {
      "query": {
        "disable_dns_lookup": True,
        "urls": url_list 
      }

   }
  
   response = requests.post(apiurl, headers=header, json=payload, verify=False)

   if response.status_code != 200 :
      print("Error getting URLs - Status Code "+str(response.status_code))
      exit()
   jsondata = json.loads(response.content)
   print(json.dumps(jsondata, indent=4))
       
if __name__ == "__main__":
#    # Create the Parser for the command line arguments
#    # Panorama IP, Number of Minuites, IP1, Port
    p = argparse.ArgumentParser(description = 'Script to query URL Categories from Netskope')
    p.add_argument('tenant', type=str, default="", help="Enter your netskope tenant id WITHOUT .goskope.com)")
    p.add_argument('url_list', type=str, nargs='+', help="Enter URL List to query")
    args = p.parse_args()
    main(args.tenant, args.url_list)   