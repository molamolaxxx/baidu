import pymysql
import numpy as np
def connect_mysql():
    db=pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', passwd = '314', db = 'baidu_db')
    return db
def save_one_item(database,item):
    baidu_item=np.array([item.id,item.title,item.abstract,item.content,item.s_content,item.t_content
                ,item.img,item.last_time,item.ref,item.click
                ,item.share,item.good,item.edit_time,item.tag,item.items
                ,item.lemmaId
                ,item.editor_goodVersionCount,
                item.editor_commitPassedCount,
                item.editor_level,
                item.editor_featuredLemmaCount,
                item.editor_createPassedCount,
                item.editor_commitTotalCount,
                item.editor_experience,
                item.editor_passRatio,
                #输出
                item.flag])
    print(len(baidu_item))
    #如果可以存,存入数据库
    if item.is_available==True:
        #存
        print("存储到mysql")
        #创建游标
        cursor=database.cursor(cursor = pymysql.cursors.DictCursor)
        sql = "insert into baidu(id,title,abstract,content,s_content,t_content,img" \
              ",lasttime,ref,click"+\
                ",share,good,edittime,tag,items"+\
                ",lemmaID,editor_goodVersionCount,"+\
                "editor_commitPassedCount,"+\
                "editor_level,"+\
                "editor_featuredLemmaCount,"+\
                "editor_createPassedCount,"+\
                "editor_commitTotalCount,"+\
                "editor_experience,"+\
                "editor_passRatio,"+\
                "flag) values (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s)"
        try:
            cursor.execute\
                (sql,[baidu_item[0],baidu_item[1],baidu_item[2],baidu_item[3]
                , baidu_item[4], baidu_item[5],baidu_item[6],baidu_item[7]
                , baidu_item[8], baidu_item[9],baidu_item[10],baidu_item[11]
                , baidu_item[12], baidu_item[13],baidu_item[14],baidu_item[15]
                , baidu_item[16], baidu_item[17],baidu_item[18],baidu_item[19]
                , baidu_item[20], baidu_item[21],baidu_item[22],baidu_item[23]
                , baidu_item[24]])
        except:
            print("存储数据出错!大概率主键重复")
            return
        database.commit()
        cursor.close()
        print("储存成功")
    else:
        return