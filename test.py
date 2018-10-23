from urllib import request
import requests
import numpy as np
import baidu.spider as sp
import baidu.run as sp_run
base_url="http://baike.baidu.com/view/"
headers = {
    'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/64.0.3282.186 Safari/537.36',
    'Connection': 'keep-alive'
}
if __name__ == '__main__':
    for _ in range(10000):
        sp_run.run_spider(0,10000)
