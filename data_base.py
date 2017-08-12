# -*- coding: utf-8 -*-
import pymssql

from timeout_deco import timeout
import user_password
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
def search_fac():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    temp = ms.ExecQuery("SELECT fac_num,fac_name FROM fac_info")
    fac_lst = []
    for line in temp:
        fac_lst.append([line[0],line[1]])
    return fac_lst
def search_maj(f):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    temp = ms.ExecQuery("SELECT ZYBH,ZYMC FROM maj_info where YXBH = %s"%f)
    maj_lst = []
    for line in temp:
        maj_lst.append([line[0].rstrip(),line[1]])
    return maj_lst
def get_gra_fac_maj(user_id_):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    m=ms.ExecQuery("select gra,fac,maj from user_info where user_id =%d "%user_id_)
    for a,b,c in m:
        a = str(a).rstrip()
        b = str(b).rstrip()
        c = str(c).rstrip()
    return a,b,c
def user_info_update_gra_fac(user_id,g,f):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("update user_info set gra = %s,fac = %s where user_id = %d"%(g,f,user_id))
def user_info_update_maj(user_id,maj):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("update user_info set maj = %s,COL_GRA_MAJ = 1 where user_id = %d"%(maj,user_id))
def search_cou_dic(gra,maj):
    #gra未使用，待完善
    #
    #!!!!!!!!!!!!!!
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    ZYMC=ms.ExecQuery("select ZYMC from maj_info where ZYBH = %s"%maj)
    try:
        ZYMC = ZYMC[0][0]
    except:
        ZYMC = u'电气工程及其自动化'
    ZYMC = ZYMC.encode('utf-8')
    m=ms.ExecQuery("select KCDM,KCMC from KCXX where NJ=%s and ZYMC = '%s' group by KCDM,KCMC"%(gra,ZYMC))
    cou_lst = []
    i = 0
    for line in m:
        jsxm=ms.ExecQuery("select XKKH,JSXM from KCXX where KCMC ='%s' and NJ=%s and ZYMC = '%s' group by XKKH,JSXM"%(line[1].encode('utf-8'),gra,ZYMC))
        jsxm_list = [[]]
        for i in jsxm:
            jsxm_list[0].append([i[0],i[1]])
        cou_lst.append([line[0].rstrip(),line[1],jsxm_list[0]])
        #print cou_lst
    #sort = sorted(cou_dic.iteritems(), key = lambda asd:asd[0], reverse=False)
    return cou_lst
def search_cou_bind_id(bind_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    m=ms.ExecQuery("select KCDM,KCMC,jxrwb2.BH,JSXM from ZFXFZB_XKXXB_LH join jxrwb2 on ZFXFZB_XKXXB_LH.XKKH = jxrwb2.XKKH where XH =%s"%bind_id)
    cou_lst = []
    for line in m:
        jsxm_list = []
        jsxm_list.append([line[2],line[3]])
        cou_lst.append([line[0].rstrip(),line[1],jsxm_list])
        #print cou_lst
    #sort = sorted(cou_dic.iteritems(), key = lambda asd:asd[0], reverse=False)
    return cou_lst
def update_rating(user_id,rat_lst):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    for i,j in rat_lst:
        ms.ExecNonQuery(u"insert into user_cour_rating values (%d,%d,%d)"%(user_id,int(i),int(j)))
def delete_rating(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("delete from user_cour_rating where user_id = %d "%user_id)
    
def get_COL_RATING(user_id_):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    m=ms.ExecQuery("select COL_RATING from user_info where user_id =%d "%user_id_)
    try:
        COL = m[0][0]
    except:
        COL = 0
    return COL

def user_info_update_COL_RATING(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("update user_info set COL_RATING = 1 where user_id = %d"%user_id)
    
def get_user_id(user):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    #服务器停止服务后再次开启，下面的查询语句会导致服务器卡死？原因未找到
    m=ms.ExecQuery("select user_id from user_info where user_name=%r"%user)
    try:
        user_id = m[0][0]
    except:
        #admin_id = 9
        user_id = 9
    return user_id
def write_user_info(user):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("insert into user_info (user_name,COL_NUM,COl_RATING,gra,fac,maj,spare_time,bind_id) values (%r,%d,%d,NULL,NULL,NULL,NULL,NULL)"%(user,0,0))
    print 'location_:sign_up_online_data_base_write_user_info__id_:00'
def delete_user_info(user_name):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    user_id = get_user_id(user_name)
    ms.ExecNonQuery("delete from spare_time where user_id = '%s' "%user_id)
    ms.ExecNonQuery("delete from user_xksj where user_id = '%s' "%user_id)
    ms.ExecNonQuery("delete from col_rat_time where user_id = '%s' "%user_id)
    ms.ExecNonQuery("delete from user_info where user_name = '%s' "%user_name)
    print 'location_:delete_account_online_data_base_delete_user_info__id_:00'    
def create_train():
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

def get_user_sim(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select other_user_id,sim from user_sim where user_id = %d"%user_id)
    #print m[:10]
    _w = []
    n  = len(m)
    for other,sim in m:
        if other==None or sim == None:
            continue
        else:
            _w.append([other,sim]) 
    return _w
def get_item_sim(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    item_lst = ms.ExecQuery("select item from train where [user] = %d"%int(user_id))
    _w = {}
    #print item_lst
    for item in item_lst:
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
        m = ms.ExecQuery("select other_item,sim from item_sim where item = %d"%item[0])
    #print m[:10]
        _w.setdefault(item[0],[])
        for lst in m:
            if lst[0]==None or lst[1] == None:
                continue
            else:
                _w[item[0]].append((lst[0],lst[1]))
    #print _w.keys()
    #print _w[385]
    return _w
def write_spare_time(lst):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    for user_id,time in lst:
        ms.ExecNonQuery("insert into spare_time values ('%d','%d')"%(int(user_id),int(time)))
    #print m[:10]
    user_id = lst[0][0]
    ms.ExecNonQuery("update user_info set spare_time = 1 where user_id = %d"%(user_id))
def delete_spare_time(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    ms.ExecNonQuery("delete from spare_time where user_id = %d "%user_id)
    
def get_spare_time_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select spare_time from user_info where user_id = %d"%user_id)
    try:
        flag = m[0][0]
    except:
        flag = 0
    return flag

def get_bind_id(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select bind_id from user_info where user_id = %d"%user_id)
    try:
        XH = m[0][0]
    except:
        XH = '1151180812'
    return XH
def update_bind_id(user_id,bind_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    NJ_ZYMC = ms.ExecQuery("select NJ,ZYMC from ZFXFZB_XKXXB_LH where XH = '%s' and NJ>2000"%bind_id)
    print 'location_:online_data_base_update_bind_id__id_:11-01'
    try:
        ZYMC = NJ_ZYMC[0][1].encode('utf-8')
        NJ = NJ_ZYMC[0][0]
    except:
        ZYMC = u'电气工程及其自动化'.encode('utf-8')
        NJ = 2015
    print 'location_:online_data_base_update_bind_id__id_:11-02'
    fac_maj = ms.ExecQuery("select YXBH,ZYBH from maj_info where ZYMC ='%s'"%ZYMC)
    try:
        fac = fac_maj[0][0]
        maj = fac_maj[0][1]
    except:
        fac = 001
        maj = 001
    print 'location_:online_data_base_update_bind_id__id_:11-03'
    ms1 = MSSQL(host="localhost",user="sa",pwd="123456",db="xuanke")  
    ms1.ExecNonQuery("update user_info set gra = %s,fac = %s,maj = %s,bind_id = %s where user_id = %d"%(NJ,fac,maj,bind_id,user_id))
    print 'location_:online_data_base_update_bind_id__id_:11-04'

def re_get_train():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    temp = ms.ExecQuery("SELECT user_id,BH,rating FROM user_cour_rating ")
    train={}
    for user, item, rating in temp:
        train.setdefault(user, {})
        train[user][item] = rating
    return train
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
def search_detail(BH):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")  
    m = ms.ExecQuery("select KCMC,JSXM,SKSJ,XF,XN from jxrwb2 where BH = %d group by KCMC,JSXM,SKSJ,XF,XN"%BH)
    return m
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
def course_filtering(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    user_KCDM_list=ms.ExecQuery("select t2.KCDM from user_cour_rating as t1 join [XKXX].[dbo].[jxrwb2] as t2 on t1.BH=t2.BH where user_id=%d group by t2.KCDM"%user_id)
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    all_BH_list = []
    for KCDM in user_KCDM_list:
        BH_list = ms.ExecQuery("select BH from jxrwb2 where KCDM='%s' group by BH"%KCDM)
        for row in BH_list:
            all_BH_list.append(row[0])
    return all_BH_list
def insert_xksj(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    ms.ExecNonQuery("delete from [xuanke].[dbo].[user_XKSJ] where user_id = %d "%user_id)
    XH = get_bind_id(user_id)
    XN_list = ms.ExecQuery("select t2.XN,t2.XQ from ZFXFZB_XKXXB_LH as t1 join jxrwb2 as t2 on t1.XKKH = t2.XKKH where t1.XH ='%s' group by t2.XN,t2.XQ"%XH)
    for XN,XQ in XN_list:
        ms.ExecNonQuery(u"insert into [xuanke].[dbo].[user_XKSJ] (user_id,XN,XQ,flag,ulike,dislike) values(%d,%r,%d,0,0,0)"%(user_id,str(XN),XQ))
def get_user_XKSJ_flag(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    flag = ms.ExecQuery("select flag from user_XKSJ where user_id = %d"%user_id)
    return flag
def get_user_info_flag(user_id):
    # 查询用户是否完成规定流程
    # 返回标志字典，没有完成标志为0
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    flag = ms.ExecQuery("select user_id,bind_id,COL_RATING,spare_time from user_info where user_id = %d"%user_id)
    try:
        user_id = flag[0][0]
    except:
        user_id = 9
        flag = ms.ExecQuery("select user_id,bind_id,COL_RATING,spare_time from user_info where user_id = %d"%user_id)
    if flag[0][1]==None:
        bind_id = 0
    else:
        bind_id = flag[0][1]
    if flag[0][2]==None:
        COL_RATING = 0
    else:
        COL_RATING = flag[0][2]
    if flag[0][3]==None:
        spare_time = 0
    else:
        spare_time = flag[0][3]
    flag_dic = {'user_id':user_id,'bind_id':bind_id ,'COL_RATING':COL_RATING,'spare_time':spare_time}    
    return flag_dic
def online_admin():
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    user_info = ms.ExecQuery("select user_name,COL_RATING,gra,ZYMC,spare_time,bind_id from user_info as t1 join [XKXX].[dbo].[maj_info] as t2 on convert(int,t2.ZYBH)=convert(int,t1.maj)")
    #user_rating= ms.ExecQuery("select * from user_cour_rating")
    #print user_rating[:10]
    print user_info
    dic ={}
    dic['user_info'] = user_info
    return dic
if __name__ == '__main__':
    #write_user_info('liuheng123')
    #maj_dic,sort = search_maj('001')
    #print sort[0][1]
    #gra,fac,maj = get_gra_fac_maj(1)
    #print search_fac()
    #print len(search_cou_dic(gra,maj))
    #get_item_sim(9)
    #get_bind_id(9)
    #get_user_info_flag(3)
    online_admin()
    print '11111111111111111111111111111111111111111111111'
        
        
