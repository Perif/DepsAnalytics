import json
import urllib2
import pickle as pkl
from progressbar import ProgressBar
pbar = ProgressBar()


print "Download deputes en mandat"
response = urllib2.urlopen('http://www.nosdeputes.fr/deputes/enmandat/json')
data = json.loads(response.read())

# get the list of all deputies with a current mandat
print "Build deputes url list"
urls = []
ids = []
for l in data['deputes']:
  urls.append(l['depute']['url_nosdeputes_api'])
  ids.append(l['depute']['id_an'])


# download the json doc for each deputy
print "Download Depute files:",len(urls)
deputes = {}
for dep in pbar(zip(urls,ids)):
  (url,uid) = dep
  dep_json = json.loads(urllib2.urlopen(url).read())
  deputes[uid] = dep_json


print "Write to disk"
# export to pickle
with open('deputes_data.pkl', 'wb') as output:
  pkl.dump(deputes,output)
with open('deputes_list.pkl', 'wb') as output:
  pkl.dump(data,output)
# export to json
with open('deputes_data.json', 'wb') as output:
  json.dump(deputes,output)
with open('deputes_list.json', 'wb') as output:
  json.dump(data,output)