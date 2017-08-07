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

def get_selected_cou(XH):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    KCXZ = u'校选修课'
    KCXZ = KCXZ.encode('utf-8')
    m=ms.ExecQuery("select jxrwb2.KCDM,jxrwb2.KCMC from ZFXFZB_XKXXB_LH as XKXXB join jxrwb2 on XKXXB.XKKH = jxrwb2.XKKH where XH ='%s' and KCXZ ='%s'"%(XH,KCXZ))
    return m
def get_full_cou():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    KCXZ = u'校选修课'
    KCXZ = KCXZ.encode('utf-8')
    m=ms.ExecQuery("select top 50 KCDM,KCMC from jxrwb2 where KCXZ='%s' and XN='2015-2016' group by KCDM,KCMC"%KCXZ)
    return m
def delete_bind_id(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("update user_info set bind_id =null,gra=null,maj=null,COL_RATING=null,spare_time=null where user_id = %d"%user_id)
    delete_spare_time(user_id)
    
def delete_spare_time(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("delete from spare_time where user_id = %d "%user_id)
if __name__ == '__main__':
    pass
        
        
