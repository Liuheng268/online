# -*- coding: utf-8 -*-
import data_base
import numpy as np
#***************************************************************************

def user_info():
    user_info = data_base.get_user_info()
    train = data_base.create_re_train()
    new_lst = []
    for row in user_info:
        try:
            rating_std = np.std(train[row[0]].values())
            new_lst.append([row[1],row[2],row[3],row[4],row[5],row[6],rating_std])
        except:
            new_lst.append([row[1],row[2],row[3],row[4],row[5],row[6],'未填写评分'])
    dic = {}
    dic['user_info'] = new_lst
    dic1 = extra_info(new_lst)
    dic.update(dic1)
    return dic

def extra_info(new_lst):
    #计算用户评分标准差，用于判断评分有效性
    dic = {}
    user_num = len(new_lst)
    dic['user_num'] = user_num
    rating_num = 0
    useful_rating_num = 0
    for row in new_lst:
        if row[6]>0.5:
            useful_rating_num+=1
        if row[1] ==1:
            rating_num +=1
    dic['useful_rating_num'] = useful_rating_num
    dic['rating_num'] = rating_num
    return dic

def get_maj_avr(user_id, threshold=5):
    maj = data_base.get_maj(user_id)
    maj_name = data_base.get_maj_name(maj)
    user_tuple_str = data_base.get_maj_user_tuple(maj)
    #print user_tuple_str
    item_avr = data_base.get_maj_avr_rating(user_tuple_str,threshold)
    lst = []
    for item in item_avr.keys():
        lst.append([item,item_avr[item]['rating'],item_avr[item]['count']])
    rank = data_base.transfer_lst(0,0,lst)
    #for row in rank:
        #print row
    dic = {}
    dic['rank'] = rank
    dic['maj_name'] = maj_name
    return dic

