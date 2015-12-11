#encoding=utf-8

from selenium import webdriver

browser = webdriver.Firefox()


browser.get('http://image.baidu.com/')  
browser.implicitly_wait(60)
elem = browser.find_element_by_link_text('stu')
elem.click()
elem = browser.find_element_by_link_text('从本地上传')
#elem.click()

elem = browser.find_element_by_id("stfile")
elem.send_keys('D:\Workspace-Python\kenan.jpg')


