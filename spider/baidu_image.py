import requests 
import json
import re
          
def get_page(url,keyword,num):
    payload = {
        'tn':'resultjson_com',
        'ipn':'rj',
        'ct': 201326592,
        'is':'',
        'fp':'result',
        'queryWord':keyword,
        'cl':2,
        'lm':-1,
        'ie':'utf-8',
        'oe':'utf-8',
        'adpicid':'',
        'st':-1,
        'z':'',
        'ic':0,
        'hd':'',
        'latest':'',
        'copyright':'',
        'word':keyword,
        's':'',
        'se':'',
        'tab':'',
        'width':'',
        'height':'',
        'face':'0',
        'istype':'2',
        'qc':'',
        'nc':'1',
        'fr':'',
        'expermode':'',
        'force':'',
        'pn':num,
        'rn':'30',
        'gsm':hex(num),
        '1557803274366':'',
    }

    img_num = 0
    for j in range(1,num+1):
        payload['pn'] = j*30
        payload['gsm'] = hex(j*30)

        response = requests.get(url,params=payload)
        jsdata = json.loads(response.text)
        for i in range(30):  
            img_url = decode(jsdata['data'][i]['objURL'])
            print(img_url)
            #下载图片
            re =requests.get(img_url)    
            with open('baiduimg/pic_{0:02d}.png'.format(img_num),'wb') as f:
                f.write(re.content)
                print('图片pic_{0:02d}.png'.format(img_num),'下载完成')
            img_num += 1

            
def decode(str):
    res = ''
    special = ['_z2C$q','_z&e3B','AzdH3F']

    table = {
        'w': "a",'k': "b",'v': "c",'1': "d",'j': "e",'u':"f",\
        '2':"g",'i':"h",'t':"i",'3':"j",'h':"k",'s':"l",'4':"m",\
        'g': "n",'5':"o",'r':"p",'q': "q",'6': "r",'f': "s",'p': "t",\
        '7': "u",'e': "v",'o': "w",'8': "1",'d': "2",'n': "3",'9': "4",\
        'c': "5",'m': "6",'0': "7",'b': "8",'l': "9",'a': "0",'_z2C$q': ":",\
        "_z&e3B": ".",'AzdH3F': "/"   }
    if (str == None) or ('http' in str):
        return str
    else:
        temp = str
        for s in special:
            temp = temp.replace(s,table[s])
        for c in temp:
            if re.match('^[a-w\d]+$',c):
                c = table[c]
            res= res+c
        return res

def mian():
    url ='https://image.baidu.com/search/acjson'
    word = u'键盘'
    get_page(url,word,2)

if __name__ == "__main__":
    mian()