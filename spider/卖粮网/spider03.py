from selenium import webdriver
import requests
import codecs

'''
http://www.mailiangwang.com/
商家名称|商品品类|产地|供货地|等级|年份|价格类型|参考单价(元/吨)|供货时间
'''
#禁止浏览器的图片和js


url = 'http://www.mailiangwang.com'
filename = '最新稻谷报价.txt'

def get_form(url,fiename):

    chromeOpt = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
            'javascript':2,
        }
    }
    chromeOpt.add_experimental_option('prefs',prefs)
    chrome = webdriver.Chrome(chrome_options=chromeOpt)
    chrome.get(url)

    titles = [index.text for index in chrome.find_elements_by_xpath(r'//*[@id="paddy_supply"]/div[1]/span')]
    records = []
    for i in range(2,6):
        
        xpath = r'//*[@id="paddy_supply"]/div['+str(i)+']/div[1]/span'
        record = []
        for index in chrome.find_elements_by_xpath(xpath):
            text = index.get_attribute('title')
            if text:
                record.append(index.get_attribute('title'))
            else:
                record.append(index.text)
                
        
        record = '|'.join(record)
        records.append(record)
    
    with codecs.open(filename,'w','utf-8') as f:
        f.write("|".join(titles)+"\n")
        for i in records:
            f.write(i+"\n")
    chrome.quit()

get_form(url,filename) 

