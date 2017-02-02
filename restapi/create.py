import requests
from requests.auth import HTTPBasicAuth 
import json

# Replace with the correct URL
url = "http://localhost:7001/management/weblogic/latest/domainConfig/JMSServers/JMSServer1?fields=messagesThresholdHigh,deploymentOrder"
user = "system"
pwd = "gumby1234"
# It is a good practice not to hardcode the credentials. So ask the user to enter credentials at runtime
myResponse = requests.get(url,auth=HTTPBasicAuth(user, pwd), verify=True)
print (myResponse.status_code)
print (myResponse.content)

# For successful API call, response code will be 200 (OK)
if(myResponse.ok):

    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jData = json.loads(myResponse.content)
    print(jData.get("messagesThresholdHigh"))
    print(jData.get("deploymentOrder"))
else:
  # If response code is not ok (200), print the resulting http error code with description
    myResponse.raise_for_status()
