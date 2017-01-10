import sqlite3
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def insertdb(file_name, cmd, song_index=0):
    with open(file_name) as data_file:
        data = json.load(data_file)

    if cmd == '0':
        for i in range(0, len(data)):
            print i
            title = data[i]['title_content']['title']
            content = data[i]['title_content']['content']
            likenum = data[i]['title_content']['likenum']
            classname = data[i]['title_content']['classname']
            postnum = data[i]['postnum']
            c.execute("INSERT INTO crawling VALUES(?,?,?,?,?)", (classname, content, likenum, title, postnum))

    elif cmd == '1':
        year = int(file_name[-9:-5])
        for i in range(0, len(data['album'])):
            for j in range(0, len(data['album'][i]['songs'])):
                aname = data['album'][i]['name']
                month = int(data['album'][i]['month'])
                singer = data['album'][i]['singer']
                lyrics = data['album'][i]['songs'][j]['lyrics']
                sname = data['album'][i]['songs'][j]['name']
                c.execute("INSERT INTO crawling VALUES(?,?,?,?,?,?)", (aname, sname, lyrics, singer, month, year))

    elif cmd == '2':
        c.execute("SELECT sname from crawling")
        snames = c.fetchall()

        for i in range(0, len(data)):
            sname = snames[i][0]
            values = ",".join(str(value) for value in data[i])
            c.execute("INSERT INTO c_10_500 VALUES(?,?,?)", (sname, song_index, values))
            song_index = song_index + 1

if __name__ == '__main__':

    cmd = raw_input('cmd: ')
    if len(sys.argv) < 3:
        print 'You need the input file!'
        sys.exit(1)

    else:
        conn = sqlite3.connect(sys.argv[1])
        c = conn.cursor()
        for i in range(2, len(sys.argv)):
            insertdb(sys.argv[i], cmd)
        conn.commit()
        c = conn.cursor()
