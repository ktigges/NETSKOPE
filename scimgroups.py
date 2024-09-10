

# Author.....: Kevin Tigges
# Script Name: scimgroups.py
# Desc.......: Script to query Netskope groups
# 
#
# Last Updates: 9/9/2024
# v001
#

import requests
import xml.etree.ElementTree as ET
import json
import argparse
import pdb
import urllib3
from common import *


urllib3.disable_warnings()


def main(tenant, function, groupID):

   apitoken = get_api()
   nstenant = tenant.strip() 

   # Pull in Netskope Group Data
   
   if function.lower() == 'list' and  groupID.lower() == "all":
      apiurl = f'https://{nstenant}.goskope.com/api/v2/scim/Groups'
      header = { 'Netskope-Api-Token' : f'{apitoken}'}
      response = requests.get(apiurl, headers=header, verify=False)
      if response.status_code != 200 :
         print("Error Listing Groups all")
         exit()

      jsondata = json.loads(response.content)
      # Loop through Netskope Data
      for group in jsondata["Resources"]:
         n_group = group['displayName']
         n_gid = group['id']
         print(f'{n_gid} - {n_group}')
      
   
   if function.lower() == 'list' and groupID.lower() != "all":
      apiurl = f'https://{nstenant}.goskope.com/api/v2/scim/Groups/{groupID}'
      apitoken = '53afe0836ddef854b09edbf1325dc619'
      header = { 'Netskope-Api-Token' : f'{apitoken}'}
      response = requests.get(apiurl, headers=header, verify=False)
      if response.status_code != 200 :
         print("error listing groups")
         exit()
      jsondata = json.loads(response.content)
      print(json.dumps(jsondata, indent=2))
     
   
   if function.lower() == 'delete' and groupID.lower != "all":
      apiurl = f'https://{nstenant}.goskope.com/api/v2/scim/Groups/{groupID}'
      header = { 'Netskope-Api-Token' : f'{apitoken}'}
      response = requests.delete(apiurl, headers=header, verify=False)
      if response.status_code != 204 :
         print(response.status_code)
         print("error deleting group")
         exit()
      else:
         print(f'{response.status_code} Group Deleted')
      
       
if __name__ == "__main__":
#    # Create the Parser for the command line arguments
#    # Panorama IP, Number of Minuites, IP1, Port
    p = argparse.ArgumentParser(description = 'Script to query SCIM groups on tenant')
    p.add_argument('tenant', type=str, default="", help="Enter your netskope tenant id WITHOUT .goskope.com)")
    p.add_argument('function', type=str, default="LIST", help="Enter Function: LIST / DELETE or Blank to List all")
    p.add_argument('groupID', type=str, default = "all", help="Enter group guid to search - ALL for all groups")
    args = p.parse_args()
    main(args.tenant, args.function, args.groupID)   