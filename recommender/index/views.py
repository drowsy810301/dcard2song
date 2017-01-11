#-*- encoding=UTF-8 -*-
from django.shortcuts import render
from index.recomm import crawl
from gensim import models
from gensim.models import word2vec
#from index.recomm import model
from index.recomm import find_song
from index.apikey import api
def index(request):
    article = ''
    #word = u'自由'
    if request.method == 'POST':
        url = request.POST.get("link")
        article = crawl(url)
        #return render(request, "index.html", {'article_content': article_content})
        #print len(model[word])
        #song_list = find_song(model)
        song_list = find_song(article['content'])
        return render(request, "index.html", {'article': article, 'song_list': song_list, 'api': api})

    return render(request, "index.html", {'article': article})
