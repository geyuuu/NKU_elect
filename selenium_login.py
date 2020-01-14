from selenium import webdriver,common
from time import sleep
import json
from urllib import request,parse
import re


print("南开大学捞课助手 v0.1\n\n请确保你退出了教务系统，将你的学号和密码保存在user_info.txt")
_=input("\n\n按回车键继续。")
# 读取用户名密码
user_info={}
with open('user_info.txt','r') as f:
    user_info = json.load(f)
print("你的学号："+user_info['my_username'])
print("即将自动打开Edge浏览器登陆，请勿手动操作。")
sleep(3)

# 启动edge浏览器并访问教务处网站
browser = webdriver.Edge()

url='http://eamis.nankai.edu.cn'
browser.get(url)
sleep(2)
username = browser.find_element_by_id('username')
username.send_keys(user_info['my_username'])
#sleep(0.5)
password = browser.find_element_by_id('password')
password.send_keys(user_info['my_password'])
#sleep(0.5)
submit=browser.find_element_by_name('submitBtn')
submit.click()
sleep(2)

# 进入选课栏
get_gates=browser.find_element_by_xpath("//a[text()='选课']")
get_gates.click()
sleep(1)
electIndexNotices=[]
try:
    for i in range(7):
        electIndexNotices.append(browser.find_element_by_id('electIndexNotice'+str(i)))
except common.exceptions.NoSuchElementException:
    pass
finally:
    gate_num=len(electIndexNotices)
    if gate_num==0:
        print("未找到选课入口。3秒后退出。")
        sleep(3)
        exit()

# 选择选课入口
print("选课入口：\n")
for i in range(gate_num):
    print(str(i)+'. '+electIndexNotices[i].find_element_by_tag_name("h3").text)
    
gate=input("输入一个数字选择选课入口：")
elect_gate=electIndexNotices[int(gate)]

# 转到相应入口
gate_url=elect_gate.find_element_by_xpath("//a[text()='进入选课>>>>']").get_attribute('href')
# 提取最后一串数字，profileId
profileId=re.findall(r'\d+',gate_url)[-1]

browser1 = webdriver.Edge()
browser.get(gate_url)
#其实应该不需要休息1秒
sleep(1)

data_req=request.Request("http://eamis.nankai.edu.cn/eams/stdElectCourse!data.action?profileId="+profileId)
cookie=browser.get_cookies()
JSESSIONID=cookie[0]['value']
data_req.add_header('Cookie','JSESSIONID=%s'%JSESSIONID)
data=''
with request.urlopen(data_req) as f:
    data=f.read().decode('utf-8')
data=json.loads(data[18:].replace("'",'"'))

#匹配课程序号
#m_no=re.compile("no:\'d{4}\'") 
#匹配课程ID
#m_courseIds=re.compile('courseId:\d{5}')


print("课程信息获取完成。请在lessons.txt中键入课程序号并保存。按回车键继续。")
# 读取课程序号
lessons=[]
with open('lessons.txt','r') as file_obj:
    for no in file_obj:
        lessons.append(no.rstrip())

print('你想要选的课是：')
for i in lessons:
    pass
_=input('按回车键开始选课')
