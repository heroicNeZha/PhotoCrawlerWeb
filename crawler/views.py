import json
import re
from django.shortcuts import render, redirect

# Create your views here.
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def index(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        with open("static/cookie.json", encoding='utf-8') as f:
            cookie = json.load(f)
            f.close()
        cookie = cookie['cookie']
        sess = requests.session()
        c = requests.cookies.RequestsCookieJar()
        for i in cookie:  # 添加cookie到CookieJar
            c.set(i["name"], i["value"])
            sess.cookies.update(c)
        headers = {
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'cookie': '_T_WM=14825188841; WEIBOCN_FROM=1110006030; SSOLoginState=1556770256; ALF=1559362256; SCF=AmRZxY1EbDDD4h7TWluOWc7g-4BCTEeD-H8fVyepub9Fq5lt2j3OarKuLCbtaE_HsdOU-ezvHUb6BJlXvHOFWLw.; SUB=_2A25xzh2ADeRhGeNO7VES8SvIzD2IHXVTMKPIrDV6PUJbktAKLU7kkW1NTvEERCJg0_HRlAt8hpFBJJs6fe5phgKN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFKEaWiA.PzdUw_8P1Po7Ke5JpX5KzhUgL.Fo-7Soe0eK-XS022dJLoI0YLxK-LBo.LB.eLxK-L1hBLB.qLxK-L1-zLB-BLxK.LB.zL1K2LxKqL1h2LBoqLxK-L122LB.qLxK-L122L1-zt; SUHB=0YhhtaUncrGuDl; MLOGIN=1; XSRF-TOKEN=f8d362; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1078033900510477%26fid%3D1078033900510477_-_photoall%26uicode%3D10000012'
        }
        url = r"http://m.weibo.cn/api/container/getIndex?containerid=100103type%3D3%26q%3D{0}%26t%3D0&page_type=searchall".format(
            keyword)
        html_json = sess.get(url, headers=headers).json()
        card_group = html_json['data']['cards'][1]['card_group']
        users = []
        for card in card_group:
            try:
                user = {}
                user['uid'] = card['user']['id']
                user['name'] = card['user']['screen_name']
                user['cover'] = card['user']['profile_image_url']
                user['desc'] = card['desc1'] + " | " + card['desc2']
                users.append(user)
            except Exception as e:
                print(e)
        print(users)
        return render(request, "search.html", {'users': users, 'keyword': keyword})
    return render(request, "index.html")


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        browser = webdriver.Chrome()
        browser.maximize_window()
        browser.get(r'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn')
        browser.implicitly_wait(60)
        loginname = browser.find_element_by_id("loginName")
        password = browser.find_element_by_id("loginPassword")
        loginname.click()
        loginname.send_keys(username)
        password.click()
        password.send_keys(pwd)
        loginAction = browser.find_element_by_id("loginAction")
        loginAction.click()
        WebDriverWait(browser, 60 * 10, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'lite-iconf'))
        )
        print("登陆成功")
        cookies = browser.get_cookies()
        with open("static/cookie.json", 'w+') as fp:
            fp.write(json.dumps({"cookie": cookies}))
            print(">> 本地保存cookies")
            fp.close()
        browser.close()
        return redirect('crawler:index')
    return render(request, "login.html")


def user(request, uid):
    with open("static/cookie.json", encoding='utf-8') as f:
        cookie = json.load(f)
        f.close()
    cookie = cookie['cookie']
    sess = requests.session()
    c = requests.cookies.RequestsCookieJar()
    for i in cookie:  # 添加cookie到CookieJar
        c.set(i["name"], i["value"])
        sess.cookies.update(c)
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'cookie': '_T_WM=14825188841; WEIBOCN_FROM=1110006030; SSOLoginState=1556770256; ALF=1559362256; SCF=AmRZxY1EbDDD4h7TWluOWc7g-4BCTEeD-H8fVyepub9Fq5lt2j3OarKuLCbtaE_HsdOU-ezvHUb6BJlXvHOFWLw.; SUB=_2A25xzh2ADeRhGeNO7VES8SvIzD2IHXVTMKPIrDV6PUJbktAKLU7kkW1NTvEERCJg0_HRlAt8hpFBJJs6fe5phgKN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFKEaWiA.PzdUw_8P1Po7Ke5JpX5KzhUgL.Fo-7Soe0eK-XS022dJLoI0YLxK-LBo.LB.eLxK-L1hBLB.qLxK-L1-zLB-BLxK.LB.zL1K2LxKqL1h2LBoqLxK-L122LB.qLxK-L122L1-zt; SUHB=0YhhtaUncrGuDl; MLOGIN=1; XSRF-TOKEN=f8d362; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1078033900510477%26fid%3D1078033900510477_-_photoall%26uicode%3D10000012'
    }
    url = r'http://m.weibo.cn/api/container/getSecond?containerid=107803{0}_-_photoall&page={1}&count=30&luicode=10000011&lfid=107803{0}'.format(
        uid, str(index))
    html_json = sess.get(url, headers=headers).json()
    cards = html_json['data']['cards']
    return render(request, 'user.html', {'cards': cards})
