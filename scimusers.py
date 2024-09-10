
import requests
import xml.etree.ElementTree as ET
import json
import argparse
import pdb
import urllib3
from common import *

urllib3.disable_warnings()

def main(tenant, function, userID):

   apitoken = get_api()
   nstenant = tenant.strip()

   # Pull in Netskope User Data
   
   if function.lower() == 'list' and  userID.lower() == "all":
      apiurl = f'https://{nstenant}.goskope.com/api/v2/scim/Users'
      header = { 'Netskope-Api-Token' : f'{apitoken}'}
      response = requests.get(apiurl, headers=header, verify=False)
      if response.status_code != 200 :
         print("Error Listing Groups all")
         exit()

      jsondata = json.loads(response.content)
      # Loop through Netskope Data, Resource section and print user name and GUID
      for user in jsondata["Resources"]:
         n_user = user['userName']
         n_uid = user['id']
         print(f'{n_user} - {n_uid}')
      
   
   if function.lower() == 'list' and userID.lower() != "all":
      apiurl = f'https://{nstenant}.goskope.com/api/v2/scim/Users/{userID}'
      header = { 'Netskope-Api-Token' : f'{apitoken}'}
      response = requests.get(apiurl, headers=header, verify=False)
      if response.status_code != 200 :
         print("error listing user")
         exit()
      jsondata = json.loads(response.content)
      print(json.dumps(jsondata, indent=2))
     
   
   if function.lower() == 'delete' and userID.lower != "all":
      apiurl = f'https://{nstenant}.goskope.com/api/v2/scim/Users/{userID}'
      header = { 'Netskope-Api-Token' : f'{apitoken}'}
      response = requests.delete(apiurl, headers=header, verify=False)
      if response.status_code != 204 :
         print(response.status_code)
         print("error deleting user")
         exit()
      else:
         print(f'{response.status_code} User Deleted')
      
       
if __name__ == "__main__":
#    # Create the Parser for the command line arguments
#    # Panorama IP, Number of Minuites, IP1, Port
    p = argparse.ArgumentParser(description = 'Script to query SCIM groups on tenant')
    p.add_argument('tenant', type=str, default="", help="Enter your netskope tenant id WITHOUT .goskope.com)")
    p.add_argument('function', type=str, default="LIST", help="Enter Function: LIST / DELETE or Blank to List all")
    p.add_argument('userID', type=str, default = "all", help="Enter user guid to search - ALL for all users")
    args = p.parse_args()
    main(args.tenant, args.function, args.userID)   