#coding=utf-8
'''
Created on 2016年4月19日
@author: XiaoXiang
'''
#这里做一个批量的版本，通过爬虫爬取所有的收藏列表，批量下载
#本人现在的系统为python3.5

import urllib.request,urllib.parse
import re,os
   
def analysis(url,dirpath):
    if not os.path.isdir(dirpath):
      os.makedirs(dirpath)
    url=str(url)
    if url == '':
        print('错误，您的歌曲列表为空')
    else:
        if 'http://' in url:
            ID=re.search(r'\d+',url).group()
        else:
            ID=url
        try:
             mainurl='http://www.xiami.com/widget/xml-single/sid/'  
             url=mainurl+ID
        except Exception as m:
            print(Exception+":"+m)
        header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        request = urllib.request.Request( url, headers = header)  
        response = urllib.request.urlopen(request)
        html=response.read()
        flash=re.findall(b'<location><!\[CDATA\[(.*)\]\]></location>',html)
        flash=flash[0].decode("utf-8")
        name=re.findall(b'<song_name><!\[CDATA\[(.*)\]\]></song_name>',html)
        artist=re.findall(b'<artist_name><!\[CDATA\[(.*)\]\]></artist_name>',html)
        name=name[0].decode("utf-8")
        artist=artist[0].decode("utf-8")
        replacechar=str('\/:*?"<>|')
        for i in replacechar:
            if name.find(i)>-1:
                name=name.replace(i, '')
        for i in replacechar:
            if artist.find(i)>-1:
                artist=artist.replace(i, '')
        musicname=artist+'-'+name+'.mp3' 
        print(musicname)
        print(flash)
        row=flash[0]
        row=int(row)
        print(row)
        tempurl=flash[1:]
        print(tempurl)
        length=len(tempurl)
        rowlen=int(length/row)
        reminder=length%row
        remindertop=reminder
        stringlist=[]
        position=0
        for i in range(row):
            if reminder>0:
                stringlist.append(tempurl[position:position+rowlen+1])
                position+=rowlen+1
                reminder-=1
            else:
                stringlist.append(tempurl[position:position+rowlen])
                position+=rowlen
        realurl=''
        for i in range(rowlen):
            for j in range(len(stringlist)):
                realurl+=str(stringlist[j][i])
        for m in range(remindertop):
            realurl+=str(stringlist[m][-1])
        print(realurl)
        realurl=urllib.parse.unquote(realurl)
        realurl=realurl.replace('^','0')
        path=dirpath+'\\'+str(musicname)
        if  os.path.isfile(path)==False:
            urllib.request.urlretrieve(realurl,path)
        else:
            pass

    
analysis(3561993,"D:/xiami_music")