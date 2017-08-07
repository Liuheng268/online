# -*- coding: utf-8 -*-
# 此代码目的：评分收集程序
# 此代码需要调用的变量形式或文件类型如下：
#    
#    
# 此代码归属模块：评分收集模块

import data_base
import time
from datetime import datetime

def get_cou_lst(user_id):
    # 获取用户已选课程列表
    flag = data_base.get_user_XKSJ_flag(user_id)
    count = data_base.count_flag(user_id)
    if flag:
        for XN,XQ,f in flag[:1]:
            cou_lst = data_base.get_cou_lst(user_id,XN,XQ)
            dic = {}
            dic['lst'] =cou_lst
            dic['XN'] =XN
            dic['XQ'] =XQ
            if count>=4:
                dic['count']=1
        return dic
    else:
        dic ={}
        dic['lst'] =''
        return dic
def write_into_data_base(user_id,rat_lst,XN,XQ):
    # 将用户评分存入数据库
    data_base.update_rating(user_id,rat_lst,XN,XQ)

def set_col_time(user_id,flag):
    # 记录评分开始与结束时间，为提升系统健壮性做准备
    if flag =='start':
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # 先删除已有的时间数据，避免重复，重新设置时间数据
        data_base.delete_time(user_id)
        write_time(user_id,start_time,flag)
    elif flag =='end':
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        write_time(user_id,end_time,flag)
        update_COL_RATING(user_id)
    else:
        pass

def write_time(user_id,time,flag):
    # 将评分开始和结束时间存入数据库
    data_base.write_time(user_id,time,flag)

def update_COL_RATING(user_id):
    # 更新user_info 中评分收集完成的标志
    data_base.update_COL_RATING(user_id)

def update_COL_RATING_delete(user_id):
    data_base.update_COL_RATING_delete(user_id)
    data_base.update_XKSJ_flag(user_id)
if __name__ == '__main__':
    get_cou_lst(9)
