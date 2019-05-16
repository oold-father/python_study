import requests  
from HandleJs import Py4Js
    
def translate_en_to_cn(tk,content):   
    if len(content) > 4891:    
        print("翻译的长度超过限制！！！")    
        return  
 
    param = {'tk': tk, 'q': content}
 
    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)

    print('原词：',result.json()[0][0][1])
    print('翻译结果：',result.json()[0][0][0])
    #返回的结果为Json，解析为一个嵌套列表
    '''
    for text in result.json():
        try:
            print(len(text))
            print(text)
        except:
            continue
        #print(text)
    '''    

def translate_cn_to_en(tk,content):   
    if len(content) > 4891:    
        print("翻译的长度超过限制！！！")    
        return  
 
    param = {'tk': tk, 'q': content}
 
    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=zh-CN
        &tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)

    print('原词：',result.json()[0][0][1])
    print('翻译结果：',result.json()[0][0][0])
    #返回的结果为Json，解析为一个嵌套列表
    '''
    for text in result.json():
        try:
            print(len(text))
            print(text)
        except:
            continue
        #print(text)
    '''  

def main():    
    js = Py4Js()    
         
    #content = "cat"

    content = "cat"
    test = '狗'

    tk_1 = js.getTk(content)
    tk_2 = js.getTk(test)

    translate_en_to_cn(tk_1,content)
    translate_cn_to_en(tk_2,test)    
        
if __name__ == "__main__":    
    main()