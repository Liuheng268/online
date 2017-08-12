# -*- coding: utf-8 -*-
import pymssql
import numpy as np
from online.timeout_deco import timeout
from online import user_password
dbo_user,dbo_password = user_password.get_user_password()
class MSSQL:
    

    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
    @timeout(0.5)
    def __GetConnect(self):
        
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur
    @timeout(3)
    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()
        self.conn.close()
        return resList
    @timeout(0.5)
    def ExecNonQuery(self,sql):
        
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

#*************************************************************************
def create_train():
    # 从电影评分数据集中获取训练集
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select [user],item,rating from train")
    #print m[:5]
    train = {}
    for user,item,rating in m:
        user, item, rating = int(user), int(item), int(rating)
        train.setdefault(user, {})
        train[user][item] = rating
    #print train.keys()
    return train

def re_get_train():
    # 从真实课程评分数据中获取训练集
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    temp = ms.ExecQuery("SELECT user_id,BH,rating FROM user_cour_rating ")
    train={}
    for user, item, rating in temp:
        train.setdefault(user, {})
        train[user][item] = rating
    return train

def search_teacher(BH,KCXZ_flag=0):
    # 已知课程编号，课程性质
    # 获取课程代码，课程名称，教师姓名
    #KCXZ_flag 0:全部课程；1：校选修课；2：必修课
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    if KCXZ_flag ==1:
        KCXZ = u'校选修课'.encode('utf-8')
        m = ms.ExecQuery("select KCDM,KCMC,JSXM from jxrwb2 where BH = %d and KCXZ ='%s'"%(BH,KCXZ))
    elif KCXZ_flag ==2:
        KCXZ = u'必修课'.encode('utf-8')
        m = ms.ExecQuery("select KCDM,KCMC,JSXM from jxrwb2 where BH = %d and KCXZ ='%s'"%(BH,KCXZ))
    else :
        m = ms.ExecQuery("select KCDM,KCMC,JSXM from jxrwb2 where BH = %d"%BH)
    return m

def course_filtering(user_id):
    # 获取用户已选课程中课程代码相同（相同课程，不同老师或不同时间）的课程的课程编号
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    user_KCDM_list=ms.ExecQuery("select t2.KCDM from user_cour_rating as t1 join [XKXX].[dbo].[jxrwb2] as t2 on t1.BH=t2.BH where user_id=%d group by t2.KCDM"%user_id)
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    all_BH_list = []
    for KCDM in user_KCDM_list:
        BH_list = ms.ExecQuery("select BH from jxrwb2 where KCDM='%s' group by BH"%KCDM)
        for row in BH_list:
            all_BH_list.append(row[0])
    return all_BH_list

def get_cou_lst(user_id,XN,XQ):
    # 已知学年，学期，用户编号
    # 获取用户对应年度、学期已选课程列表
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    XH = get_XH(user_id)
    m=ms.ExecQuery("select KCDM,KCMC,t2.BH,JSXM from ZFXFZB_XKXXB_LH as t1 join jxrwb2 as t2 on t1.XKKH = t2.XKKH where XH ='%s' and t2.XN ='%s' and t2.XQ =%d"%(XH,XN,XQ))
    cou_lst = []
    for line in m:
        cou_lst.append([line[0].rstrip(),line[1],line[2],line[3]])
    return cou_lst

def get_spare_time(user_id):
    # 获取用户空闲时间列表
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    lst = ms.ExecQuery("select spare_time from spare_time where user_id = %d order by spare_time desc"%user_id)
    time_lst = []
    for row in lst:
        time_lst.append(row[0])
    return time_lst
def get_SKSJ(BH):
    # 获取已知课程编号的课程的上课时间，返回列表
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    m=ms.ExecQuery("select SKSJ,XN,XQ from jxrwb2 where BH =%d and XN ='2016-2017' and XQ =2"%BH)
    lst = []
    for a,b,c in m:
        lst.append(a)
    return lst
def get_2016_2017_2XXK():
    # 获取2016-2017年第二学期选修课列表
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    KCXZ = u'校选修课'
    KCXZ = KCXZ.encode('utf-8')
    lst=ms.ExecQuery("select KCDM,KCMC,JSXM,SKSJ,BH from jxrwb2 where XN ='2016-2017' and XQ =2 and KCXZ = '%s'"%KCXZ)
    cou_lst = []
    for line in lst:
        cou_lst.append([line[0],line[1],line[2],line[3],line[4]])
    return cou_lst

def get_user_rating(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    temp = ms.ExecQuery("SELECT user_id,BH,rating FROM user_cour_rating where user_id = %d"%user_id)
    train={}
    for user, item, rating in temp:
        train[item] = rating
    return train

def get_all_xuanxiu_BH():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    KCXZ = u'校选修课'.encode('utf-8')
    temp = ms.ExecQuery("SELECT BH FROM jxrwb2 where KCXZ='%s' and XN='2016-2017'"%KCXZ)
    BH_lst = []
    for row in temp:
        BH_lst.append(row[0])
    #print 12 in BH_lst
    return BH_lst
def get_avr():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    temp = ms.ExecQuery("SELECT [BH],count(BH),round(avg(cast(rating as float)),2) FROM [xuanke].[dbo].[user_cour_rating] group by BH")
    BH_lst = []
    for row in temp:
        BH_lst.append([row[0],row[1],row[2]])
    #print 12 in BH_lst
    return BH_lst
def get_cou_name(BH):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    m = ms.ExecQuery("select KCMC from jxrwb2 where BH =%d"%BH)
    try:
        KCMC = m[0][0]
    except:
        KCMC = u'查询错误'
    return KCMC
    

if __name__ == '__main__':
    #write_user_info('liuheng123')
    #maj_dic,sort = search_maj('001')
    #print sort[0][1]
    #gra,fac,maj = get_gra_fac_maj(1)
    #print search_fac()
    #print len(search_cou_dic(gra,maj))
    #get_item_sim(9)
    #get_bind_id(9)
    #get_SKSJ(2203)
    #get_2016_2017_2XXK()
    #re_get_train()
    #get_user_rating(9)
    get_all_xuanxiu_BH()
        
