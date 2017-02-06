#encoding=utf-8
#批量下载虾米音乐
#输入自己的账号密码，进入收藏列表，再输入开始页号和结束页号，批量下载
#这些页面之中的音乐
import urllib.request
import urllib.parse
from http import cookiejar
import re,os


header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	           'Accept-Encoding': 'none',
	           'Accept-Language': 'en-US,en;q=0.8',
	           'Connection': 'keep-alive',
	           }

#登陆函数，
def login(username,password):
	url='https://login.xiami.com/member/login?'
	user={
		'_xiamitoken': 'fbff784fbd58e4de3b68a47cad93dc8a',
		'done':'http%253A%252F%252Fwww.xiami.com',
		'from':'web',
		'havanaId':'',
		'email': username,
		'password': password,
		'submit':'%E7%99%BB+%E5%BD%95',
	}
	cookie=cookiejar.CookieJar()
	cj=urllib.request.HTTPCookieProcessor(cookie)
	opener=urllib.request.build_opener(cj)
	urllib.request.install_opener(opener)
	postdata=urllib.parse.urlencode(user).encode('utf-8')
	request=urllib.request.Request(url,postdata,header)
	response=urllib.request.urlopen(request).read()
	return response

def get_user_id(response):
	msg=str(response)
	#user_id=re.findall(r'\"user_id\"\:\"(.*)\"\,\"',msg)
	#2016-12-25更改该句，因网页变更
	user_id=re.findall(r'[0-9]{4,}',msg)
	user_id=str(user_id[0])
	return user_id


def getsong(user_id):
	start_page=input("please input start_page:")
	start_page=int(start_page)
	end_page=input("please input end_page:")
	end_page=int(end_page)
	id_list=[]
	for pagenum in range(start_page,end_page+1):
		url='http://www.xiami.com/space/lib-song/u/'+user_id+'/page/'+str(pagenum)+'?spm=a1z1s.6843761.226669510.3.oylhzA'
		request=urllib.request.Request(url,headers=header)
		html=urllib.request.urlopen(request).read()
		mp3_id=re.findall(b'value=\"(.*)\" checked',html)
		id_list+=mp3_id
	print(id_list)
	for id_num in id_list:
		id_num=id_num.decode('utf-8')
		print(id_num)
		try:
			anlasys(id_num)
		except:
			print('该音乐已经下架！')

def anlasys(url,dirpath="D:/xiami_music"):
    if not os.path.isdir(dirpath):
      os.makedirs(dirpath)
    url=str(url)
    if url == '':
        print('错误，您的歌曲列表为空')
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
        row=flash[0]
        row=int(row)
        tempurl=flash[1:]
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
        realurl=urllib.parse.unquote(realurl)
        realurl=realurl.replace('^','0')
        path=dirpath+'\\'+str(musicname)
        if  os.path.isfile(path)==False:
        	# try:
            urllib.request.urlretrieve(realurl,path)
            print(musicname+'下载成功')
            # except Exception,e:
            # 	print(e)
            # 	print(musicname+'下载失败')
        else:
            print(musicname+'有重复，不必下载该音乐')


if __name__=='__main__':
	'''user=input('input your user:')
	password=input('input your password:')'''
	user=''
	password=''
	res=login(user,password)
	user_id=get_user_id(res)
	getsong(user_id)
