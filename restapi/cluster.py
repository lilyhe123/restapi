import requests
from requests.auth import HTTPBasicAuth 
import json
import shutil
import sys
import os
from time import time
from collections import OrderedDict

#prefix='http://10.182.55.63:7001/management/weblogic/latest/'
prefix='http://localhost:7001/management/weblogic/latest/'
jmsdir='/Users/lilyhe/depot/src122130_build/Oracle_Home/results/wls/unit/jms/domains/TestDomain/config/jms'
modulefile='clusterData/mymodule-jms.xml'
inputfile='cluster.input'
user = 'system'
pwd = 'gumby1234'
auth = HTTPBasicAuth(user, pwd)
header1 = {'X-Requested-By': 'pythonclient','Accept':'application/json','Content-Type':'application/json'}
header2 = {'X-Requested-By': 'pythonclient','Accept':'application/json'}


def create(name, tail, filename):
    data =  open(filename, 'rb').read()
    print(data)
    myResponse = requests.post(prefix+tail, auth=auth, headers=header1, data=data, verify=True)
    result(myResponse, 'create ' + name, 'true')

def delete(tail):
    myResponse = requests.delete(prefix+tail, auth=auth, headers=header2, verify=True)
    result(myResponse, 'delete', 'false')

def get(tail):
    myResponse = requests.get(prefix+tail, auth=auth, headers=header2, verify=True)
    result(myResponse, 'get', 'false')

def result(res, opt, fail):
    print (res.status_code)
    if(not res.content.isspace()):
        print (res.content)
    if(res.ok):
        print opt, 'succeed.'
    else:
        print opt, 'failed.'
        if(fail == 'true'):
            res.raise_for_status()


def deleteAll():
    delete('edit/JMSSystemResources/mymodule/subDeployments/subsaf1')
    delete('edit/JMSSystemResources/mymodule/subDeployments/subsaf2')
    delete('edit/JMSSystemResources/mymodule/subDeployments/sub1')
    delete('edit/JMSSystemResources/mymodule/subDeployments/sub2')
    delete('edit/JMSSystemResources/mymodule')
    delete('edit/SAFAgents/safagent1')
    delete('edit/SAFAgents/safagent2')
    delete('edit/JMSServers/jmsserver1')
    delete('edit/JMSServers/jmsserver2')
    delete('edit/fileStores/filestore1')
    delete('edit/fileStores/filestore2')

def createAll():
    print('create all resources')
    try:
        os.makedirs(jmsdir)
    except OSError:
        if not os.path.isdir(jmsdir):
            raise
    shutil.copy2(modulefile, jmsdir)
    print('copy module file finished.')
    jdata = json.loads(open(inputfile, 'r').read(), object_pairs_hook=OrderedDict)
    for key in jdata.keys():
        value=jdata.get(key)
        create(key, value['url'], value['data'])

def getAll():
    get('domainConfig/fileStores/filestore1')
    get('domainConfig/fileStores/filestore2')
    get('domainConfig/JMSServers/jmsserver1')
    get('domainConfig/JMSServers/jmsserver2')
    get('domainConfig/SAFAgents/safagent1')
    get('domainConfig/SAFAgents/safagent2')
    get('domainConfig/JMSSystemResources/mymodule')
    get('domainConfig/JMSSystemResources/mymodule/subDeployments')

def monitor():
    get('domainRuntime/serverRuntimes/ms1/JMSRuntime/JMSServers/jmsserver1@ms1?links=none&fields=name,healthState')
    get('domainRuntime/serverRuntimes/ms1/JMSRuntime/JMSServers/jmsserver2@ms1?links=none&fields=name,healthState')
    get('domainRuntime/serverRuntimes/ms1/JMSRuntime/JMSServers/jmsserver1@ms1/destinations?links=none&fields=name,destinationType,messagesCurrentCount,messagesPendingCount')
    get('domainRuntime/serverRuntimes/ms1/JMSRuntime/JMSServers/jmsserver2@ms1/destinations?links=none&fields=name,destinationType,messagesCurrentCount,messagesPendingCount')

    get('domainRuntime/serverRuntimes/ms1/SAFRuntime/agents/safagent1@ms1?links=none&fields=name,healthState,messagesCurrentCount,messagesPendingCount,remoteEndpointsCurrentCount')
    get('domainRuntime/serverRuntimes/ms1/SAFRuntime/agents/safagent2@ms1?links=none&fields=name,healthState,messagesCurrentCount,messagesPendingCount,remoteEndpointsCurrentCount')
 
def test():
    get('domainConfig/JMSServers/jmsserver1')
    get('domainConfig/SAFAgents/safagent1')

print 'url:', prefix 
start=time()
option=sys.argv[1]
if(option == 'create'):
    createAll()
elif(option == 'delete'):
    deleteAll()
elif(option == 'get'):
    getAll()
elif(option == 'monitor'):
    monitor()
else:
    test()

end=time()
print option, "spent", (end-start), "seconds"
