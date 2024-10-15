

# Author.....: Kevin Tigges
# Script Name: apiquery.py
# Desc.......: Script to query any API endpoint (Caveat - you need to have the query and options ready)
#              
# Options could contain anything really that is required to 
# Example Call would be:
#              
# python ./apiquery-export.py ktigges-lab1 services/cci/app 'category=Social&offset=0&limit=1000' --view --export
# - See how the options parameter contains 'category=Social&offset=0&limit=1000' for this specific query
# - Another example with an actual "Query" of data would be
#
# python ./apiquery-export.py ktigges-lab1 events/data/application "starttime=1727803077&endtime=1727809677&limit=10000&skip=0" 
#        --query "activity eq 'Upload'"

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
import urllib.parse
from common import *
import csv
import time


urllib3.disable_warnings()


def main(tenant, endpoint, options, query, view, export):

   apitoken = get_api()
   nstenant = tenant.strip() 
   if len(query) > 0:
      enc_query = urllib.parse.quote(query)
      apiurl = f"https://{nstenant}.goskope.com/api/v2/{endpoint}?{options}&query={enc_query}"
   else:
      apiurl = f"https://{nstenant}.goskope.com/api/v2/{endpoint}?{options}"
   print(f'\n\nAPI URL Call is: {apiurl}')
   
  
   header = { 'Netskope-Api-Token' : f'{apitoken}'}
   #pdb.set_trace()
   response = requests.get(apiurl, headers=header, verify=False)
   if response.status_code != 200 :
      print(f"Error running API Call - {response.status_code}")
      exit()

   jsondata = json.loads(response.content)
   #pdb.set_trace()
   # We need to pick out the "result" key, could be 'result', could be 'data', may be something else we need to account for
   keys = jsondata.keys()
   # Convert to list and get the actualy result key
   keys = list(keys)
   if ('data' in keys):
      resultkey = 'data'
   else: 
     if ('result' in keys):
        resultkey = 'result'
     else:
        print('This json result uses a result key that you have not accounted for, please modify accordingly', keys)
        exit()
          
   result_data = jsondata[resultkey]
   if view :
     print(json.dumps(result_data, indent=4))
   # Loop through Results and Count
   count = len(jsondata[resultkey])
   # waittime = jsondata['wait_time']
   print(f'\nNumber of Results: {count}')
   # print(f'\nWait time until next query: {waittime}')
   if export:
      #Loop through and print to export.csv
      epoch_time = int(time.time())
      file_prefix = endpoint.replace('/','-')
      outputfile = f"{file_prefix}-{epoch_time}.csv"
      # Take Results Only
      #Update all fields in json data, some records may have more fields than others for the first record isn't always accurate
      print("\nDetermining Fields in all records...")
      fields = set()
      for record in result_data:
         fields.update(record.keys())
     
      print("\nWriting Output....")
      with open(outputfile, mode='w', newline='') as exporter:
         writer = csv.DictWriter(exporter, fieldnames=fields)
         writer.writeheader()
         for row in result_data:
            
            writer.writerow(row)
      print(f"\nResults have been written to {outputfile}")

   
   
   
      
       
if __name__ == "__main__":
#    # Create the Parser for the command line arguments
   p = argparse.ArgumentParser(description = 'Script to query SCIM groups on tenant')
   p.add_argument('tenant', type=str, default="", help="Enter your netskope tenant id WITHOUT .goskope.com)")
   p.add_argument('endpoint', type=str, default="", help="Enter the API Endpoint i.e. events/data/application")
   p.add_argument('options', type=str, default = "", help="Enter the options, i.e. limit=5000&offset=0&starttime=xxx&endtime=yyyyy")
   p.add_argument('--query', type=str, default="", required=False, help="Entery query, i.e. activity eq 'Upload' and access_method eq 'Client' etc..")
   p.add_argument('--view',action='store_true',help='View the Results')
   p.add_argument('--export',action='store_true',help='Export to CSV')
   args = p.parse_args()
   main(args.tenant, args.endpoint, args.options, args.query, args.view, args.export)   
 