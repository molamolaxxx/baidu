import pymysql
import pandas as pd
import numpy as np
#field字段，topnum为前多少条
def connect_mysql():
    db=pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', passwd = '314', db = 'baidu_db')
    return db
def goodVersion_percent(field,top_num):
    baidu_data=pd.read_csv("/home/molamola/桌面/数据集/百度词条数据集/baidu-item.csv")
    #inplace是否改变原始dataframe,ascending是否升序
    baidu_data.sort_values(field,inplace=True,ascending=False)
    #返回前多少行
    baidu_data_head=baidu_data.head(top_num)['flag']
    baidu_data_head=baidu_data_head.values
    good_count=0
    for item in baidu_data_head:
        if item==1:
            good_count+=1
    percent=good_count/len(baidu_data_head)
    #计算优质比
    return percent

if __name__ == '__main__':
    field=np.array([[0,0,0,0,0,
                    0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0]],dtype=float)
    for _ in range(1,21):
        field[0,_-1]=goodVersion_percent("editor_featuredLemmaCount",_*100)
    #data_f=pd.DataFrame(field)

    data_r=pd.read_csv('/home/molamola/桌面/数据集/百度词条数据集/ana.csv').values
    data_r=np.vstack((data_r,field))
    #data_f=pd.concat((data_r,data_f))
    data_r=pd.DataFrame(data_r)
    print(data_r)
    data_r.to_csv('/home/molamola/桌面/数据集/百度词条数据集/ana.csv',index=False)
