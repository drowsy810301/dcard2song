#-*-coding: utf-8 -*-
from __future__ import division
import json
from pprint import pprint
from bs4 import BeautifulSoup
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

#write the header in html file
def write_header(f):
    f.write("""<head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="bootstrap.min.css" media="screen">
        <script src="jquery-3.1.1.min.js"></script>
        <script src="bootstrap.min.js"></script>
      </head>""")
    return f

#write the song list html and insert the lyrics to the atrribute 'lyrics'
def write_song_list(songs):

    l_html = ''
    l_html = l_html + '<ul class="list-group">'

    for song in songs:
        #print song['name']
        l_html = l_html +  '<li class="list-group-item"><h4>'
        if 'lyrics' in song:
            l_html = l_html + '<a href="" data-toggle="modal" data-target="#myModal" class="lyrics" lyrics_link="" ' \
                + 'stitle="' + str(song['name']) + '" ' + 'lyrics="' + str(song['lyrics']) + '" >' \
                + song['name'] + '</a></h4></li>'
        else:
            l_html = l_html + song['name'] + '</h4></li>'

    l_html = l_html + '</ul>'
    return l_html

#write the pop-out window html
def write_lyrics():
    lyrics = ''
    lyrics = lyrics + """
        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>"""
    lyrics = lyrics + '<h3 class="modal-title" id="myModalLabel"></h3>'
    lyrics = lyrics + """
              </div>
              <h4><div class="modal-body"></div><h4>
            </div>
          </div>
        </div>"""
    return lyrics

def write_body(f, data):

    #write the title
    f.write('<div class="container"><h1>Mojim.com 魔鏡歌詞網</h1><hr/>')

    html = write_lyrics()
    f.write(html)

    #write the song-list block(three in the row) html
    for i in range(0, len(data['album']), 3):

        f.write('<div class="row">')
        html = '<div class="col-md-4"><h3>' \
        + data['album'][i]['singer'] + ': ' + data['album'][i]['name'] + '</h3>'
        f.write(html)

        html = write_song_list(data['album'][i]['songs'])
        f.write(html)
        f.write('</div>')

        if i + 1 < len(data['album']):

            html = '<div class="col-md-4"><h3>' \
            + data['album'][i+1]['singer'] + ': ' + data['album'][i+1]['name'] + '</h3>'
            f.write(html)
            html = write_song_list(data['album'][i+1]['songs'])
            f.write(html)
            f.write('</div>')

        if i + 2 < len(data['album']):

            html = '<div class="col-md-4"><h3>' \
            + data['album'][i+2]['singer'] + ': ' + data['album'][i+2]['name'] + '</h3>'
            f.write(html)
            html = write_song_list(data['album'][i+2]['songs'])
            f.write(html)
            f.write('</div>')

        f.write('</div><hr/>')
    f.write('</div>')

    #this juery will trigger the pop-out window to show the lyrics
    html = """<script type="text/javascript">
        $( ".lyrics" ).click(function() {
          console.log(this);
          console.log(this.getAttribute("lyrics_link"));
          console.log(typeof(this.getAttribute("lyrics_link")));
          $( "#myModalLabel" ).text(this.getAttribute("stitle"));
          var obj = $( ".modal-body" ).html(this.getAttribute("lyrics"));
          obj.html(obj.html().replace(/\\n/g,'<br/>'))
        });
      </script>"""
    f.write(html)

    return f

def write_file(file_name, year):
    json_file = 'all_songs_' + str(year) + '.json'
    #read the json file
    with open(file_name) as data_file:
        data = json.load(data_file)

    #write the html file
    f = open(year + '.html', 'w')

    f.write('<!DOCTYPE html><html lang="en">')
    f = write_header(f)
    f.write('<body>')
    f = write_body(f, data)
    f.write('</body></html>')

    f.close()

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'You need the json file!'
        sys.exit(1)

    #read the json file in order
    else:
        for i in range(1, len(sys.argv)):
            '''
            pattern = re.compile('songs_')
            idx = pattern.search(sys.argv[i])
            idx = idx.end(0)
            '''
            year = sys.argv[i][-9:-5]

            #check year whether is 2000~2016
            if int(year) not in range(2000, 2017):
                print 'Wrong year!'
                sys.exit(1)
            write_file(sys.argv[i], year)
