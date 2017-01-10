#-*-coding: utf-8 -*-
from __future__ import division
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def count_song(file_name, year):

    with open(file_name) as data_file:
        data = json.load(data_file)

    ct = 0
    for i in range(0 , len(data['album'])):
        ct = ct + len(data['album'][i]['songs'])

    print '%s song number: %d' % (str(year), ct)
    return ct

def count_article(file_name, idx):

    with open(file_name) as data_file:
        data = json.load(data_file)

    ct = 0
    ct = len(data)

    print '%s article number: %d' % (str(idx), ct)
    return ct

if __name__ == '__main__':
    total_song = 0
    total_article = 0
    if len(sys.argv) < 2:
        print 'You need the json file!'
        sys.exit(1)

    else:
        for i in range(1, len(sys.argv)):

            y = ''
            pattern = re.compile('dcard')
            if pattern.search(sys.argv[i]):
                t = 'dcard'
                ylist = ['2243', '2245','2247','2249','2253','2255']
                for j in ylist:
                    pattern = re.compile(j)
                    if pattern.search(sys.argv[i]):
                        y = j
                total_article = total_article + count_article(sys.argv[i], y)
            else:
                t = 'songs'
                ylist = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014', '2015', '2016']
                for j in ylist:
                    pattern = re.compile(j)
                    if pattern.search(sys.argv[i]):
                        y = j
                total_song = total_song + count_song(sys.argv[i], y)

            '''
            with open(sys.argv[i]) as data_file:
                data = json.load(data_file)
            print '%s album number: %d' % (str(year), len(data['album']))
            '''
        print 'total song number: ' + str(total_song)
        print 'total article number: ' + str(total_article)
