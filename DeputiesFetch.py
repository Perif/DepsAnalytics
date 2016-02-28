import json
import urllib2
import pickle as pkl
from progressbar import ProgressBar
pbar = ProgressBar()


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


print "Write to disk"
# export to pickle
with open('deputes_data.pkl', 'wb') as output:
  pkl.dump(deputes,output)
with open('deputes_list.pkl', 'wb') as output:
  pkl.dump(deplist,output)
# export to json
with open('deputes_data.json', 'wb') as output:
  json.dump(deputes,output)
with open('deputes_list.json', 'wb') as output:
  json.dump(deplist,output)