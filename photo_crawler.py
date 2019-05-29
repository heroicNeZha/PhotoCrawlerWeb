import os

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PhotoCrawler():
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cookie': '_T_WM=14825188841; WEIBOCN_FROM=1110006030; SSOLoginState=1556770256; ALF=1559362256; SCF=AmRZxY1EbDDD4h7TWluOWc7g-4BCTEeD-H8fVyepub9Fq5lt2j3OarKuLCbtaE_HsdOU-ezvHUb6BJlXvHOFWLw.; SUB=_2A25xzh2ADeRhGeNO7VES8SvIzD2IHXVTMKPIrDV6PUJbktAKLU7kkW1NTvEERCJg0_HRlAt8hpFBJJs6fe5phgKN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFKEaWiA.PzdUw_8P1Po7Ke5JpX5KzhUgL.Fo-7Soe0eK-XS022dJLoI0YLxK-LBo.LB.eLxK-L1hBLB.qLxK-L1-zLB-BLxK.LB.zL1K2LxKqL1h2LBoqLxK-L122LB.qLxK-L122L1-zt; SUHB=0YhhtaUncrGuDl; MLOGIN=1; XSRF-TOKEN=f8d362; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1078033900510477%26fid%3D1078033900510477_-_photoall%26uicode%3D10000012'
        }

    # 模拟登录
    def login(self):
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(r'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn')
        browser.implicitly_wait(60)
        loginname = browser.find_element_by_id("loginName")
        password = browser.find_element_by_id("loginPassword")
        loginname.click()
        loginname.send_keys('603718938@qq.com')
        password.click()
        password.send_keys('0322Hj')
        loginAction = browser.find_element_by_id("loginAction")
        loginAction.click()
        WebDriverWait(browser, 60 * 10, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf'))
        )
        print(">>登录成功")
        cookies = browser.get_cookies()
        print(">>获取cookie")
        # with open("cookie.json", 'w+') as fp:
        #     fp.write(json.dumps(cookies))
        #     print(">> 本地保存cookie")
        #     fp.close()
        browser.close()
        # 添加cookie
        c = requests.cookies.RequestsCookieJar()
        for i in cookies:
            c.set(i["name"], i["value"])
            self.session.cookies.update(c)

    def getPictures(self, uid):
        try:
            rootpath = os.getcwd() + '/' + uid
            os.makedirs(rootpath)
            print(">>创建用户文件夹")
            # 访问用户照片墙
            for index in range(1, 10):
                filepath = rootpath + '/page_' + str(index)
                os.makedirs(filepath)
                os.chdir(filepath)
                url = r'http://m.weibo.cn/api/container/getSecond?containerid=107803{0}_-_photoall&page={1}&count=30&luicode=10000011&lfid=107803{0}'.format(
                    uid, str(index)
                )
                html_json = self.session.get(url, headers=self.headers).json()
                photoall = html_json['data']['cards']
                for i in range(len(photoall)):
                    pics = photoall[i]['pics']
                    for j in range(len(pics)):
                        pic_down = requests.get(pics[j]['pic_big'])
                        with open(str((i + 1) * (j + 1)) + r'.jpeg', 'ab+') as fp:
                            fp.write(pic_down.content)
                            fp.close()
                print('>>第{0}页写入完成'.format(str(index)))
        except Exception as err:
            print(err)


if __name__ == '__main__':
    uid = input("输入微博用户的uid，为空则默认鹭(3900510477)：\n>> ")
    if uid == '':
        uid = '3900510477'
    photoCrawler = PhotoCrawler()
    photoCrawler.login()
    photoCrawler.getPictures(uid)
