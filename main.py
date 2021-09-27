import requests
import os
import sys
import time
import json
import pandas as pd
from selenium import webdriver
from retrying import retry
from hashlib import md5

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
url1 = ' https://wxyqfk.zhxy.net/?yxdm=10623#/login'
url2 = 'https://wxyqfk.zhxy.net/?yxdm=10623#/clockIn'


def login():
    global data_login
    data_login = {
        "Name": stu_name,
        "PassWord": stu_sign_password,
        "UserType": "1",
        "XGH": stu_xgh,
        "YXDM": "10623"
    }
    login_url = "https://wxyqfk.zhxy.net/?yxdm=10623#/login"
    # 登陆
    s = requests.Session()
    s.post(login_url, data=data_login, headers=headers)
    # post登陆页面
    login_result = s.post("https://yqfkapi.zhxy.net/api/User/CheckUser")
    print(login_result)
    return s


# 成功发邮箱提醒
def email_send_right(stu_xgh, to_addr):
    # smtplib 用于邮件的发信动作
    import smtplib
    from email.mime.text import MIMEText
    import datetime

    # email 用于构建邮件内容
    from email.header import Header

    # 用于构建邮件头

    email = '感谢使用青柠疫服自动打卡系统，你的账号【{0}】已经成功打卡！'.format(stu_xgh)

    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'xxx'
    password = 'xxx'

    # 收信方邮箱


    # 发信服务器
    smtp_server = 'smtp.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(email, 'plain', 'utf-8')

    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(str(datetime.date.today()) + '青柠打卡结果反馈')

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    # 发送完成反馈
    print("邮箱发送成功")


# 错误发邮箱提醒
# 发邮箱提醒
def email_send_wrong(stu_xgh, to_addr):
    # smtplib 用于邮件的发信动作
    import smtplib
    from email.mime.text import MIMEText
    import datetime

    # email 用于构建邮件内容
    from email.header import Header

    # 用于构建邮件头

    email = '感谢使用青柠疫服自动打卡系统，你的账号【{0}】打卡失败了请手动打卡！'.format(stu_xgh)

    # 发信方的信息：发信邮箱，QQ 邮箱授权码
    from_addr = 'xxxxx'
    password = 'xxxxx'

    # 收信方邮箱
    to_addr = 'xxxxxx'

    # 发信服务器
    smtp_server = 'smtp.qq.com'

    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
    msg = MIMEText(email, 'plain', 'utf-8')

    # 邮件头信息
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(str(datetime.date.today()) + '青柠打卡结果反馈')

    # 开启发信服务，这里使用的是加密传输
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    # 发送完成反馈
    print("邮箱发送成功")


# 图像识别接口一 http://www.fateadm.com/
def get_qrcode():
    pic1 = requests.get('https://yqfkapi.zhxy.net/api/common/getverifycode')
    tex1 = pic1.content
    tex2 = bytes.decode(tex1)
    if json.loads(tex2)['info'] == '非法访问！':
        print(tex2)
        sys.exit(1)
    tex3 = json.loads(tex2)['data']['img']
    key = json.loads(tex2)['data']['key']
    url = 'data:image/png;base64,' + tex3
    # print(url)
    # print(qr_key)
    # 1.识别验证码
    img_url = url
    from get_code import TestFunc
    from urllib.request import urlretrieve
    urlretrieve(img_url, 'qrcode_temp.png')
    code = TestFunc()
    # code="1234"
    print(code)
    print("调用了1接口（斐斐打码接口）")
    return key, code


# 图鉴识别接口2 http://www.ttshitu.com/
def get_qrcode2():
    pic1 = requests.get('https://yqfkapi.zhxy.net/api/common/getverifycode')
    tex1 = pic1.content
    tex2 = bytes.decode(tex1)
    if json.loads(tex2)['info'] == '非法访问！':
        print(tex2)
        sys.exit(1)
    tex3 = json.loads(tex2)['data']['img']
    key = json.loads(tex2)['data']['key']
    url = 'data:image/png;base64,' + tex3
    # print(url)
    # print(qr_key)
    # 1.识别验证码
    img_url = url
    from tujian import base64_api
    from urllib.request import urlretrieve
    urlretrieve(img_url, 'qrcode_temp.png')
    time.sleep(2)
    code = base64_api()
    # code="1234"
    print("调用了2接口（图鉴接口）")
    return key, code


# ddddocr接口
@retry(stop_max_delay=3)
def new_ocr():
    pic1 = requests.get('https://yqfkapi.zhxy.net/api/common/getverifycode')
    tex1 = pic1.content
    tex2 = bytes.decode(tex1)
    if json.loads(tex2)['info'] == '非法访问！':
        print(tex2)
        sys.exit(1)
    tex3 = json.loads(tex2)['data']['img']
    key = json.loads(tex2)['data']['key']
    url = 'data:image/png;base64,' + tex3
    # print(url)
    # print(qr_key)
    # 1.识别验证码
    img_url = url
    from ddddocr_NB import free
    from urllib.request import urlretrieve
    urlretrieve(img_url, 'qrcode_temp.png')
    filepath = "qrcode_temp.png"
    code = free(filepath)
    # code="1234"
    print(code)
    print("调用了免费接口（ddddocr接口）")
    return key, code


# 创建日志，清除日志内容
def recoding_clean():
    with open("recoding.txt", 'w+') as f:
        f.read()
    with open("recoding.txt", 'r+') as f:
        f.seek(0)
        f.truncate()  # 清空文件


# 运行成功写入1,
def recoding_ture():
    with open("recoding.txt", 'a+') as f:
        state = "1,"
        f.write(state)


# 运行失败写入0,
def recoding_false():
    with open("recoding.txt", 'a+') as f:
        state = "0,"
        f.write(state)


# post数据部分
def health_daka(s, key, code):
    data_health = {
        "UID": stu_uid,
        "UserType": "1",
        "JWD": JWD,
        "key": key,
        "code": code,
        "ZZDKID": "37",
        "A1": "正常",
        "A4": "无",
        "A2": "全部正常",
        "A3": Place,
        "A11": "在校",
        "A12": "未实习",
        "A13": "低风险区",
        "YXDM": "10623",
        "version": "v1.3.2"
    }

    # for i in range(2):
    health_url = 'https://wxyqfk.zhxy.net/?yxdm=10623#/clockIn'
    s.post(health_url, headers=headers)
    health_result = s.post('https://yqfkapi.zhxy.net/api/ClockIn/Save', data=data_health, headers=headers)


# 浏览器操作部分
def webdriver_holdon():
    path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-software-rasterizer')
    # options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.get("https://wxyqfk.zhxy.net/?yxdm=10623#/login")
    time.sleep(2)
    XGH = driver.find_elements_by_class_name('van-field__body')[0].find_element_by_tag_name('input')
    XGH.send_keys(data_login['XGH'])
    Name = driver.find_elements_by_class_name('van-field__body')[1].find_element_by_tag_name('input')
    Name.send_keys(data_login['Name'])
    Password = driver.find_elements_by_class_name('van-field__body')[3].find_element_by_tag_name('input')
    Password.send_keys(data_login['PassWord'])
    time.sleep(1)
    login_button = driver.find_element_by_class_name('sign-in-btn')
    login_button.click()
    time.sleep(2)
    driver.get("https://wxyqfk.zhxy.net/?yxdm=10623#/clockIn")
    time.sleep(1)
    return driver

'''获取uid'''
def uid():
    formdata = {
        "YXDM": "10623",
        "UserType": "1",
        "XGH": stu_xgh,
        "Name": stu_name,
        "PassWord": stu_password
    }
    url = "https://yqfkapi.zhxy.net/api/User/CheckUser"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    response = requests.post(url, data=formdata, headers=headers)
    # 使用json()方法，将response对象，转为列表/字典
    json_response = response.json()
    # print(json_response)
    # 获取UID
    UID = json_response['data']['ID']
    # print(UID)
    stu_uid = str(UID)
    return stu_uid


# 创建日志，清除日志内容
def recoding_clean():
    with open("recoding.txt", 'w+') as f:
        f.read()
    with open("recoding.txt", 'r+') as f:
        f.seek(0)
        f.truncate()  # 清空文件


# 运行成功写入1,
def recoding_ture():
    with open("recoding.txt", 'a+') as f:
        state = "1,"
        f.write(state)


# 运行失败写入0,
def recoding_false():
    with open("recoding.txt", 'a+') as f:
        state = "0,"
        f.write(state)

def all_data():
    # 1.连接
    import pymysql
    import pandas as pd
    conn = pymysql.connect(host='localhost', user='xxxx', password='xxxx', db='xxx')
    sql_query = 'SELECT * FROM user'
    table = pd.read_sql(sql_query, con=conn)
    conn.close()
    # print(df)
    return table

if __name__ == '__main__':
    position = 0
    recoding_clean()
    lis = []
    # table=pd.read_excel("data.xls")
    # path = r"C:\Users\Administrator\Desktop\Robot B\BOT3559802084-20733\nb2\gzh.csv"
    #path ="gzh.csv"
    # table = pd.read_csv(path)
    # print(table)
    table=all_data()
    for i in range(table.shape[0]):
        data = table.loc[i]
        lis.append(dict(data))
    for i in lis:
        try:

            a = "fall"
            #姓名
            stu_name = str(i['stu_name'])
            #学号
            stu_xgh = str(i['stu_num'])
            #密码
            password=str(i['password'])
            stu_password = md5(password.encode('utf8')).hexdigest()

            # JWD = str(i['JWD'])
            JWD = str("30.77826,103.95662")
            Place = str("中国四川省成都市西华大学")
            to_addr = str(i['email'])
            # phone = str(int(i['phone']))

            stu_uid = uid()
            if stu_uid:
                print("查询成功")
                stu_sign_password = str(i['password'])  # 登录密码
                # print(stu_name, stu_password, stu_xgh, stu_uid, JWD, Place)
                s = login()
                driver = webdriver_holdon()
                # 检测是否打卡
                try:
                    # time.sleep(2)
                    if driver.find_element_by_class_name('already-title'):
                        print(stu_name + "今天已打卡")
                        driver.close()
                        a = "success"
                        email_send_right(stu_xgh, to_addr)
                    else:
                        time.sleep(1)
                        driver.refresh()
                        driver.find_element_by_class_name("already-title")
                        print(stu_xgh + "今天已打卡")
                        driver.close()
                        a = "success"
                        # email_send_right(stu_xgh, to_addr)
                except:
                    try:
                        # 试着调用新的ocr接口如果出错还是用原来的
                        key, code = new_ocr()
                        time.sleep(1)
                        if len(code) == 4 and code.isalnum():
                            health_daka(s, key, code)
                            a = "success"
                            driver.refresh()
                            if driver.find_element_by_class_name('already-title'):
                                print(stu_name + "今天已打卡")
                                email_send_right(stu_xgh, to_addr)
                                driver.close()
                            else:
                                continue
                        else:
                            key, code = new_ocr()
                            time.sleep(1)
                            if len(code) == 4 and code.isalnum():
                                health_daka(s, key, code)
                                a = "success"
                                driver.refresh()
                                if driver.find_element_by_class_name('already-title'):
                                    print(stu_name + "今天已打卡")
                                    email_send_right(stu_xgh, to_addr)
                                    driver.close()
                                else:
                                    continue
                    except:
                        key, code = new_ocr()
                        time.sleep(2)
                        health_daka(s, key, code)
                        if len(code) == 4 and code.isalnum():
                            a = "success"
                            email_send_right(stu_xgh, to_addr)
                        else:
                            a = 'wrong'
                            email_send_wrong(stu_xgh, to_addr)
                        driver.close()
            else:
                print("密码错误")
                break

        except:
            print("密码或者邮箱错误")


        time.sleep(3)
        # 记录日志
        if a == "success":
            print(stu_name + "打卡成功")
            recoding_ture()
        else:
            print(stu_name + "打卡失败")
            recoding_false()
