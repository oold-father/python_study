from selenium import webdriver
import requests

'''
https://tieba.baidu.com/p/3910118183
'''

#禁止浏览器的图片和js
chromeOpt = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values': {
        'images': 2,
        'javascript':2,
    }
}


chromeOpt.add_experimental_option('prefs',prefs)
chrome = webdriver.Chrome(chrome_options=chromeOpt)

chrome.get("https://tieba.baidu.com/p/3910118183")


url = chrome.find_elements_by_xpath(r'//*[@id="post_content_71962012327"]/img')
urls = [src.get_attribute('src') for src in url]

#chrome.close()
chrome.quit()

for i in range(len(urls)):
    re =requests.get(urls[i])
    with open('image/pic_'+str(i)+".png",'wb') as f:
        f.write(re.content)
        print('图片',i,'下载完成')

print('done!')
    

