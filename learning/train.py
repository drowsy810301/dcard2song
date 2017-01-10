#-*-coding: utf-8 -*-
from gensim.models import word2vec
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    sentences = word2vec.Text8Corpus("seg.txt")
    for i in range(5, 6): #window
        for j in range(250, 251, 50): #size
            for k in ['s']: #model name
                if k == 'c':
                    sg = 0
                else:
                    sg = 1
                model = word2vec.Word2Vec(sentences, size=j, sg=sg, window=i)
                model.save_word2vec_format(k + "_0" + str(i) + "_" + str(j) + ".model.bin", binary=True)

    #special case
    '''
    model = word2vec.Word2Vec(sentences, size=500, sg=0, window=10, hs=1, iter=10)
    model.save_word2vec_format("c_10_500.model.bin", binary=True)
    '''
