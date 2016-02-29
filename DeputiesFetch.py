import json
import urllib2
import os
import sys
import pickle as pkl
import argparse
from progressbar import ProgressBar

pbar = ProgressBar()
parser = argparse.ArgumentParser()

parser.add_argument('--pics', '-p',
                    action='store_true',
                    help='Download pictures')
parser.add_argument('--json', '-j',
                    action='store_true',
                    help='Download data')

data_directory = 'deputy_data'
pics_directory = 'deputy_pics'

# check if any argument, if so parse them
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

print "Download deputes en mandat"
response = urllib2.urlopen('http://www.nosdeputes.fr/deputes/enmandat/json')
deplist = json.loads(response.read())['deputes']

# get the list of all deputies with a current mandat
print "Build deputes url list"
urls = []
for l in deplist:
  urls.append(l['depute']['url_nosdeputes_api'])

if(args.json):
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


if(args.pics):
  # create the picts directory if it does not exists
  if not os.path.exists(pics_directory):
      os.makedirs(pics_directory)

  # now fetch the picture of each deputy, use an_id as a name
  print "Download Depute pictures"
  for dep in pbar(list(deplist)):
    url_name = dep['depute']['url_nosdeputes'].split('/')[-1]
    id_an = dep['depute']['id_an']
    pic_url = 'http://www.nosdeputes.fr/depute/photo/'+url_name

    #print "open",pics_directory+'/'+str(id_an)+'.png'
    with open(pics_directory+'/'+str(id_an)+'.png', 'wb') as output:
      output.write(urllib2.urlopen(pic_url).read())

  print "Process finished"