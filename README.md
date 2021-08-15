# HDU-Health_checkin
基于Legroft大佬的脚本编写的自动健康打卡脚本
原仓库链接https://github.com/Legroft/HDU-DailyHealthy
详细使用说明可参考原仓库

原代码采用的是获取token的方式，但是我实地测试了一下发现获取token比较麻烦，而且现在打卡界面貌似又进行了改版，所以改成了直接登录的形式

**请注意：帐号密码均以明文储存于代码中，本代码仅供参考使用，切勿随意传播导致自己的帐号和密码泄露**
具体使用如下
```python3
un="000"
##用来确定数字杭电的学号

pd="×××"
##“×××”处代表了数字杭电的密码
```

由于健康打卡取消了手动选择地理位置的功能，故改成了虚拟定位的形式，可以更改以下代码修改具体定位
```python3
#设置模拟位置数据：杭州市钱塘区120.350228,30.324128，更多位置查询：http://api.map.baidu.com/lbsapi/getpoint/
params = {
    "latitude": 30.324128,
    "longitude": 120.350228,
    "accuracy": 100
}
```
代码运行依赖
```
chrome
chromedrive
selenium
```
具体安装方式可以自行搜索

另外，原代码使用qmsg进行推送，我改为了使用serverchan推送，大体并无区别，serverchan的具体使用方法也可以自行上网查询
