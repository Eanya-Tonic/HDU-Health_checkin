#coding=utf-8
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
# 导入时间模块
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException,ElementNotInteractableException
# 导入随机模块
import random


# 获取驱动路径
# linux
DRIVER_PATH = '/usr/bin/chromedriver'
# 浏览器设置
options = Options()
options.add_argument('--no-sandbox')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=#{linux_useragent}")
options.add_argument("--disable-web-security")
options.add_argument("--disable-xss-auditor")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
# 无头参数
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# serverchan函数
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

# 判断是否有弹出框
def alert_is_present(driver):
    try:
        alert = driver.switch_to.alert
        alert.text
        return alert
    except:
        return False

# 执行打卡
def daka(un,pd,sendkey):
    browser = Chrome(executable_path=DRIVER_PATH, options=options)
    # 访问数字杭电
    browser.get("https://cas.hdu.edu.cn/cas/login")
    # 窗口最大化
    browser.maximize_window()
    # 随机睡眠
    randomSleep = random.randint(8,525)
    time.sleep(randomSleep)
    # 登录账户
    browser.find_element_by_id('un').clear()
    browser.find_element_by_id('un').send_keys(un)# 传送帐号
    browser.find_element_by_id('pd').clear()
    browser.find_element_by_id('pd').send_keys(pd)# 输入密码
    browser.find_element_by_id('index_login_btn').click()
    time.sleep(3)
    try:
        flag=browser.find_element_by_id('errormsg').is_enabled()
    except NoSuchElementException:
        flag=False
    if flag==True:
        print(un+"帐号登录失败")
        serverchan(sendkey, un+"帐号登录失败")
        browser.quit()# 帐号登录失败
    else:
        # 访问打卡界面
        browser.get("https://skl.hduhelp.com/passcard.html#/passcard")
        print("正在执行"+un+"操作")
        time.sleep(10)
        # 注入ua
        browser.execute_cdp_cmd("Emulation.setUserAgentOverride", {"userAgent": "Mozilla/5.0 (Linux; Android 11; Pixel 4 XL Build/RQ3A.210705.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36 AliApp(DingTalk/5.1.5) com.alibaba.android.rimet/13534898 Channel/212200 language/zh-CN UT4Aplus/0.2.25 colorScheme/light"})
        # 重新打开打卡界面
        browser.get("https://skl.hduhelp.com/passcard.html#/punch")
        time.sleep(3)
        # 如果有弹出框 点击确定
        if alert_is_present(browser):
            browser.switch_to.alert.accept()
        # 输入位置信息
        browser.execute_script("window.localStorage.setItem('punch','{\"currentLocation\":\"浙江省杭州市钱塘区\",\"city\":\"杭州市\",\"districtAdcode\":\"330114\",\"province\":\"浙江省\",\"district\":\"钱塘区\",\"healthCode\":0,\"healthReport\":0,\"currentLiving\":0,\"last14days\":0}')")
        # 执行确认打卡
        browser.refresh()
        time.sleep(2)
        # 滚动到底部
        browser.execute_script("window.scrollTo(0,document.body.clientHeight)")
        time.sleep(2)
        browser.find_element_by_xpath('/html/body//form//div[@role="checkbox"]').click()
        submit = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[3]/div/form/div[13]/button')
        if "disabled" in submit.get_attribute('class'):
            browser.execute_script("arguments[0].disabled = false", submit)
            browser.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", submit, 'class', "van-button van-button--primary van-button--normal van-button--block van-button--round")
        submit.click()
        time.sleep(3)
        try:
            browser.find_element_by_css_selector('.text-center.is-success').click()
            print(un+"点击打卡按钮成功")
            serverchan(sendkey,un+"打卡成功！")
        except (NoSuchElementException, ElementNotInteractableException):
            print(un+"打卡时出错")
            serverchan(sendkey, un+"打卡时出错")
            browser.quit()
            return
        time.sleep(3)
        # 退出窗口
        browser.quit()

# 相关参数定义
un=""# 学号
pd=""# 数字杭电密码
# ServerChan发送key，0表示不启用推送
sendkey='0'
daka(un,pd,sendkey)
time.sleep(3)