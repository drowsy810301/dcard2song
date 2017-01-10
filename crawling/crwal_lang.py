#-*-coding: utf-8 -*-
import urllib, urllib2
import requests
from bs4 import BeautifulSoup, NavigableString
import re
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

new_album = []
hot_songs = []
hot_album = []
#all_songs = []

def crawl_lang(url):
    lang = ''
    #get the request
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    #use beautifulsoup packet
    soup = BeautifulSoup(html_doc.text, from_encoding="utf-8")
    h2 = soup.find('h2')

    pattern = re.compile(ur'】【 國語 】')
    for content in h2.contents:
        print type(content)
        if content.__class__ == NavigableString:
            print content
            idx = pattern.search(content)
            if idx:
                return u'國語'

    return u'非國語'


def crawl_all(url, all_songs, album_len, month):

    #get the request
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    #use beautifulsoup packet
    soup = BeautifulSoup(html_doc.content, 'html.parser', from_encoding="utf-8")
    dds = soup.find_all('dd')

    print '=======================' + str(month) + '======================='
    i = 0

    #find the correct tag
    for dd in dds:

        all_songs['album'].append({})
        singer = dd.find('a')
        aname = singer.find_next_sibling('a')
        singer = singer.contents[0]

        album_href = aname.get('href')
        #this block is exception condition

        if str(aname.contents[0])[:3] == '<sp':
            aname = aname.contents[0].contents[0]
        else:
            aname = aname.contents[0]
        print str(singer) + ': ' + str(aname)

        #store the album info
        all_songs['album'][album_len + i]['singer'] = str(singer)
        all_songs['album'][album_len + i]['name'] = str(aname)
        lang = ''
        #all_songs[0]['album'][album_len + i]['href'] = str(album_href)
        #print str(album_href)
        lang = crawl_lang('https://mojim.com'+str(album_href))
        all_songs['album'][album_len + i]['href'] = str(lang)
        all_songs['album'][album_len + i]['month'] = str(month)

        #all_songs['album'][album_len + i]['songs'] = []

        i = i + 1

    return all_songs

#encode the data to json file and output
def write_json(file_name, data):
    f = open(file_name+'_lang.json', 'w')
    json_data = json.dumps(data)
    f.write(json_data)
    f.close()

if __name__ == '__main__':

    #command form the user
    select = raw_input('1)hot songs and albums 2)latest albums 3)all songs in the year(enter the year later): ')
    if select == '1':
        #crawl hot songs and album
        hot_songs = crawl_hot_songalbum('http://mojim.com/twzhot-song.htm', hot_songs, 'mx5_A')
        write_json('hot_songs', hot_songs)
        hot_album = crawl_hot_songalbum('http://mojim.com/twzhot-cd.htm', hot_album, 'mx4_A')
        write_json('hot_album', hot_album)

    elif select == '2':
        #craw latest album
        crawl_new_album('https://mojim.com/', 'new_album_all')
        crawl_new_album('https://mojim.com/twzlistA.htm', 'new_album_male')
        crawl_new_album('https://mojim.com/twzlistB.htm', 'new_album_female')
        crawl_new_album('https://mojim.com/twzlistC.htm', 'new_album_group')
        crawl_new_album('https://mojim.com/twzlistE.htm', 'new_album_EUAM')
        crawl_new_album('https://mojim.com/twzlistF.htm', 'new_album_JAKO')
        crawl_new_album('http://mojim.com/twzlistZ.htm', 'new_album_other')
        write_json('new_album', new_album)

    elif select == '3':
        #craw all songs in the year
        year = raw_input('year: ')
        if int(year) not in range(2000, 2017):
            print 'Wrong input!'
            sys.exit(1)

        all_songs = {}
        all_songs['year'] = year
        all_songs['album'] = []

        #craw all songs in January to December in order
        for i in range(1, 13):
            if i < 10:
                month = '0' + str(i)
            else:
                month = str(i)
            all_songs_each_year = crawl_all('https://mojim.com/twzlist' + str(year) + '-' + month + '.htm', all_songs, len(all_songs['album']), i)

        write_json('all_songs_' + str(year), all_songs)
    else:
        print 'Not a valid selection!'
        sys.exit(1)
