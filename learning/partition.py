#-*-coding: utf-8 -*-
from gensim.models import word2vec
import json
import jieba
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def is_number(s):
    try:
        if s.isdigit():
            return True
    except (TypeError, ValueError):
        pass
    except:
        pass

    try:
        float(s)
        return True
    except ValueError:
        pass
    except:
        pass

    return False

def partition(file_name, stopwordset, t, output):
    with open(file_name) as data_file:
        data = json.load(data_file)

    if t == 'dcard':
        for i in range(0, len(data)):
            data[i]['title_content']['content'] = re.sub(r'^https?:\/\/.*[\r\n]*', '', data[i]['title_content']['content'], flags=re.MULTILINE)
            words = jieba.lcut(data[i]['title_content']['content'])
            for word in words:
                if word != '\n' and word != u'\n' and not word.isspace() and word not in stopwordset:
                    if is_number(word):
                        continue
                    output.write(word + ' ')
    else:
        for i in range(0, len(data['album'])):
            for j in range(0, len(data['album'][i]['songs'])):
                words = jieba.lcut(data['album'][i]['songs'][j]['lyrics'], cut_all=False)
                for word in words:
                    if word != '\n' and word != u'\n' and not word.isspace() and word not in stopwordset:
                        if is_number(word):
                            continue
                        output.write(word + ' ')

if __name__ == '__main__':

    stopwordset = set()
    with open('stopwords.txt','r') as sw:
        for line in sw:
            stopwordset.add(unicode(line.strip('\n'), 'utf-8'))

    output = open('seg.txt','w')
    if len(sys.argv) < 2:
        print 'You need the json file!'
        sys.exit(1)

    else:
        for i in range(1, len(sys.argv)):
            '''
            year = sys.argv[i][-9:-5]
            if int(year) not in range(2000, 2017):
                print 'Wrong year!'
                sys.exit(1)
            '''
            print sys.argv[i]
            pattern = re.compile('dcard')
            if pattern.search(sys.argv[i]):
                t = 'dcard'
            else:
                t = 'songs'
            partition(sys.argv[i], stopwordset, t, output)
    output.close()
