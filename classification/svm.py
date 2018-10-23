from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.preprocessing import scale
IS_TRAIN=True
def cal_result(my_result,target):
    correct=0
    i=0
    for each in my_result :
        if each==target[i]:
            correct+=1
        i+=1
    return correct/len(my_result)
if __name__ == '__main__':
    #训练
    if IS_TRAIN:
        train=pd.read_csv('/home/molamola/桌面/数据集/百度词条数据集/实验数据/svm-3/trainwithouttarget.csv')
        test=pd.read_csv('/home/molamola/桌面/数据集/百度词条数据集/实验数据/svm-3/testwithouttarget.csv')
        #
        x_train=scale(train.values)
        print(x_train[0])
        target=pd.read_csv('/home/molamola/桌面/数据集/百度词条数据集/实验数据/svm-3/target.csv')
        y_train=target.values
        #
        x_test=scale(test.values)
        print(x_test[0])
        test_target=pd.read_csv('/home/molamola/桌面/数据集/百度词条数据集/实验数据/svm-3/test-target.csv')
        y_test=test_target.values
        trainer=svm.SVC()
        trainer.fit(x_train,y_train)
        ####
        result=trainer.predict(x_test)
        print("svm分类器准确率:"+str(cal_result(result,y_test)))

