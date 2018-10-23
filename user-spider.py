import requests
from urllib import request
from bs4 import BeautifulSoup
import json
import numpy as np
user_api_base_url="https://baike.baidu.com/api/usercenter/getusercard?uid="

headers = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/64.0.3282.186 Safari/537.36',
        'Connection': 'keep-alive'
    }
headers_with_cookie={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/68.0.3440.75 Safari/537.36',
        'Connection':'keep-alive',
        'Cookie':'BIDUPSID=908D0DD31368CC3F260711674B9A94A1; PSTM=1532963872; BAIDUID=D839A958D9E30E9CBFE838C7F22245EC:FG=1; BDUSS=BMWU45TTcyLS03QzJoOUVFYlpscGVJZm1HYTFaMWMwLXJFQnV4NWFaY0RLOUZiQUFBQUFBJCQAAAAAAAAAAAEAAACz7V0KanNudHh6eQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOeqVsDnqlbcT; freshGuide=1; BK_SEARCHLOG=%7B%22key%22%3A%5B%22python%22%2C%22%E6%90%9C%E7%8B%97%22%2C%22%E4%BF%A1%E7%94%A8%E8%AF%84%E7%BA%A7%22%5D%7D; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1539564314,1539564324,1539582754,1539584692; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1539585323; delPer=0; PSINO=3; H_PS_PSSID=26523_1467_21092_26350_20927'
    }
def get_cookie_content():
    f = open(r'cookie.txt', 'r')  # 打开所保存的cookies内容文件
    cookies = {}  # 初始化cookies字典变量
    for line in f.read().split(';'):  # 按照字符：进行划分读取
        # 其设置为1就会把字符串拆分成2份
        name, value = line.strip().split('=', 1)
        cookies[name] = value  # 为字典cookies添加内容
    print(cookies)
def get_page_url(lemmaId,page):
    return 'https://baike.baidu.com/api/wikiui/gethistorylist?tk=4ea302be758a18c41a5f86c58b60109b&lemmaId='+str(lemmaId)+'&from='+str(page)+'&count=1&size=25'
#获得用户id群
def get_uid_list(lemmaId,page):
    #获得历史页面soup
    url=get_page_url(lemmaId,page)
    print(url)
    editor_request=request.Request(url,headers=headers_with_cookie)
    editor_response=request.urlopen(editor_request)
    editor_page=editor_response.read()
    editor_soup = BeautifulSoup(editor_page, "html.parser").text
    editor_json=json.loads(editor_soup)
    editor_json=editor_json['data']['pages'][str(page)]
    #获得name
    #uid_list=editor_soup.select('a.uname')
    #编辑者总数
    editor_total_num=len(editor_json)
    # 编辑者属性(总值)
    editor_goodVersionCount = 0
    editor_commitPassedCount = 0
    editor_level = 0
    editor_featuredLemmaCount = 0
    editor_createPassedCount = 0
    editor_commitTotalCount = 0
    editor_experience = 0
    editor_passRatio = 0
    for each in editor_json:
        uid=each['uid']
        print(uid)
        info=get_json(uid)
        editor_goodVersionCount+=float(info['goodVersionCount'])
        editor_commitPassedCount += float(info['commitPassedCount'])
        editor_level += float(info['level'])
        editor_featuredLemmaCount += float(info['featuredLemmaCount'])
        editor_createPassedCount += float(info['createPassedCount'])
        editor_commitTotalCount += float(info['commitTotalCount'])
        editor_experience += float(info['experience'])
        editor_passRatio += float(info['passRatio'])
    #info数组
    info=np.array([editor_goodVersionCount,editor_commitPassedCount,editor_level,editor_featuredLemmaCount,editor_createPassedCount,
          editor_commitTotalCount,editor_experience,editor_passRatio])
    #平均值
    average_info=np.divide(info,editor_total_num)
    return average_info
    print(average_info[7])
def get_json(uid):
    info_request = request.Request(user_api_base_url+str(uid), headers=headers)
    info_response = request.urlopen(info_request)
    info_page = info_response.read()
    info_json = BeautifulSoup(info_page, "html.parser").text
    info_json_obj = json.loads(info_json)
    #一条编辑者数据
    info=info_json_obj['data']
    return info
if __name__ == '__main__':

    #print(get_json(14553))
    #计算编辑者平均属性
    each_info=get_uid_list(234922,1)
    print(each_info)

