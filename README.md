<<<<<<< HEAD
Netskope API Scripts
=======
Collection of scripts to quickly query the Netskope SCIM API and return information
about users and groups defined on the back end.

scimgroups - Lists or Deletes Groups
scimusers - Lists or Deletes Users

Note:  There is currently no checking for requrements when deleting.  Meaning it will not check if a user if there are
members in a group you are deleting and will error out.

Both take the following parameters

tenant = Netskope tenant ID (Without the .goskope.com)
function = LIST or DELETE - You can use this to delete users that are in a "Stuck" status for resync
ID = GUID of User or Group to search

Examples:

python ./scimgroups list all
python ./scimgroups list 948b4cc3-6368-4a3c-8669-e73c22c3c4c5
python ./scimusers list all
python ./scimusers list ef8fd947-32e7-474c-b502-02c012a63bff


apiquery.py

This one takes a few more parameters

1 = tenant name (Required - without .goskope.com)
2 = API Endpoint (Required without api/v2/ - will be prepended by default)
3 = What I call Options, so basically anything that needs to be sent with the api call EXCEPT for the actualy query if supported)
4 = --query (optional - Query that you want to use if supported)
5 = --view (Optional - View the json blob on the screen)
6 = --export (Optional - Will export the results to a file named "apiendpoint-epochtime.txt")

Example:

python ./apiquery.py tenantname events/data/application "starttime=1727803077&endtime=1727809677&limit=10000&skip=0" --query "activity eq 'Upload'" --view --export


The API Key needed for the calls is encoded in 2 files - not meant to be suer secure, but at least it's not in clear text.
Obviously it can be reverse engineered by reading the script - so modify accordingly for your environment.

Place your api key in a file called api.txt, then run the script encrypt_api in order to encrypt the api key in 2 files 
apikey.txt and apipass.txt.  Again, technically we should not have the key and pass in both places, but this is just for 
simplicity and obfuscation.  You are free to modify accordingly to meet your own securitDy requirements and make it better.

Running the scripts

requirements are in requirements.txt

1. Create a Virtual Environment
   - python3 -m venv netskopeapi

2. Install Requirements
   - pip install -r ./requirements.txt

3. Encode the API Key
   - Get your API Key from the Netskope admin portal
   - Create a file called ./api.txt and put your api key in it (Don't put any other text other than the api key)
   - Run python ./encrypt_api.py to encode the API Key - it will remove ./api.txt from the file system after complete

4. Run the scripts
