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

def get_user_XKSJ_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    flag = ms.ExecQuery("select XN,XQ,flag from user_XKSJ where user_id = %d and flag = 0 order by XN,XQ  "%user_id)
    return flag
def count_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    lst = ms.ExecQuery("select count(flag) from user_XKSJ where user_id = %d and flag = 1"%user_id)
    if lst:
        count = lst[0][0]
    else:count =0
    return count
def get_user_xksj(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    user_xksj = ms.ExecQuery("select XN,XQ from user_XKSJ where user_id = %d"%user_id)
    return user_xksj
def get_XH(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select bind_id from user_info where user_id = %d"%user_id)
    return m[0][0]
def get_cou_lst(user_id,XN,XQ):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    XH = get_XH(user_id)
    m=ms.ExecQuery("select KCDM,KCMC,t2.BH,JSXM from ZFXFZB_XKXXB_LH as t1 join jxrwb2 as t2 on t1.XKKH = t2.XKKH where XH ='%s' and t2.XN ='%s' and t2.XQ =%d"%(XH,XN,XQ))
    cou_lst = []
    for line in m:
        cou_lst.append([line[0].rstrip(),line[1],line[2],line[3]])
    return cou_lst
def delete_rating(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("delete from user_cour_rating where user_id = %d "%user_id)
def update_rating(user_id,rat_lst,XN,XQ):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    for i,j in rat_lst:
        ms.ExecNonQuery(u"insert into user_cour_rating values (%d,%d,%d)"%(user_id,int(i),int(j)))
    ms.ExecNonQuery(u"update user_XKSJ set flag =1 where user_id = '%s' and XN ='%s' and XQ =%d"%(user_id,XN,XQ))
def update_XKSJ_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery(u"update user_XKSJ set flag =0 where user_id = '%s'" %user_id)
    print 'set XKSJ_flag = 0 successfully'
def write_time(user_id,time,flag):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    if flag =='start':
        ms.ExecNonQuery("insert into col_rat_time (user_id,start_time,end_time) values(%d,%r,0)"%(user_id,time))
    elif flag =='end':
        ms.ExecNonQuery("update col_rat_time set end_time = %r where user_id =%d"%(time,user_id))
def delete_time(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("delete from col_rat_time where user_id = %d "%user_id)
def write_spare_time(user_id,time,time_flag):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("insert into spare_time (user_id,spare_time,time_flag) values(%d,'%s','%s')"%(user_id,time,time_flag))
def delete_spare_time(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("delete from spare_time where user_id = %d "%user_id)
def get_spare_time(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    lst = ms.ExecQuery("select spare_time from spare_time where user_id = %d order by spare_time desc"%user_id)
    time_lst = []
    for row in lst:
        time_lst.append(row[0])
    return time_lst
def update_COL_RATING(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery(u"update user_info set COL_RATING =1 where user_id = %d"%user_id)
    print 'set COL_RATING = 1 successfully'
def update_COL_RATING_delete(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery(u"update user_info set COL_RATING=null where user_id = %d "%user_id)
    delete_rating(user_id)
    print 'delete rating successfully'
    
def write_user_info_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("update user_info set spare_time =1 where user_id=%d"%user_id)

def update_spare_time_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("update user_info set spare_time=0  where user_id = %d"%user_id)

if __name__ == '__main__':
    #get_cou_lst(9,'2015-2016',1)
    get_spare_time(9)
        
        
