# -*- coding: utf-8 -*-
# 此代码目的：学号绑定认证程序
# 此代码需要调用的变量形式或文件类型如下：
#    
#    
# 此代码归属模块：学号绑定模块
import random
import data_base

def get_cou_list(XH):
    selected_lst = data_base.get_selected_cou(XH)
    full_lst = data_base.get_full_cou()
    flag = 0
    while flag ==0:
        n = 0
        random_selected_lst = random.sample(selected_lst,2)
        random_full_lst = random.sample(full_lst, 3)
        selected_dic = dict(selected_lst)
        full_dic = dict(random_full_lst)
        for value in selected_dic.values():
            if value in full_dic.values():
                continue
            else:
                n += 1
        if n == len(selected_dic):
            flag = 1
    result= random_selected_lst+random_full_lst
    random.shuffle(result)
    dic = {}
    dic['result'] = result
    dic['confirm'] = list(dict(random_selected_lst).keys())
    return dic
def confirm(select,result):
    flag = 1
    for i in select:
        if i not in result:
            flag = 0
    return flag
def delete_bind_id(user_id):
    data_base.delete_bind_id(user_id)

if __name__ == '__main__':
    get_cou_list('1151180812')

