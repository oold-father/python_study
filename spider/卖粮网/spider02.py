from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import codecs

'''
http://www.mailiangwang.com/
'''

#禁止浏览器的图片和js
chromeOpt = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript':2,
    }
}

url = 'http://www.mailiangwang.com'
filename = '最新参考价格.txt'

"""
名称|涨跌幅|最新价|昨收|今收|最高|最低|买入|卖出|成交量
"""
def get_text(url,filename):
    chromeOpt.add_experimental_option('prefs',prefs)
    chrome = webdriver.Chrome(chrome_options=chromeOpt)
    chrome.get(url)
    
    records = [index.text for index in chrome.find_elements_by_xpath(r'//*[@id="fuCornPrice"]')]
    records = ''.join(records).split('\n')
    
    with codecs.open(filename,'w','utf-8') as f:
        f.write('名称|涨跌幅|最新价|昨收|今收|最高|最低|买入|卖出|成交量\n')
        for i in range(len(records)):
            if i%10 == 0 and i != 0:
                f.write('\n')
            
            f.write(records[i]+"|")

       
    chrome.quit()

get_text(url,filename)

