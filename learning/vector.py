#-*-coding: utf-8 -*-
from __future__ import division
import json
from pprint import pprint
from gensim.models import word2vec
from gensim import models
from bs4 import BeautifulSoup
import jieba
import sys
import re
import os
reload(sys)
sys.setdefaultencoding('utf-8')


def calculate(file_name, t, vsize):
    with open(file_name) as data_file:
        data = json.load(data_file)

    if t == 'dcard':
        for i in range(0, len(data)):
            vector = [0] * vsize
            data[i]['title_content']['content'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', data[i]['title_content']['content'], flags=re.MULTILINE)
            words = jieba.lcut(data[i]['title_content']['content'])
            for word in words:
                if word in model.vocab:
                    vector = map(lambda (x, y): x + y, zip(vector, model[word]))
            dcard_vector.append(vector)
            #print data[i]['title_content']['title']

    else:
        for i in range(0, len(data['album'])):
            for j in range(0, len(data['album'][i]['songs'])):
                vector = [0] * vsize
                words = jieba.lcut(data['album'][i]['songs'][j]['lyrics'], cut_all=False)
                for word in words:
                    if word in model.vocab:
                        vector = map(lambda (x, y): x + y, zip(vector, model[word]))
                song_vector.append(vector)
                #print data['album'][i]['songs'][j]['name']
                '''
                data['album'][i]['songs'][j]['vector'] = vector
                if vector == [0] * vsize:
                    print data['album'][i]['songs'][j]['name']
                '''


def write_file(vsize, window, mname):
    dirpath = './' + mname + '_' + window + '_' + str(vsize)
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

    if len(dcard_vector) > 0:
        fname = 'dcard_vector.json'
        f = open(dirpath + '/' + fname, 'w')
        json_data = json.dumps(dcard_vector)
        f.write(json_data)
        f.close()


    if len(song_vector) > 0:
        fname = 'song_vector.json'
        f = open(dirpath + '/' + fname, 'w')
        json_data = json.dumps(song_vector)
        f.write(json_data)
        f.close()

if __name__ == '__main__':
    print sys.argv[1]
    if len(sys.argv) < 3:
        print 'You need the input file!'
        sys.exit(1)

    else:
        stopwordset = set()
        with open('stopwords.txt','r') as sw:
            for line in sw:
                stopwordset.add(unicode(line.strip('\n'), 'utf-8'))

        bin_file = sys.argv[1]
        vsize = int(bin_file[-13:-10])
        window = bin_file[-16:-14]
        mname = bin_file[-18:-17]

        model = models.Word2Vec.load_word2vec_format(sys.argv[1],binary=True)
        dcard_vector = []
        song_vector = []
        for i in range(2, len(sys.argv)):
            pattern = re.compile('dcard')
            if pattern.search(sys.argv[i]):
                t = 'dcard'
            else:
                t = 'songs'

            #year = sys.argv[i][-9:-5]
            print '================' + sys.argv[i] + '================'
            calculate(sys.argv[i], t, vsize)

        write_file(vsize, window, mname)

