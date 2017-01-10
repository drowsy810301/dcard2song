#-*-coding: utf-8 -*-
from __future__ import division
import json
from pprint import pprint
from bs4 import BeautifulSoup
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')



if __name__ == '__main__':
    data3 = {}
    data3['album'] = []
    if len(sys.argv) < 2:
        print 'You need the json file!'
        sys.exit(1)

    with open(sys.argv[1]) as data_file1:
        data1 = json.load(data_file1)

    with open(sys.argv[2]) as data_file2:
        data2 = json.load(data_file2)

    pattern = re.compile('songs_')
    idx = pattern.search(sys.argv[1])
    idx = idx.end(0)
    year = sys.argv[1][idx:idx+4]

    for i in range(0, len(data1['album'])):
        for j in range(0, len(data2['album'])):
            if data1['album'][i]['name'] == data2['album'][j]['name'] and data1['album'][i]['singer'] == data2['album'][j]['singer']:
                if(data2['album'][j]['href'] == '國語'):
                    data3['album'].append(data1['album'][i])
                    data3['album'][-1]['lang'] = data2['album'][j]['href']
                break;

    print len(data3['album'])

    f = open(str(year)+'.json', 'w')
    json_data = json.dumps(data3)
    f.write(json_data)
    f.close()
