# -*- coding: utf-8 -*-
import pymssql
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
    @timeout(0.5)
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
def get_user_info():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    user_info = ms.ExecQuery("select user_id,user_name,COL_RATING,gra,ZYMC,spare_time,bind_id from user_info as t1 join [XKXX].[dbo].[maj_info] as t2 on convert(int,t2.ZYBH)=convert(int,t1.maj)")
    return user_info

def create_re_train():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select user_id,BH,rating from user_cour_rating")
    train = {}
    for user,item,rating in m:
        user, item, rating = int(user), int(item), int(rating)
        train.setdefault(user, {})
        train[user][item] = rating
    return train
def get_all_xuanxiu_BH():
    ms = MSSQL(host="localhost",user="xuankeadmin",pwd="xuanketuijian1996LH",db="XKXX")
    KCXZ = u'校选修课'.encode('utf-8')
    temp = ms.ExecQuery("SELECT BH FROM jxrwb2 where KCXZ='%s' and XN='2016-2017'"%KCXZ)
    BH_lst = []
    for row in temp:
        BH_lst.append(row[0])
    #print 12 in BH_lst
    return BH_list

def get_avr(threshold=0):
        #根据数据集计算平均评分
        #threshold:评分人数阈值，小于阈值则过滤数据
        KCXZ = u'校选修课'.encode('utf-8')
        ms = MSSQL(host="localhost",user="xuankeadmin",pwd="xuanketuijian1996LH",db="xuanke")  
        m = ms.ExecQuery("select user_id,t1.BH,rating from [xuanke].[dbo].[user_cour_rating] as t1 left join [XKXX].[dbo].[jxrwb2] as t2 on t1.BH=t2.BH where KCXZ='%s' group by user_id,t1.BH,rating"%KCXZ)
        _item_users = {}
        for user,item,rating in m:
            user, item, rating = int(user), int(item), int(rating)
            _item_users.setdefault(item, {})
            _item_users[item][user] = rating
        _avr = {}
        for item, users in _item_users.iteritems():
            if len(users)>threshold:
                _avr[item]={}
                _avr[item]['rating'] = sum(users.itervalues())*1.0 / len(users)
                _avr[item]['count'] = len(users)
        print _avr
        return _avr
def get_maj(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select maj from user_info where user_id =%d"%user_id)
    try:
        maj = int(m[0][0])
    except:
        maj = 5
    return maj
def get_maj_user_tuple(maj):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select user_id from user_info where maj =%d"%maj)
    user_lst = []
    for row in m:
        user_lst.append(row[0])
    if len(user_lst) ==1:
        user_tuple_str = '(%d)'%user_lst[0]
    else:
        user_tuple_str = str(tuple(user_lst))
    return user_tuple_str

def get_all_xuanxiu_BH():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    KCXZ = u'校选修课'.encode('utf-8')
    temp = ms.ExecQuery("SELECT BH FROM jxrwb2 where KCXZ='%s' and XN='2016-2017'"%KCXZ)
    BH_lst = []
    for row in temp:
        BH_lst.append(row[0])
    #print 12 in BH_lst
    return BH_lst

def get_maj_avr_rating(user_tuple_str, threshold=5):
    #只保留与用户同专业的选修课平均分
    BH_list = get_all_xuanxiu_BH() #选修课列表
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    sql = "select a.BH,count(BH),round(avg(cast(a.rating as float)),2) as avr from (select user_id,BH,rating from [xuanke].[dbo].[user_cour_rating] where user_id  in %s group by user_id,BH,rating) a group by a.BH order by avr desc"%user_tuple_str
    m = ms.ExecQuery(sql)
    _avr = {} #平均评分字典
    for item,count,avr in m:
        if item not in BH_list:
            continue
        if count>=threshold: #评分人数阈值
            _avr[item]={}
            _avr[item]['rating'] = avr
            _avr[item]['count'] = count
    return _avr
def transfer_lst(start,n,rank):
    #如果n=0,返回全部平均评分 
    lst = list(rank)
    lst = sorted(lst,key=lambda t:t[1],reverse=True)
    rec = []
    if n==0:
        for line in lst:
            temp = search_teacher(line[0],KCXZ_flag=0)
            if temp:
                rec.append([temp[0][0],temp[0][1],temp[0][2],line[1],line[0],line[2]])
    else:
        for line in lst[start:start+n]:
            temp = search_teacher(line[0],KCXZ_flag=0)
            if temp:
                rec.append([temp[0][0],temp[0][1],temp[0][2],line[1],line[0],line[2]])
    return rec

def search_teacher(BH,KCXZ_flag=0):
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
def get_maj_name(maj):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    m = ms.ExecQuery("select ZYMC from maj_info where ZYBH=%d"%maj)
    try:
        maj_name = m[0][0]
    except:
        maj_name = u'查询错误'
    return maj_name
if __name__ == '__main__':
    
    get_user_info()
        
        
