from urllib import request
import requests
import numpy as np
import baidu.spider as sp
import baidu.saver as saver
base_url="http://baike.baidu.com/view/"
headers = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/64.0.3282.186 Safari/537.36',
        'Connection': 'keep-alive'
    }
def run_one_page(page_id):
    url = base_url + str(page_id) + ".htm"
    try:
        my_request = request.Request(url, headers=headers)
        my_response = request.urlopen(my_request)
    except:
        print("页面出错！")
    else:
        print(url)
        saver.save_one_item(saver.connect_mysql(),sp.get_one_page(url, page_id))
def run_spider(low,high):
    page_id = int(np.random.uniform(low, high))
    run_one_page(page_id)
