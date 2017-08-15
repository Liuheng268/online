# -*- coding: utf-8 -*-
import pymssql
from online import data_base
from online.collect_info import col_spare_time
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

#***************************************************************************
    #s = data_base.SEARCH()
    
    #lst = s.search_detail(3)#课程基础信息
    #lst = s.count(5,233)#各专业历年选特定课程人数(专业编号，课程编号)
    #lst = s.avr_rating()#课程平均评分降序排列

class SEARCH:
    def __init__(self):
        pass
    def search_detail(self,BH):
        #课程基本信息
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")  
        m = ms.ExecQuery("select KCDM,KCMC,JSXM,SKSJ,XF,XN from jxrwb2 where BH = %d"%BH)
        return m
    def count(self,ZYBH,BH):
        #各专业历年选特定课程人数
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")  
        m = ms.ExecQuery("select * from Count1 where BH = %d and ZYBH =%d"%(BH,ZYBH))
        return m
    def create_re_train(self):
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
        m = ms.ExecQuery("select user_id,BH,rating from user_cour_rating")
        train = {}
        for user,item,rating in m:
            user, item, rating = int(user), int(item), int(rating)
            train.setdefault(user, {})
            train[user][item] = rating
        #print train.keys()
        return train
    def maj_re_train(self,maj):
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
        m = ms.ExecQuery("select t1.user_id,XKKH,rating from user_cour_rating as t1 join user_info as t2 on t1.user_id =t2.user_id where t2.maj=%d "%maj)
        train = {}
        for user,item,rating in m:
            user, item, rating = int(user), int(item), int(rating)
            train.setdefault(user, {})
            train[user][item] = rating
        return train
    def get_maj(self):
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
        m = ms.ExecQuery("select ZYBH from maj_info")
        return m
    def avr_rating(self,start,n,threshold = 5):
        #生成各课程平均评分降序列表
        s=SEARCH()
        item_avr = s.get_avr(threshold)
        lst = []
        for item in item_avr.keys():
            lst.append([item,item_avr[item]['rating'],item_avr[item]['count']])
        rank = s.transfer_lst(start,n,lst)
        return rank
    def transfer_lst(self,start,n,rank):
        #如果n=0,返回全部平均评分 
        lst = list(rank)
        lst = sorted(lst,key=lambda t:t[1],reverse=True)
        rec = []
        if n==0:
            for line in lst:
                temp = data_base.search_teacher(line[0],KCXZ_flag=0)
                if temp:
                    rec.append([temp[0][0],temp[0][1],temp[0][2],line[1],line[0],line[2]])
        else:
            for line in lst[start:start+n]:
                temp = data_base.search_teacher(line[0],KCXZ_flag=0)
                if temp:
                    rec.append([temp[0][0],temp[0][1],temp[0][2],line[1],line[0],line[2]])
        return rec
    def maj_avr_rating(self):
        #各专业各课程平均评分降序列表
        s=SEARCH()
        maj_lst = s.get_maj()
        final = {}
        for maj in maj_lst:
            train = s.maj_re_train(int(maj[0]))
            item_avr = s.get_avr(train)
            if item_avr:
                lst = []
                for item in item_avr.keys():
                    lst.append([item,item_avr[item]])
                lst = sorted(lst,key=lambda t:t[1],reverse=True)
                final[maj] = lst
        return final
    def get_avr(self, threshold=5):
        #根据数据集计算平均评分
        #threshold:评分人数阈值，小于阈值则过滤数据
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
        m = ms.ExecQuery("select a.BH,count(BH),round(avg(cast(a.rating as float)),2) as avr from (select user_id,BH,rating from [xuanke].[dbo].[user_cour_rating] group by user_id,BH,rating) a group by a.BH order by avr desc")
        _avr = {}
        s = SEARCH()
        BH_list = s.get_all_xuanxiu_BH()
        for item,count,avr in m:
            if item not in BH_list:
                continue
            if count>=threshold:
                _avr[item]={}
                _avr[item]['rating'] = avr
                _avr[item]['count'] = count
        return _avr
    
    def get_all_xuanxiu_BH(self):
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
        KCXZ = u'校选修课'.encode('utf-8')
        temp = ms.ExecQuery("SELECT BH FROM jxrwb2 where KCXZ='%s' and XN='2016-2017'"%KCXZ)
        BH_lst = []
        for row in temp:
            BH_lst.append(row[0])
        #print 12 in BH_lst
        return BH_lst

    def search_cou_info(self,start,n,XN,XQ):
        ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
        if XN=='2017-2018':
            cou_list=ms.ExecQuery("select KCMC,JSXM,SKSJ,SKDD,XF from dbo.[2017-2018-1-1] order by KCMC,SKSJ,JSXM,SKDD,XF")
        else:
            KCXZ = u'校选修课'.encode('utf-8')
            cou_list=ms.ExecQuery("select KCMC,JSXM,SKSJ,SKDD,XF from jxrwb where XQ =%d and XN='%s' and KCXZ='%s' order by KCMC,SKSJ,JSXM,SKDD,XF"%(XQ,XN,KCXZ))
        rec = []
        for line in cou_list[start:start+n]:
            if line:
                rec.append([line[0],line[1],line[2],line[3],line[4]])
        return rec

def search_user_info(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")
    m = ms.ExecQuery("select gra,maj,bind_id,COL_RATING from user_info where user_id =%d"%user_id)
    if m:
        if m[0][0]==None:
            gra = 0
        else:
            gra = m[0][0]
        if m[0][1]==None:
            maj = 0
        else:
            maj= ms.ExecQuery("SELECT ZYMC from [XKXX].[dbo].[maj_info] where ZYBH =%s"%m[0][1])
            maj = maj[0][0]
        if m[0][2]==None:
            bind_id =0
        else:
            bind_id = m[0][2]
        if m[0][3]==None:
            col_rating ='未填写'
        else:
            col_rating ='已填写'
        info_dic = {'grade':gra,'major':maj,'bind_id':bind_id,'col_rating':col_rating}
    else:
        info_dic = {}
    spare_time = col_spare_time.get_spare_time(user_id)
    info_dic['spare_time'] = spare_time
    dic = search_xuanxiu_num_XF(user_id)
    info_dic = dict(info_dic,**dic)
    return info_dic

def search_xuanxiu_num_XF(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="XKXX")
    KCXZ =u'校选修课'
    KCXZ = KCXZ.encode('utf-8')
    XH = str(get_XH(user_id))
    m = ms.ExecQuery("SELECT count(KCMC),sum(XF) FROM [XKXX].[dbo].[jxrwb2] as t1 join [XKXX].[dbo].[ZFXFZB_XKXXB_LH] as t2 on t1.XKKH=t2.XKKH where t2.XH='%s' and t1.KCXZ='%s'"%(XH,KCXZ))
    if m[0][0]:
        xuanxiu_num=m[0][0]
    else:
        xuanxiu_num='未找到数据'
    if m[0][1]!=None:
        xuanxiu_XF=m[0][1]
    else:
        xuanxiu_XF='未找到数据'
    dic = {'xuanxiu_num':xuanxiu_num,'xuanxiu_XF':xuanxiu_XF}
    return dic
def get_XH(user_id):
    ms = MSSQL(host="localhost",user="%s"%dbo_user,pwd="%s"%dbo_password,db="xuanke")  
    m = ms.ExecQuery("select bind_id from user_info where user_id = %d"%user_id)
    try:
        XH = m[0][0]
    except:
        XH = ''
    return XH
if __name__ == '__main__':
    #write_user_info('liuheng123')
    #maj_dic,sort = search_maj('001')
    #print sort[0][1]
    #gra,fac,maj = get_gra_fac_maj(1)
    #print search_fac()
    #print len(search_cou_dic(gra,maj))
    #get_item_sim(9)
    #get_bind_id(9)
    s = SEARCH()
    final_dic = s.maj_avr_rating()

    
        
        
