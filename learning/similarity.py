#-*-coding: utf-8 -*-
from __future__ import division
import json
from gensim.models import word2vec
from gensim import models
import jieba
import sys
import re
import os
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
import sqlite3
reload(sys)
sys.setdefaultencoding('utf-8')


def cal_similarity(avector, songs):
    rank = []
    for song in songs:
        tmp = song[2].split(',')
        if all(v == u'0' for v in tmp):
            continue

        svector = [float(x) for x in tmp]
        cos_sim = 1 - spatial.distance.cosine(avector, svector)
        rank.append((song[0], song[1], cos_sim))

    rank.sort(key=lambda tup: tup[2], reverse=True)

    c3 = conn.cursor()
    c3.execute("SELECT * FROM crawling")
    crawling_songs = c3.fetchall()

    for i in range(0, 50):
        #print crawling_songs[rank[i][1]][0]
        print "song index: {} song name: {} album name: {} singer: {} similarity: {}".format(rank[i][1], rank[i][0], crawling_songs[rank[i][1]][0], crawling_songs[rank[i][1]][3], rank[i][2])

    '''
    print type(1 - spatial.distance.cosine(data[target], data[target+1]))
    print type(cosine_similarity(data[target], data[target+1])[0][0])
    print cosine_similarity(data[target], data[target+1])[0][0]
    '''

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'argv error'
        sys.exit(1)

    bin_file = sys.argv[1]
    vsize = int(bin_file[-13:-10])
    window = bin_file[-16:-14]
    mname = bin_file[-18:-17]
    model = models.Word2Vec.load_word2vec_format(sys.argv[1], binary=True)

    conn = sqlite3.connect('../crawling/dcard.db')
    c = conn.cursor()
    c.execute("SELECT title, content FROM crawling WHERE likenum>100 and classname='感情'")
    article = c.fetchall()

    content = article[50][1]
    print '{}'.format(article[50][0])
    print '{}'.format(article[50][1])

    avector = [0] * vsize
    content = re.sub(r'^https?:\/\/.*[\r\n]*', '', content, flags=re.MULTILINE)
    words = jieba.lcut(content)
    for word in words:
        if word in model.vocab:
            avector = map(lambda (x, y): x + y, zip(avector, model[word]))

    conn = sqlite3.connect('../crawling/song.db')
    c2 = conn.cursor()
    table_name = mname + '_' + window + '_' + str(vsize)
    c2.execute("SELECT * FROM {}".format(table_name))
    songs = c2.fetchall()
    cal_similarity(avector, songs)
