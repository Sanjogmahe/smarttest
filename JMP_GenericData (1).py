import json
from collections import defaultdict

from jira import JIRA
import pandas as pd
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import multiprocessing as mp
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

authDetails=("lakshmypriya-kuttappan.chettiar-ananda-lekshmy@allianz.com", "Kripakalk4#")
header = {'Content-Type': 'application/json'}
## Extract Project Lists to be displayed in UI and to be selected

url="https://jmp.allianz.net/rest/api/2/project"
html = requests.get(url, verify=False, headers=header, auth=authDetails)
data = html.text
jsonLink = json.loads(data)
#print(jsonLink)
ProjectData = pd.DataFrame()
for record in jsonLink:

 d={
  'projectName': record['name'],
  'projectID':record['id'],
  'projectKey':record['key']
 }
 #dataset = pd.DataFrame(d, index=[0])
 ProjectData = ProjectData.append(d, ignore_index=True)
print(ProjectData)

#Extracting Release List

selectedProjectKey="19120"

url="https://jmp.allianz.net/rest/api/2/project/"+selectedProjectKey+"/versions"
html = requests.get(url, verify=False, headers=header, auth=authDetails)
data = html.text
jsonLink = json.loads(data)
releaseList=pd.DataFrame()

for record in jsonLink:
 d = {
  'releaseName': record['name']
 }
 releaseList = releaseList.append(d, ignore_index=True)

print(releaseList)