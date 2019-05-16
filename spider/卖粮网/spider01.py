from selenium import webdriver
import requests
import codecs

'''
http://www.mailiangwang.com/biz/list?province=&keyword=%E5%A4%A7%E7%B1%B3
http://www.mailiangwang.com/biz/list?province=&keyword=%E5%A4%A7%E7%B1%B3&pageid=2
'''

#禁止浏览器的图片和js
chromeOpt = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript':2,
    }
}


title_list =     []
capital_list =   []
addresses_list = []
category_list =  []

def get_text(url):
    chromeOpt.add_experimental_option('prefs',prefs)
    chrome = webdriver.Chrome(chrome_options=chromeOpt)
    chrome.get(url)
    #公司名
    titles =    chrome.find_elements_by_xpath(r'/html/body/div[3]/div[3]/div[1]/div/span[1]/a')
    #注册资本
    capitals =  chrome.find_elements_by_xpath(r'/html/body/div[3]/div[3]/div[1]/div/span[3]')
    #注册地址
    addresses = chrome.find_elements_by_xpath(r'/html/body/div[3]/div[3]/div[1]/div/span[5]')
    #主营
    category =  chrome.find_elements_by_xpath(r'/html/body/div[3]/div[3]/div[1]/div/span[6]')
    
    for i in range(1,len(titles)+1):
        title_list.append(titles[i-1].get_attribute('title'))
        capital_list.append(capitals[i].text)
        addresses_list.append(addresses[i].text)
        category_list.append(category[i].text)
    
    chrome.quit()

get_text('http://www.mailiangwang.com/biz/list?province=&keyword=%E5%A4%A7%E7%B1%B3')
get_text('http://www.mailiangwang.com/biz/list?province=&keyword=%E5%A4%A7%E7%B1%B3&pageid=2')

with codecs.open('data.txt','w','utf-8') as f:
        f.write("s1|s2|s3|s4\n")
        for i in range(len(title_list)):
            f.write(title_list[i]+"|"+capital_list[i]+"|"+addresses_list[i]+"|"+category_list[i]+"\n")

        print('done!')
