# -*- coding: utf-8 -*-
# 此代码目的：空闲时间收集程序
# 此代码需要调用的变量形式或文件类型如下：
#    
#    
# 此代码归属模块：推荐系统模块
import time
import data_base

def col_spare_time(user_id,dic):
    spare_time = transfer_to_str(dic)
    spare_time = spare_time.encode('utf-8')
    time_flag = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    write_into_data_base(user_id,spare_time,time_flag)
    
def transfer_to_str(dic):
    # 将网页收集的空闲时间数据转换成固定格式
    # 例如：'周二第1,2节{第3-6周};周四第1,2节{第3-5周}'
    XQ = dic['XQ']
    start_week = dic['start_week']
    end_week = dic['end_week']
    SKSJ = dic['SKSJ']
    result = XQ+u'第'+SKSJ+u'节'+u'{第'+start_week+'-'+end_week+u'周}'
    return result

def write_into_data_base(user_id,time,time_flag):
    #将用户空闲时间存入数据库
    data_base.write_spare_time(user_id,time,time_flag)

def delete_spare_time(user_id):
    data_base.delete_spare_time(user_id)
    data_base.update_spare_time_flag(user_id)

def get_spare_time(user_id):
    time_lst = data_base.get_spare_time(user_id)
    return time_lst
def write_user_info_flag(user_id):
    data_base.write_user_info_flag(user_id)

if __name__ == '__main__':
    dic = {'XQ':u'周一','start_week':'2','end_week':'8','SKSJ':'1,2'}
    user_id = 9
    time = transfer_to_str(dic)
    time = time.encode('utf-8')
    write_into_data_base(user_id,time)
