#-*- encoding=UTF-8 -*-
from bs4 import BeautifulSoup
import requests
import sys
import re
from gensim import models
from gensim.models import word2vec
from recommender.settings import PROJECT_ROOT
import jieba
import json
from scipy import spatial
###
from index.models import S05250
from index.models import Crawling
reload(sys)
sys.setdefaultencoding('utf-8')
###
model = models.Word2Vec.load_word2vec_format(PROJECT_ROOT + '/data/bin/s_05_250.model.bin', binary=True)
###
vsongs = S05250.objects.all()
csongs = Crawling.objects.all()
def crawl(url):

    pattern = re.compile('-')
    aid = ''
    if pattern.search(url):
        idx = pattern.search(url).start(0)
        aid = url[idx-9:idx]

    print aid
    api = 'https://www.dcard.tw/_api/posts/' + aid + '?'

    tmp = requests.get(str(api))
    a = json.loads(tmp.text)
    print a['title']

    '''
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

        content = """大一時總不理解為何有人說大學交不到
    高中的摯友
    曾經深信身旁的室友會陪自己走過四年
    年級越大越能體悟出那種社會感

    雖然一起上課
    雖然就坐在隔壁
    雖然一起吃飯聊天

    可是討論的話題不再是自己熟悉的內容
    可是提到的人名不再是之前的那幾個人

    開始有些出外玩打卡沒有了自己
    開始有些約在事後才知道被放鳥
    開始要提問才知道她們在說什麼
    開始有些事可能永遠最後才知道

    就在想說算了的時候
    好像又開始跟她們有了交集
    過了一下子那交集又斷了聯繫

    起起落落的關係
    久了其實蠻累的
    不是不能自己一個人
    只是因為自己還在乎所以不想失去
    失去那份得來不易的友情


    尤其最討厭分組實驗
    以前總信誓旦旦的知道自己會有組
    現在總要擔心我是否會成為落單的那一個
    怕又找到雷的
    說好一起時
    然後交名單時你卻直接被放生他們再來跟你說

    啊 他們把我拉過去啊

    大學真的是一個你今天不搶先他 明天就就被他搶先了
    然後有些心機又是蠻傷人的
    可是明明知道他在幹麻卻還要裝作沒這回事
    整天笑臉迎人
    真是噁心

    只是有感而發啦
    哀哀

    我想我還是搬出去好了..'
    """
    '''
    article = {'title': a['title'], 'content': a['content']}
    return article

def find_song(article):

    ###
    avector = [0] * 250
    article = re.sub(r'^https?:\/\/.*[\r\n]*', '', article, flags=re.MULTILINE)
    words = jieba.lcut(article)
    for word in words:
        if word in model.vocab:
            avector = map(lambda (x, y): x + y, zip(avector, model[word]))


    r = []
    for song in vsongs:
        tmp = (song.val).split(',')
        if all(v == u'0' for v in tmp):
            continue
        svector = [float(x) for x in tmp]
        cos_sim = 1 - spatial.distance.cosine(avector, svector)
        r.append((song.name , song.index, cos_sim))
    r = sorted(r, key=lambda tup: tup[2], reverse=True)
    r = r[:5]
    rank = []
    for i in range(0,5):
        print r[i][2]
        rank.append({'sname': r[i][0], 'aname': csongs[r[i][1]].aname, 'singer': csongs[r[i][1]].singer, 'lyrics': csongs[r[i][1]].lyrics})
    return rank
