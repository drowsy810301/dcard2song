#-*- encoding=UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import re
from gensim import models
from gensim.models import word2vec
from recommender.settings import PROJECT_ROOT
import jieba
from scipy import spatial
###
from index.models import S05250
reload(sys)
sys.setdefaultencoding('utf-8')
###
model = models.Word2Vec.load_word2vec_format(PROJECT_ROOT + '/data/bin/s_05_250.model.bin', binary=True)

def crawl(url):
    try:
        html_doc = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        return False

    soup = BeautifulSoup(html_doc.text, from_encoding="utf-8")
    try:
        title = soup.find('h1', "Post_title_1T3V5").string
    except:
        title = ''
    try:
        date = soup.find('div', 'Post_published_13TGw')
        date = date.contents[0].string
    except:
        date = ''
    try:
        board = soup.find('a', 'Post_forum_2urwA').string
    except:
        board = ''
    try:
        author = soup.find('span', 'PostAuthor_root_3vAJf').string
    except:
        author = ''
    try:
        gender = soup.find('div', 'PostAuthorHeader_avatar_1V21V').contents[0]['class'][0]
        pattern = re.compile('female')
        if pattern.search(gender):
            gender = 'g'
        else:
            pattern = re.compile('male')
            if pattern.search(gender):
                gender = 'b'
            else:
                gender = 'n'
    except:
        gender = ''

    try:
        content = ''
    except:
        content = ''

    print gender
    article = {'title': title, 'content': content, 'author':author, 'board': board, 'date': date, 'gender': gender}
    return article

def find_song(article):
    obj = S05250.objects.all()
    print len(obj)
    '''
    ###
    avector = [0] * 250
    article = re.sub(r'^https?:\/\/.*[\r\n]*', '', article, flags=re.MULTILINE)
    words = jieba.lcut(article)
    for word in words:
        if word in model.vocab:
            avector = map(lambda (x, y): x + y, zip(avector, model[word]))
    '''
    '''
    r = []
    for song in songs:
        tmp = song[2].split(',')
        if all(v == u'0' for v in tmp):
            continue

        svector = [float(x) for x in tmp]
        cos_sim = 1 - spatial.distance.cosine(avector, svector)
        r.append((song[0], song[1], cos_sim))

    rank = sorted(r, key=lambda tup: tup[2], reverse=True)
    '''
