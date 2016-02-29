import json
import urllib2
import os
import sys
import pickle as pkl
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('--pics', '-p',
                    action='store_true',
                    help='Download pictures')
parser.add_argument('--json', '-j',
                    action='store_true',
                    help='Download data')

# directories where to download data
data_directory = 'deputy_data'
pics_directory = 'deputy_pics'

# check if any argument, if so parse them
try:
  args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(1)


print "Download deputes en mandat"
response = urllib2.urlopen('http://www.nosdeputes.fr/deputes/enmandat/json')
deplist = json.loads(response.read())['deputes']

# get the list of all deputies with a current mandat
print "Build deputes url list"
deps = []
for i in tqdm(range(len(deplist))):
  deps.append(deplist[i]['depute'])

if(args.json):
  # download the json doc for each deputy
  print "Download Depute files:",len(deps)
  deputes = []
  for i in tqdm(range(len(deps))):
    dep_json = json.loads(urllib2.urlopen(deps[i]['url_nosdeputes_api']).read())['depute']
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


if(args.pics):
  # create the picts directory if it does not exists
  if not os.path.exists(pics_directory):
      os.makedirs(pics_directory)

  # now fetch the picture of each deputy, use an_id as a name
  print "Download Depute pictures"
  for i in tqdm(range(len(deps))):
    url_name = deps[i]['url_nosdeputes'].split('/')[-1]
    id_an = deps[i]['id_an']
    pic_url = 'http://www.nosdeputes.fr/depute/photo/'+url_name

    with open(pics_directory+'/'+str(id_an)+'.png', 'wb') as output:
      output.write(urllib2.urlopen(pic_url).read())

  print "Process finished"