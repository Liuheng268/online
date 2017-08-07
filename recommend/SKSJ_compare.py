# -*- coding: utf-8 -*-
# 此代码目的：课程时间转换
# 此代码需要调用的变量形式或文件类型如下：
#    
#    
# 此代码归属模块：推荐模块



def time_convert(time):
    # 将数据库中上课时间转换成可以计算比较的结构
    # XQ：星期
    # SJBH:课程时间编号,例如，1,2（节）
    # WEEK:上课周数，例如，1-16（周）
    lst = []
    s = time.split(';')
    for row in s:
        if not row:
            continue
        spt = row.split(u'第')
        spt2 = spt[2].split(u'周')
        WEEK = spt2[0]
        XQ = spt[0]
        spt = spt[1].split(u'节')
        SJBH = spt[0]
        lst.append([XQ,SJBH,WEEK])
    return lst
    
def whether_conflict(t1,t2):
    # 判断两个上课时间t1,t2是否覆盖重复时段
    # flag 返回值为 0：不重复 或 1：重复
    flag = 0
    for time in t1:
        for time2 in t2:
            if time[0] == time2[0]:
                if time[1] == time2[1]:
                    spt = time[2].split('-')
                    l1 = int(spt[0])
                    h1 = int(spt[1])
                    spt2 = time2[2].split('-')
                    l2 = int(spt2[0])
                    h2 = int(spt2[1])
                    if h1>h2:
                        if h2>=l1:
                            flag = 1
                        else:
                            pass
                    else:
                        if h1>=l2:
                            flag = 1
                        else:
                            pass                            
                else:
                    pass
            else:
                pass
            
    
    return flag

def whether_contain(t1,t2):
    # 判断两个上课时间t1,t2是否存在t1包含t2的情况
    # flag 返回值为 0：不包含 或 1：包含
    flag = 0
    for time in t1:
        for time2 in t2:
            if time[0] == time2[0]:
                if time[1] == time2[1]:
                    spt = time[2].split('-')
                    l1 = int(spt[0])
                    h1 = int(spt[1])
                    spt2 = time2[2].split('-')
                    l2 = int(spt2[0])
                    h2 = int(spt2[1])
                    if h1>=h2:
                        if l2>=l1:
                            flag = 1
                        else:
                            pass
                    else:
                        pass                         
                else:
                    pass
            else:
                pass
    return flag

def judge_conflicit(time1,time2):
    #flag是判断标志，0表示没有冲突，1表示有冲突
    t1 = time_convert(time1)
    t2 = time_convert(time2)
    flag = whether_conflict(t1,t2)
    return flag

def judge_contain(time1,time2):
    #flag是判断标志，0表示time1包含time2，1表示time1不包含time2
    t1 = time_convert(time1)
    t2 = time_convert(time2)
    flag = whether_contain(t1,t2)
    return flag

if __name__ == '__main__':
    #time1 = u'周一第1,2节{第1-16周};周四第1,2节{第3-5周}'
    #time2 = u'周一第1,2节{第7-10周};周三第1,2节{第6-10周}'
    #flag = judge_conflicit(time1,time2)
    time1 = u'周一第1,2节{第1-16周}'
    time2 = u'周一第1,2节{第1-15周}'
    flag = judge_contain(time1,time2)
    
    print flag
