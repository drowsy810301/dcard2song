#-*-coding: utf-8 -*-
import urllib, urllib2
import requests
from bs4 import BeautifulSoup
import re
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

new_album = []
hot_songs = []
hot_album = []
#all_songs = []

def crawl_new_album(url, album_type):

    alb = []
    #get the request
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    #use beautifulsoup packet
    soup = BeautifulSoup(html_doc.content, 'html.parser', from_encoding="utf-8")

    #find all new release albums
    new_all = soup.find('div', id='inS')
    new_all = new_all.find_all('dd')

    j = 0

    #store every album's info
    for album in new_all:
        title = album.find('h1')

        #this block is exception condition
        if title == None:
            continue
        alb.append({})
        date = title.next_sibling
        singer = title.find('a')
        date = singer.previous_sibling.strip(' \t\n\r')
        name = singer.find_next_sibling('a')
        songs = album.find_all('span')

        #use regular expresion to find th date
        pattern = re.compile(r'[0-9]{4}')
        match = pattern.match(str(date)[:4])
        if(len(str(date)) > 4) and match:
            alb[j]['date'] = str(date)
        alb[j]['singer'] = str(singer.string)
        alb[j]['name'] = str(name.string)

        #store the song list
        alb[j]['song'] = []
        if len(songs) > 0:
            i = 1
            for song in songs:
                name = song.find('a').string
                alb[j]['song'].append(str(name))
                i = i + 1
        j = j + 1

    #write_json(album_type, alb)
    alb_type = album_type[10:]

    #store the album type
    new_album.append({})
    if  alb_type == 'all':
        new_album[0]['type'] = 'all'
        new_album[0]['alb'] = alb
    elif alb_type == 'male':
        new_album[1]['type'] = 'male'
        new_album[1]['alb'] = alb
    elif alb_type == 'female':
        new_album[2]['type'] = 'female'
        new_album[2]['alb'] = alb
    elif alb_type == 'group':
        new_album[3]['type'] = 'group'
        new_album[3]['alb'] = alb
    elif alb_type == 'EUAM':
        new_album[4]['type'] = 'EUAM' #European and American
        new_album[4]['alb'] = alb
    elif alb_type == 'JAKO':
        new_album[5]['type'] = 'JAKO' #Japanese or Korean
        new_album[5]['alb'] = alb
    elif alb_type == 'other':
        new_album[6]['type'] = 'other'
        new_album[6]['alb'] = alb


def crawl_hot_songalbum(url, data, ID):
    #get the request
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    #use beautifulsoup packet
    soup = BeautifulSoup(html_doc.content, 'html.parser', from_encoding="utf-8")
    hot_songs_types = soup.find_all('div', id=ID)
    j = 0

    data = []
    for hot_songs_type in hot_songs_types:
        data.append({})
        data[j]['song'] = []
        hsongs = hot_songs_type.find_all('td')
        i = 0
        for hsong in hsongs:

            #find the song list type
            if i == 0:
                htype = hsong.find('strong')
                htype = str(htype.string[8:10])
                data[j]['type'] = htype

                i = i + 1
                continue

            name = hsong.find('a')

            #this block is exception condition
            if name == None:
                continue

            data[j]['song'].append({})

            #find the song list and store every songs info
            singer = name.find_next_sibling('a')
            if ID == 'mx5_A':
                pattern = re.compile('\.')
                idx = pattern.search(name.string)
                idx = idx.end(0)
                data[j]['song'][i-1]['name'] = str(name.string[idx:])
            else:
                data[j]['song'][i-1]['name'] = str(name.string)

            singer = singer.string[2:]
            singer = singer[:len(singer)-2]
            data[j]['song'][i-1]['singer'] = str(singer)
            i = i + 1
        j = j + 1
    return data

def crawl_album_detail(url):
    #get the request
    album_detail = {}
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    #use beautifulsoup packet
    soup = BeautifulSoup(html_doc.content, 'html.parser', from_encoding="utf-8")
    h2 = soup.find('h2')
    h2 = h2.string

    #purify the string and store the value of language and month
    lang = h2[len(h2)-10:len(h2)-13]
    month = h2[len(h2)-5:len(h2)-2]
    album_detail['lang'] = str(lang)
    album_detail['month'] = str(month)
    return album_detail

def crawl_lyrics(url):

    #get the request
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)
    #use beautifulsoup packet
    soup = BeautifulSoup(html_doc.content, 'html.parser', from_encoding="utf-8")
    ctents = soup.find('dd', id="fsZx3")

    #this block is exception condition
    if ctents == None:
        return 'error'

    ctents = ctents.contents
    lyrics = ''

    #flag use to cut the ad info
    flag = False
    for ctent in ctents:
        if flag == True:
            flag = False
            continue

        #replace the <br> tag with newline '\n'
        if str(ctent) == '<br/>':
            lyrics = lyrics + '\n'

        #cut the ad info
        elif str(type(ctent)) == "<class 'bs4.element.NavigableString'>":
            if str(ctent[0]) == u'更':
                continue
            else:
                lyrics = lyrics + str(ctent)
        else:
            flag = True
            continue

    return lyrics

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
        #all_songs[0]['album'][album_len + i]['album_href'] = str(album_href)
        all_songs['album'][album_len + i]['month'] = str(month)
        all_songs['album'][album_len + i]['songs'] = []

        k = 0
        m0as = dd.find_all('span', 'm0a')

        #store the all song's info in the album
        for m0a in m0as:
            all_songs['album'][album_len + i]['songs'].append({})
            t1 = m0a.find('a', 't1')

            if t1 == None:
                t2 = m0a.find('a', 't2')
                sname = t2.string
                all_songs['album'][album_len + i]['songs'][k]['name'] = str(sname)
                #all_songs['album'][album_len + i]['songs'][k]['href'] = False
                k = k + 1
                continue

            sname = t1.string
            shref = t1.get('href')
            all_songs['album'][album_len + i]['songs'][k]['name'] = str(sname)
            #all_songs['album'][album_len + i]['songs'][k]['href'] = str(shref)
            lyrics = ''

            #crawl the lyrics in nest
            lyrics = crawl_lyrics('https://mojim.com' + str(shref))
            all_songs['album'][album_len + i]['songs'][k]['lyrics'] = lyrics

            k = k + 1

        i = i + 1

    return all_songs

#encode the data to json file and output
def write_json(file_name, data):
    f = open(file_name+'.json', 'w')
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
