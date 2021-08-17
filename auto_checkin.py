from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
# 导入时间模块
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,ElementNotInteractableException


# 获取驱动路径
# linux
DRIVER_PATH = './chromedriver'
# 浏览器设置
options = Options()
options.add_argument('--no-sandbox')
# 无头参数
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#设置模拟位置数据：杭州市钱塘区120.350228,30.324128，更多位置查询：http://api.map.baidu.com/lbsapi/getpoint/
params = {
    "latitude": 30.324128,
    "longitude": 120.350228,
    "accuracy": 100
}

#serverchan函数
def serverchan(sendkey, msg):
    if sendkey=='0':
        pass
    else:
        browser = Chrome(executable_path=DRIVER_PATH, options=options)
        # serverchan消息推送 https://sctapi.ftqq.com/****************.send?title=messagetitle
        url = "https://sctapi.ftqq.com/" + str(sendkey)+".send?title="+str(msg)
        browser.get(url)
        time.sleep(3)
        # 退出窗口
        browser.quit()



def daka(un,pd,sendkey):
    browser = Chrome(executable_path=DRIVER_PATH, options=options)
    browser.execute_cdp_cmd("Emulation.setGeolocationOverride", params)
    #避免爬虫被检测
    script='''Object.defineProperties(navigator, {webdriver:{get:()=>undefined}})'''
    browser.execute_script(script)
    # 访问数字杭电
    browser.get("https://cas.hdu.edu.cn/cas/login")
    # 窗口最大化
    browser.maximize_window()
    time.sleep(2)
    #登录账户
    browser.find_element_by_id('un').clear()
    browser.find_element_by_id('un').send_keys(un)#传送帐号
    browser.find_element_by_id('pd').clear()
    browser.find_element_by_id('pd').send_keys(pd)#输入密码
    browser.find_element_by_id('index_login_btn').click()
    time.sleep(3)
    try:
        flag=browser.find_element_by_id('errormsg').is_enabled()
    except NoSuchElementException:
        flag=False
    if flag==True:
        print(un+"帐号登录失败")
        serverchan(sendkey, "帐号登录失败")
        browser.quit()#帐号登录失败
    else:
        #访问打卡界面
        browser.get("https://healthcheckin.hduhelp.com/")
        print("正在执行"+un+"操作")
        time.sleep(3)
        #注入ua
        browser.execute_cdp_cmd("Emulation.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Linux Android 8.0.0 MIX 2 Build/OPR1.170623.027 wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36 yiban_android"})
        #重新打开打卡界面
        browser.get("https://healthcheckin.hduhelp.com/")
        time.sleep(3)
        # 点击 确认打卡 按钮
        print("正在点击确认抗疫答题按钮")
        try:
            browser.find_element_by_css_selector('.van-hairline--top.van-dialog__footer').click()
            print("点击确认抗疫答题按钮成功")
        except NoSuchElementException:
            pass
        print("正在点击确认打卡按钮")
        if browser.find_element_by_css_selector('.van-button.van-button--info.van-button--normal').is_enabled()==False:
            print(un+"今日已打卡")
            serverchan(sendkey, "今日已打卡！")
            browser.quit()
        else:
            browser.find_element_by_css_selector('.van-button.van-button--info.van-button--normal').click()
            print("点击确认打卡按钮成功")
            time.sleep(8)
            # 点击弹出的 确认 按钮
            try:
                print("正在点击确认按钮")
                browser.find_element_by_class_name('van-dialog__confirm').click()
                print("点击确认按钮成功")
                serverchan(sendkey,"打卡成功！")
            except (NoSuchElementException, ElementNotInteractableException):
                print(un+"授权地理位置时出错")
                serverchan(sendkey, "授权地理位置时出错")
                browser.quit()
                return
            # 退出窗口
            browser.quit()

#相关参数定义
un="000"#学号
pd="***"#数字杭电密码
#ServerChan发送key，0表示不启用推送
sendkey='0'
daka(un,pd,sendkey)
time.sleep(3)
