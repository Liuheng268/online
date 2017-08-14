# -*- coding: utf-8 -*-
# 此代码目的：推荐程序调用
# 此代码需要调用的变量形式或文件类型如下：
#    
#    
# 此代码归属模块：推荐模块
import numpy as np
import lfm
import user_cf
import item_cf
import data_base
import SKSJ_compare
from online.info_search import search

def re_user_cf(start,user,n):
    #根据真实评分数据产生推荐列表
    #获取原始训练集
    train = data_base.re_get_train()
    #过滤无效信息的有效训练集
    train = screening_training_set(train,threshold = 0.1)
    #如果有效训练集中不含当前用户，则添加当前用户评分到训练集中备用
    if user not in train.keys():
        print 'user not in screening_training_set'
        user_rating = data_base.get_user_rating(user)
        train[user] = user_rating
        print 'adding user rating successfully'
    user_cf.pre_treat(train, False)
    user_cf.user_similarity_cosine(train, iif=False, implicit=False)
    result = user_cf.recommend_explicit(user)
    if result =='less_than_standard':
        rec = 'less_than_standard'
        return rec
    else:
        new_rank = Course_filtering(user,result)
        
        rank_lst = transfer_lst(start,n,new_rank)
        #rank = course_filtering_SKSJ(rank_lst,user)
        rec = add_pre_avr_min(rank_lst)
        return rec

def re_lfm(start,user,n):
    #根据真实评分数据产生推荐列表
    #获取原始训练集
    train = data_base.re_get_train()
    #过滤无效信息的有效训练集
    train = screening_training_set(train,threshold = 0.1)
    #如果有效训练集中不含当前用户，则添加当前用户评分到训练集中备用
    if user not in train.keys():
        print 'user not in screening_training_set'
        user_rating = data_base.get_user_rating(user)
        train[user] = user_rating
        print 'adding user rating successfully'
    lfm.factorization(train, bias=True, svd=True, svd_pp=True, steps=5, gamma=0.03, slow_rate=0.94, Lambda=0.1)
    result = lfm.recommend_explicit(user)
    if result ==[]:
        rec = 'less_than_standard'
        return rec
    else:
        new_rank = Course_filtering(user,result)
        rank_lst = transfer_lst(start,n,new_rank)
        #rank = course_filtering_SKSJ(rank_lst,user)
        rec = add_pre_avr_min(rank_lst)
        return rec

def re_item_cf(start,user,n):
    train = data_base.re_get_train()
    #过滤无效信息的有效训练集
    train = screening_training_set(train,threshold = 0.1)
    #如果有效训练集中不含当前用户，则添加当前用户评分到训练集中备用
    if user not in train.keys():
        print 'user not in screening_training_set'
        user_rating = data_base.get_user_rating(user)
        train[user] = user_rating
        print 'adding user rating successfully'
    item_cf.__pre_treat(train, False)
    item_cf.item_similarity_cosine(train, iuf=False, implicit=False)
    result = item_cf.recommend_explicit(user)
    rank1 = result['rank']
    explain = result['explain']
    if rank1 ==[]:
        rec = 'less_than_standard'
        return rec
    else:
        rank2 = Course_filtering(user,rank1)
        rank3 = transfer_lst(start,n,rank2)
        #print rank_lst
        #rank = course_filtering_SKSJ(rank_lst,user)
        rank4 = add_pre_avr_min(rank3)
        rank5 = add_explain(explain,rank4)
        return rank5
def add_explain(explain, rank):
    explain_lst = list(explain)
    new_rank = []
    for item,item1 in explain_lst:
        KCMC = data_base.get_cou_name(item1)
        for row in rank:
            if item == row[4]:
                new_rank.append([row[0],row[1],row[2],row[3],row[4],row[5],KCMC])
    #print new_rank
    new_rank.sort(key=lambda x:x[3] ,reverse=True)
    return new_rank
def get_train():
    # 从数据库获取用户评分数据
    train = data_base.create_train()
    return train
def Course_filtering(user,rank):
    # 过滤用户已选课程及相似课程（不同教师）
    all_BH_list = data_base.course_filtering(user)
    rank2 = list(rank)
    rank2.sort(key=lambda x:x[1] ,reverse=True)
    new_rank = []
    for BH,rating in rank2 :
        if BH in all_BH_list:
            continue
        else:
            new_rank.append([BH,rating])
    return new_rank

def course_filtering_SKSJ(rank,user_id):
    # 将已经获得的课程列表中与用户空闲时间列表有冲突的课程过滤
    user_spare_time = data_base.get_spare_time(user_id)
    time1 = transfer_lst_to_string(user_spare_time)
    new_rank = []
    for row in rank:
        if not row:
            continue
        time2_lst = data_base.get_SKSJ(row[4])
        time2 = transfer_lst_to_string(time2_lst)
        if not time2:
            continue
        flag = SKSJ_compare.judge_contain(time1,time2)
        if flag ==1:
            new_rank.append(row)
    return new_rank

def transfer_lst_to_string(time_lst):
    # 将从数据库获得的SKSJ列表转化成字符串str，与上课时间比较程序算法衔接
    string = ''
    for row in time_lst:
        string +=row+';'
    return string
        
        
def transfer_lst(start,n,rank):
    # 将协同过滤算法获得的推荐列表变换成向用户展示的形式
    lst = list(rank)
    #lst = sorted(lst,key=lambda t:t[1],reverse=True)
    rec = []
    for line in lst[start:start+n]:
        temp = data_base.search_teacher(line[0])
        if temp:
            rec.append([temp[0][0],temp[0][1],temp[0][2],line[1],line[0]])
    return rec

def get_2016_2017_2_XXK(user_id):
    # 在用户已经填写空闲课程时间后！！
    # 获取与该用户没有时间冲突的所有选修课列表
    rank = data_base.get_2016_2017_2XXK()
    new_rank = course_filtering_SKSJ(rank,user_id)
    return new_rank

def add_pre_avr_min(rank):
    #增加预测-平均分差
    s = search.SEARCH()
    #time_start = time.time()
    avr_rank = data_base.get_avr()
    #time_stop = time.time()
    #print 'calculate recommend rank cost %.05f seconds'%(time_stop-time_start)    
    new_rank = []
    for row in rank:
        for avr_row in avr_rank:
            if row[4]==avr_row[0]:
                new_rank.append([row[0],row[1],row[2],row[3],row[4],row[3]-avr_row[2]])
    new_rank.sort(key=lambda x:x[3] ,reverse=True)
    return new_rank

def screening_training_set(train,threshold=0.1):
    #筛选训练集，删除无效数据，提高算法精度
    #返回有效训练集
    #threshold:阈值
    s_train = {}
    for user in train.keys():
        rating_std = np.std(train[user].values())
        #print 'user:',user,' ***  std:',rating_std
        if rating_std > threshold:
            s_train[user] = train[user]
    #print len(s_train.keys())
    #print s_train
    return s_train
if __name__ == '__main__':

    #rank = re_user_cf(0,9,10)
    rank = get_2016_2017_2_XXK(9)
    print len(rank)
    for a,b,c,d,e in rank:
        print a,b,c,d,e
    #print re_item_cf(0,1,10)
    #print re_lfm(0,1,10)
    
