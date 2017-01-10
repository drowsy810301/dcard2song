# music-recommender
---

##Final project of data science course
* Dataset: [Dcard](https://www.dcard.tw/f) and [Mojim](https://mojim.com/)
* Use jieba to segment text
* Use Word2vec to train data
* Each vector of an article or a song is the sum of all the word vector in it
* Input a dcard link, the recommender will output the top five songs which have the highest cosine similarity

####Dependencies:
* python2.7
* python-dev
* python-pip
* sqlite3
* nodejs
* npm
* bower
* django1.8
* django-bower
* requests
* jieba
* gensim

####Install dependencies (for ubuntu):
```
apt-get install sqlite3 libsqlite3-dev
apt-get remove nodejs
apt-get install curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g bower
pip install django-bower
python manage.py bower install
pip install gensim
pip install jieba
pip install requests
```
