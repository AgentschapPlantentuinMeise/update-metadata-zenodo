#to run: python3 update_community.py filename
#where filename is the file with the record ids
#which needs 'id' as header (see example camtrapids.txt file)

import requests
import json
import sys
import datetime
import pandas as pd

#read list of ids
updids = pd.read_csv(sys.argv[1],sep=';')

#open log of json responses of requests
#this can grow quite big
logfilepub=open('updlog.txt','a+')
logfilepub.write('[')

#open overview status log of requests success
quicklog=open('quicklog upd.txt','a+')
quicklog.write('Depo ID\tGet\tEdit\tUpdate\tPublish\n')

#set your zenodo api access token here
#do not share with others
access_token = 'your token'

#modify the base url to use the sandbox
headers = {'Accept': 'application/json',}
headers2 = {'Content-Type': 'application/json'}
base_url = 'https://zenodo.org/api/'
#base_url = 'https://sandbox.zenodo.org/api/'

#modify the range if only part of the id file needs to be processed
init = 0
endit = len(updids)

print(str(datetime.datetime.now()))

#process the list of ids in a loop
#using try catches to avoid the whole script crashing if a request times out
#which can definitely happen, so check your log afterwards
for i in range(init, endit):
    quicklog.write('%s\t' % updids['id'][i])
    try:
        #get the current metadata of the record
        r = requests.get(base_url + 'records/%i' % updids['id'][i],
            headers=headers)
            
        logfilepub.write(json.dumps(r.json(),
            indent=4,
            sort_keys=True))
        logfilepub.write(',')
        quicklog.write('%s\t' % r.status_code)
        
        #modify the metadata by adding the MeiseBG community identifier
        expor = r.json()
        mdata = {'metadata' : expor['metadata']}
        if 'communities' in mdata['metadata']:
            mdata['metadata']['communities'].append({'identifier':'meisebotanicgarden'})
        else:
            mdata['metadata']['communities'] = [{'identifier':'meisebotanicgarden'}]

        #delete the record's own identifier to avoid the API refusing your request
        del mdata['metadata']['related_identifiers'][0]
        
        try:
            #open the record for editing
            r2 = requests.post(base_url + 'deposit/depositions/%i/actions/edit?access_token=%s' % (updids['id'][i],
                access_token))
                
            logfilepub.write(json.dumps(r2.json(),
                indent=4,
                sort_keys=True))
            logfilepub.write(',')
            quicklog.write('%s\t' % r2.status_code)
            
            #update the record's metadata
            r3 = requests.put(base_url + 'deposit/depositions/%i' % updids['id'][i],
                params = {'access_token': access_token}, data = json.dumps(mdata),
                headers = headers2)
                
            logfilepub.write(json.dumps(r3.json(),
                indent=4,
                sort_keys=True))
            logfilepub.write(",")
            quicklog.write('%s\t' % r3.status_code)
            
            #Publish the record again
            r4 = requests.post(base_url + 'deposit/depositions/%i/actions/publish?access_token=%s' % (updids['id'][i],
                access_token))
                
            logfilepub.write(json.dumps(r4.json(),
                indent=4,
                sort_keys=True))
            quicklog.write('%s\t' % r4.status_code)
            
            if i != endit-1:
                logfilepub.write(',')
                
        except:
            quicklog.write('%s\n' % sys.exc_info()[0])
            
    except:
        quicklog.write('%s\n' % sys.exc_info()[0])
        
    quicklog.write('\n')
    
print(str(datetime.datetime.now()))

logfilepub.write(']')
logfilepub.close()
quicklog.close()