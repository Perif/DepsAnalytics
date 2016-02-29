import json
import urllib2
import os
import pickle as pkl
from progressbar import ProgressBar
pbar = ProgressBar()


data_directory = 'deputy_data'

print "Download deputes en mandat"
response = urllib2.urlopen('http://www.nosdeputes.fr/deputes/enmandat/json')
deplist = json.loads(response.read())['deputes']

# get the list of all deputies with a current mandat
print "Build deputes url list"
urls = []
for l in deplist:
  urls.append(l['depute']['url_nosdeputes_api'])


# download the json doc for each deputy
print "Download Depute files:",len(urls)
deputes = []
for url in pbar(urls):
  dep_json = json.loads(urllib2.urlopen(url).read())['depute']
  deputes.append(dep_json)


# create the output directory if it does not exists
if not os.path.exists(data_directory):
    os.makedirs(data_directory)


print "Write to disk"
# export to pickle
with open(data_directory+'/deputes_data.pkl', 'wb') as output:
  pkl.dump(deputes,output)
with open(data_directory+'/deputes_list.pkl', 'wb') as output:
  pkl.dump(deplist,output)
# export to json
with open(data_directory+'/deputes_data.json', 'wb') as output:
  json.dump(deputes,output)
with open(data_directory+'/deputes_list.json', 'wb') as output:
  json.dump(deplist,output)