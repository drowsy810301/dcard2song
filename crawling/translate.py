#-*-coding: utf-8 -*-
from __future__ import division
import json
from pprint import pprint
from bs4 import BeautifulSoup
import sys
import re
import opencc
reload(sys)
sys.setdefaultencoding('utf-8')



def translate(file_name, year):
    with open(file_name) as data_file:
        data = json.load(data_file)


    for i in range(0, len(data['album'])):
        for j in range(0, len(data['album'][i]['songs'])):
            data['album'][i]['songs'][j]['lyrics'] = opencc.convert(data['album'][i]['songs'][j]['lyrics'], config='s2t.json')

    f = open(file_name, 'w')
    json_data = json.dumps(data)
    f.write(json_data)
    f.close()

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'You need the json file!'
        sys.exit(1)

    else:
        for i in range(1, len(sys.argv)):

            '''
            pattern = re.compile('songs_')
            idx = pattern.search(sys.argv[i])
            idx = idx.end(0)
            '''
            year = sys.argv[i][-9:-5]

            if int(year) not in range(2000, 2017):
                print 'Wrong year!'
                sys.exit(1)

            translate(sys.argv[i], year)
