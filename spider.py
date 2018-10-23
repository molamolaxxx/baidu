from bs4 import BeautifulSoup
from urllib import request
import requests
import re
import numpy as np
import json
from baidu.editorsp import get_uid_list
from baidu.item import B_item

BAIDU_BAIKE_URL="https://baike.baidu.com"

html_doc = """
https://baike.baidu.com
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
def get_img_num(img_url):
    headers = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/64.0.3282.186 Safari/537.36',
        'Connection': 'keep-alive'
    }
    my_request = request.Request(img_url, headers=headers)
    my_response = request.urlopen(my_request)
    pic_html = my_response.read()
    pic_soup=BeautifulSoup(pic_html,"html.parser")
    pic_num=pic_soup.select('span.number')[0]
    pic_num_total=pic_num.select('span')
    return pic_num_total[1].text
    '''except:
        print("图片出错！")
    else:
        print(pic_html)'''
def get_lammapv_url(id):
    lammapv_url="https://baike.baidu.com/api/lemmapv?id="+id+"&r=0.9994191620892552"
    return lammapv_url
#获得引号内内容
def get_deep_txt(txt):
    index_first=txt.find('"')
    txt_sub=txt[index_first+1:index_first+40]
    index_last=txt_sub.find('"')
    id=txt_sub[0:index_last]
    return id
def get_lemmaPv_id(java_script):
    for txt in java_script:
        index=txt.text.find('newLemmaIdEnc')
        if (index != -1):
            txt_sub = txt.text[index:index + 60]
            return get_deep_txt(txt_sub)

def get_lemmaId(java_script):
    for txt in java_script:
        index=txt.text.find('rightCheck.editView')
        if(index!=-1):
            txt_sub=txt.text[index+15:index+30]
            lemma_id=re.sub("\D", "", txt_sub)
        index2 = txt.text.find('newLemmaIdEnc')
        if (index2 != -1):
            txt_sub = txt.text[index2:index2 + 60]
            pv_id= get_deep_txt(txt_sub)
    return lemma_id,pv_id
def get_share_counter_url(lemmaId):
    share_counter_url = "https://baike.baidu.com/api/wikiui/sharecounter?lemmaId="+str(lemmaId)+"&method=get"
    return share_counter_url
def get_word_nums(text):
    num = 0
    for i in text:
        if i not in ' \n!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~':
            num = num +1
    return num
def remove_brackets(str):
    a=str.replace('（','').replace('）','')
    return a
def remove_reference(str):
    a=str.replace(' ','')
    return a
#获得一页的信息
def get_one_page(url,id):
    headers = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/64.0.3282.186 Safari/537.36',
        'Connection': 'keep-alive'
    }
    #获得词条对象
    baidu_item=B_item()
    my_request = request.Request(url,headers=headers)
    my_response=request.urlopen(my_request)
    html_doc=my_response.read()

    soup = BeautifulSoup(html_doc,"html.parser")
    #错误页
    count_down=soup.select('.countdown')
    if len(count_down)!=0:
        print("找不到页面!")
        return baidu_item
    #id,int
    baidu_item.id=id
    print("id:"+str(baidu_item.id))
    # 爬取大标题
    title_content=soup.select('.lemmaWgt-lemmaTitle-title')
    #para
    main_title=title_content[0].select('h1')[0].string
    baidu_item.title=main_title
    print("标题:"+str(baidu_item.title))
    #获取摘要字数
    try:
        summary_root=soup.select('div.lemma-summary')
        summary=summary_root[0].text
    except:
        baidu_item.abstract=0
        print("抓取摘要失败")
    else:
        baidu_item.abstract=get_word_nums(summary)
        print("摘要字数："+str(baidu_item.abstract))
    #获取正文字数
    try:
        content_root=soup.select('div.main-content')
        content=content_root[0].select('div.para')
        num=0
        for txt in content:
            num+=get_word_nums(txt.text)
    except:
        baidu_item.content=0
        print("正文抓取失败")
    else:
        baidu_item.content=num
        print("正文字数:" + str(num))
    #二级标题个数
    try:
        second_title=soup.select('h2.title-text')
        second_title_num=len(second_title)
    except:
        baidu_item.s_content=0
        print("抓取二级标题失败")
    else:
        baidu_item.s_content=second_title_num
        print("二级标题数:"+str(second_title_num))
    #三级标题个数
    try:
        third_title=soup.select('h3.title-text')
        third_title_num=len(third_title)
    except:
        baidu_item.t_content=0
        print("抓取三级标题失败")
    else:
        baidu_item.t_content=third_title_num
        print("三级标题数:"+str(third_title_num))
    #图片数
    try:
        img_div=soup.select('div.summary-pic')[0]
        img_a=img_div.select('a')[0]
        href=BAIDU_BAIKE_URL+str(img_a['href'])
        #深度爬取
        num=get_img_num(href)
    except:
    #出现异常
        baidu_item.img=0
        print("图片数:0")
    else:
        baidu_item.img=num
        print("图片数:"+num)
    #最近更新时间
    recent_time=soup.select('span.j-modified-time')
    if len(recent_time)!=0:
        recent_time=soup.select('span.j-modified-time')[0].string
        recent_time=remove_brackets(recent_time)
        baidu_item.last_time=recent_time
        print("最近更新时间："+str(recent_time))
    else:
        baidu_item.last_time='None'
        print("没有更新时间")
    #参考数
    reference_list=soup.select('.reference-list')
    if len(reference_list)!=0:
        reference_list=soup.select('.reference-list')[0]
        reference=reference_list.find_all('li')
        baidu_item.ref=len(reference)
        print("参考数:" + str(baidu_item.ref))
    else:
        baidu_item.ref=0
        print("参考数:0")

    # 通过分析js文件
    try:
        java_script = soup.select('script')
        lammaId,id = get_lemmaId(java_script)
        baidu_item.lemmaId=lammaId
        print("lemmaId:"+str(lammaId))
        share_counter_url=get_share_counter_url(lammaId)


        lammapv_url = get_lammapv_url(id)

        _request = request.Request(share_counter_url, headers=headers)
        _response = request.urlopen(_request)

        _request2 = request.Request(lammapv_url, headers=headers)
        _response2 = request.urlopen(_request2)
        #获得json数据
        share_json = _response.read()
        share_json = BeautifulSoup(share_json, "html.parser").text
        share_json_obj=json.loads(share_json)

        pv_json=_response2.read()
        pv_json = BeautifulSoup(pv_json, "html.parser").text
        pv_json_obj = json.loads(pv_json)
    except:
        print("获取用户数据失败")
        baidu_item.click=0
        baidu_item.share=0
        baidu_item.good=0
        print("丢弃数据")
        return baidu_item
    #点击数
    else:
        baidu_item.click=pv_json_obj['pv']

        # 分享数
        baidu_item.share=share_json_obj['shareCount']

        # 点赞数
        baidu_item.good=share_json_obj['likeCount']

    print("点击数:" + str(baidu_item.click))
    print("分享数:" + str(baidu_item.share))
    print("点赞数:" + str(baidu_item.good))
    #编辑次数
    try:
        edit_count_root=soup.select('dd.description')
        edit_count=edit_count_root[0].select('ul')[0].select('li')[1].text
        edit_count=edit_count.replace('次历史版本','')
    except:
        baidu_item.edit_time=0
        print("编辑次数：0")
    else:
        baidu_item.edit_time=re.sub("\D", "", edit_count)
        print("编辑次数："+str(baidu_item.edit_time))
    #标签数
    tag_count=soup.select('#open-tag-item')
    if len(tag_count)!=0:
        tag_count=soup.select('#open-tag-item')[0].select('span')
        baidu_item.tag=len(tag_count)
        print("标签数:"+str(baidu_item.tag))
    else:
        baidu_item.tag=0
        print("标签数:0")
    #义项数
    try:
        item_num=soup.select('div.polysemantList-header-title')[0].select('a')
    except:
        baidu_item.items=1
        print("义项数:1")
    else:
        item_num=item_num[2].text
        baidu_item.items=re.sub("\D", "", item_num)
        print("义项数:"+baidu_item.items)
    #是否是特色词条
    try:
        flag=soup.select('.posterFlag')[0]
    except:
        baidu_item.flag=0
    else:
        flag=flag['title'][0:1]
        if flag=='特':
            #print("特色词条")
            baidu_item.flag=1
        elif flag=='专':
            #print("专家词条")
            baidu_item.flag=2
        else:
            baidu_item.flag=0
    print(baidu_item.flag)
    #编辑者属性
    #编辑者信息
    try:
        editor_info_list = get_uid_list(lammaId, 1)
    except:
        print("获取编辑者页面失败")
        return baidu_item
    baidu_item.editor_goodVersionCount=editor_info_list[0]
    print("平均好版本数:"+str(baidu_item.editor_goodVersionCount))
    #
    baidu_item.editor_commitPassedCount = editor_info_list[1]
    print("平均通过版本数:" + str(baidu_item.editor_commitPassedCount))
    #
    baidu_item.editor_level = editor_info_list[2]
    print("平均等级:" + str(baidu_item.editor_level))
    #
    baidu_item.editor_featuredLemmaCount = editor_info_list[3]
    print("featuredLemmaCount:" + str(baidu_item.editor_featuredLemmaCount))
    #
    baidu_item.editor_createPassedCount = editor_info_list[4]
    print("平均创建词条通过数:" + str(baidu_item.editor_createPassedCount))
    #
    baidu_item.editor_commitTotalCount = editor_info_list[5]
    print("平均总提交数:" + str(baidu_item.editor_commitTotalCount))
    #
    baidu_item.editor_experience = editor_info_list[6]
    print("平均经验:" + str(baidu_item.editor_experience))
    #
    baidu_item.editor_passRatio = editor_info_list[7]
    print("平均通过率:" + str(baidu_item.editor_passRatio))
    #返回条目
    baidu_item.is_available=True
    return baidu_item
if __name__ == '__main__':
    #url="https://baike.baidu.com/item/Python/407313?fr=aladdin"
    # 获得html
    base_url="http://baike.baidu.com/view/"
    headers = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/64.0.3282.186 Safari/537.36',
        'Connection': 'keep-alive'
    }
    for i in range(5000):
        page_id = int(np.random.uniform(0, 10000))
        url = base_url + str(page_id) + ".htm"
        try:
            my_request = request.Request(url, headers=headers)
            my_response = request.urlopen(my_request)
        except:
            print("页面出错！")
        else:
            print(url)
            get_one_page(url,page_id)



