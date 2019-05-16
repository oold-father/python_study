import requests
import json

url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
def translate(url,word=None):
    payload = {
        'i': word,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': '15577985003246',
        'sign': '01d488f8f786f9eee745e30043021cd5',
        'ts': '1557798500324',
        'bv': '316dd52438d41a1d675c1d848edf4877',
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME'
    }

    header ={
        
    }
    response = requests.post(url,data=payload)
    print(response.text)

if __name__ =='__main__':
    translate(url,'猫')