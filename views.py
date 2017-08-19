#-*-coding: utf-8 -*-
# default
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from account.decorators import login_required
from django import forms
from django.forms import fields
from django.forms import widgets

# added myself
import data_base
from info_search import search
from recommend import recommend
from XH_confirm import XH_confirm
from collect_info import col_rat
from collect_info import col_spare_time
from info_search import info_search

@login_required
def col_rating_new(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if 'close_help' in req.GET:
        data_base.close_help(user_id)
    # 绑定学号成功后提示成功success
    success = int(req.session.get('success',0))
    # 获得个人信息并创建网页信息字典
    dic = search.search_user_info(user_id)
    first_log_in = data_base.get_first_log_in_flag(user_id)
    print 'location_:col_rating_new__id_:01-01'
    if req.method == 'GET':
        dic1 = col_rat.get_cou_lst(user_id)
        dic = dict(dic,**dic1)
        print 'location_:col_rating_new__id_:01-02'
        if dic['lst']:
            if success:
                # 绑定学号成功后跳转到收集评分页面，同时记录收集评分开始的时间
                col_rat.set_col_time(user_id,'start')
                print 'location_:col_rating_new__id_:01-03'
                dic['success'] = '1'
                req.session['success'] = 0
            print 'location_:col_rating_new__id_:01-03-01'
            if first_log_in ==0:
                dic['first_log_in'] = 1
            return render(req,'info_collect/col_rat.html',dic,)
        else:
            # 记录收集评分结束的时间
            # 同时设置user_info中COL_RATING =1
            col_rat.set_col_time(user_id,'end')
            print 'location_:col_rating_new__id_:01-04'
            return HttpResponseRedirect('/online/spare_time')
    if req.method == 'POST':
        print 'location_:col_rating_new__id_:01-05'
        dic = col_rat.get_cou_lst(user_id)
        cou_lst = dic['lst']
        try:
            XN = dic['XN']
            XQ = dic['XQ']
            rat_lst = []
            d = dict(req.POST)
            print 'location_:col_rating_new__id_:01-06'
            for num,name,BH,jsxm in cou_lst:
                if str(BH) in d.keys():
                    rating = d[str(BH)]
                    rat_lst.append([BH,rating[0]])
            col_rat.write_into_data_base(user_id,rat_lst,XN,XQ)
            print 'location_:col_rating_new__id_:01-07'
            return HttpResponseRedirect('/online/col_rat')
        except:
            return HttpResponseRedirect('/online/col_rat')

@login_required
def user_cf(req):
    print 'location_:user_cf__id_:02'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if 'update_rating' in req.GET:
        col_rat.update_COL_RATING_delete(user_id)
        return HttpResponseRedirect('/online/col_rat')
    if 'close_help' in req.GET:
        data_base.close_help(user_id)
    first_log_in = data_base.get_first_log_in_flag(user_id)
    if req.method == 'GET':
        # 获取翻页信息
        if 'a' in req.GET:
            opt = req.GET.get('a')
        else:
            opt = 0
        # 获取详细课程信息
        if 'BH' in req.GET:
            BH = req.GET.get('BH')
        else:
            BH = 0
        # 获得个人信息并创建网页信息字典
        dic = search.search_user_info(user_id)
        print 'location_:user_cf__id_:02-01'
        if 'no_time_conflicit' in req.GET:
            flag = data_base.get_spare_time_flag(user_id)
            print 'location_:user_cf__id_:02-02'
            if flag ==0:
                dic['no_spare_time'] = 1
            else:
                rec = recommend.get_2016_2017_2_XXK(user_id)
                if rec:
                    dic['spare_time'] = 1
                    dic['rank'] = rec
                else:
                    dic['no_spare_time'] = 2
            return render(req,'info_search/no_time_conflicit.html',dic,)
        if BH:
            response = HttpResponseRedirect('/online/detail_BH=%s/'%BH)
            response.set_cookie('BH',BH)
            print 'location_:user_cf__id_:02-03'
            return response
        start = 0
        if opt:
            start = int(opt)
        rec = recommend.re_user_cf(start,user_id,10)
        print 'location_:user_cf__id_:02-04'
        if 'invalid_rating' in rec:
            dic['invalid_rating'] = 1
            if first_log_in==0:
                dic['first_log_in'] = 1
            return render(req,'recommend/tuijian.html',dic,)
        if 'less_than_standard' in rec :
            dic['error'] = 1
            dic['notworked'] = 1
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic['rank'] = rec
            print 'location_:user_cf__id_:02-05'
        elif rec:
            dic['rank'] = rec
            dic['worked'] = 1
        else:
            dic['error'] = 2
            dic['notworked'] =1
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic['rank'] = rec
            print 'location_:user_cf__id_:02-06'
        if first_log_in==0:
            dic['first_log_in'] = 1
        return render(req,'recommend/tuijian.html',dic,)
    else:
        return HttpResponseRedirect('/online/user_cf')

@login_required
def item_cf(req):
    print 'location_:item_cf__id_:03'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if 'close_help' in req.GET:
        data_base.close_help(user_id)
    first_log_in = data_base.get_first_log_in_flag(user_id)
    dic = search.search_user_info(user_id)
    if req.method == 'GET':
        if 'a' in req.GET:
            opt = req.GET.get('a')
        else:
            opt = 0
        if 'BH' in req.GET:
            BH = req.GET.get('BH')
        else:
            BH = 0
        # 获得个人信息并创建网页信息字典
        print 'location_:item_cf__id_:03-01'
        if 'no_time_conflicit' in req.GET:
            flag = data_base.get_spare_time_flag(user_id)
            print 'location_:user_cf__id_:02-02'
            if flag ==0:
                dic['no_spare_time'] = 1
            else:
                rec = recommend.get_2016_2017_2_XXK(user_id)
                if rec:
                    dic['spare_time'] = 1
                    dic['rank'] = rec
                else:
                    dic['no_spare_time'] = 2
            return render(req,'info_search/no_time_conflicit.html',dic,)
        if BH:
            response = HttpResponseRedirect('/online/detail_BH=%s/'%BH)
            response.set_cookie('BH',BH)
            print 'location_:item_cf__id_:03-03'
            return response
        start = 0
        if opt:
            start = int(opt)
        rec = recommend.re_item_cf(start,user_id,10)
        print 'location_:item_cf__id_:03-04'
        if 'invalid_rating' in rec:
            dic['invalid_rating'] = 1
            if first_log_in==0:
                dic['first_log_in'] = 1
            return render(req,'recommend/item_cf.html',dic,)
        if 'less_than_standard' in rec:
            dic['error'] = 1
            dic['notworked'] = 1
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic['rank'] = rec
            print 'location_:item_cf__id_:03-05'
        elif rec:
            dic['rank'] = rec
            dic['worked'] = 1
        else:
            dic['error'] = 2
            dic['notworked'] = 1
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic['rank'] = rec
        print 'location_:item_cf__id_:03-06'
        if first_log_in==0:
            dic['first_log_in'] = 1
        return render(req,'recommend/item_cf.html',dic,)
    else:
        return HttpResponseRedirect('/online/item_cf')        

@login_required
def lfm(req):
    print 'location_:lfm__id_:02'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if 'close_help' in req.GET:
        data_base.close_help(user_id)
    first_log_in = data_base.get_first_log_in_flag(user_id)
    if req.method == 'GET':
        # 获取翻页信息
        if 'a' in req.GET:
            opt = req.GET.get('a')
        else:
            opt = 0
        # 获取详细课程信息
        if 'BH' in req.GET:
            BH = req.GET.get('BH')
        else:
            BH = 0
        # 获得个人信息并创建网页信息字典
        dic = search.search_user_info(user_id)
        print 'location_:lfm__id_:02-01'
        if 'no_time_conflicit' in req.GET:
            flag = data_base.get_spare_time_flag(user_id)
            print 'location_:user_cf__id_:02-02'
            if flag ==0:
                dic['no_spare_time'] = 1
            else:
                rec = recommend.get_2016_2017_2_XXK(user_id)
                if rec:
                    dic['spare_time'] = 1
                    dic['rank'] = rec
                else:
                    dic['no_spare_time'] = 2
            return render(req,'info_search/no_time_conflicit.html',dic,)
        if BH:
            response = HttpResponseRedirect('/online/detail_BH=%s/'%BH)
            response.set_cookie('BH',BH)
            print 'location_:lfm__id_:02-03'
            return response
        start = 0
        if opt:
            start = int(opt)
        rec = recommend.re_lfm(start,user_id,10)
        print 'location_:lfm__id_:02-04'
        if 'invalid_rating' in rec:
            dic['invalid_rating'] = 1
            if first_log_in==0:
                dic['first_log_in'] = 1
            return render(req,'recommend/tuijian.html',dic,)
        if 'less_than_standard' in rec:
            dic['error'] = 1
            dic['notworked'] = 1
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic['rank'] = rec
            print 'location_:lfm__id_:02-05'
        elif rec:
            dic['rank'] = rec
            dic['worked'] = 1
        else:
            dic['error'] = 2
            dic['notworked'] =1
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic['rank'] = rec
            print 'location_:lfm__id_:02-06'
        if first_log_in==0:
            dic['first_log_in'] = 1
        return render(req,'recommend/tuijian.html',dic,)
    else:
        return HttpResponseRedirect('/online/lfm')
        
#********************************************************************
@login_required        
def base_info(req):
    print 'location_:base_info__id_:04'
    if req.method == 'GET':
        if 'a' in req.GET:
            opt = req.GET.get('a')
        else:
            opt = 0
        if 'BH' in req.GET:
            BH = req.GET.get('BH')
        else:
            BH = 0
        if BH:
            response = HttpResponseRedirect('/online/detail_BH=%s/'%BH)
            response.set_cookie('BH',BH)
            return response
        if opt:
            start = int(opt)
            s = search.SEARCH()
            rec = s.avr_rating(start,10)
            dic = {}
            dic['rank'] = rec
            print 'location_:base_info__id_:04-01'
            return render(req,'info_search/avr_rating.html',dic,)
        else:
            s = search.SEARCH()
            rec = s.avr_rating(0,10)
            dic = {}
            dic['rank'] = rec
            print 'location_:base_info__id_:04-02'
            return render(req,'info_search/avr_rating.html',dic,)
    else:
        print 'location_:base_info__id_:04-03'
        s = search.SEARCH()
        rec = s.avr_rating(0,10)
        dic = {}
        dic['rank'] = rec
        print 'location_:base_info__id_:04-04'
        return render(req,'info_search/avr_rating.html',dic,)
@login_required        
def avr_rating(req):
    print 'location_:avr_rating__id_:05'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    dic = search.search_user_info(user_id)
    if req.method == 'GET':
        print 'location_:avr_rating__id_:05-01'
        if 'maj_avr' in req.GET:
            result_dic = info_search.get_maj_avr(user_id, threshold=5)
            if result_dic['rank']==[]:
                dic['error']=1
            else:
                dic['maj_avr']=1
            dic['rank'] = result_dic['rank']
            dic['maj_name'] = result_dic['maj_name']
            return render(req,'info_search/avr_rating.html',dic,)
        if 'a' in req.GET:
            opt = req.GET.get('a')
        else:
            opt = 0
        if opt:
            start = int(opt)
            s = search.SEARCH()
            rec = s.avr_rating(start,50)
            if rec==[]:
                dic['error']=1
            else:
                dic['worked']=1
            dic['rank'] = rec
            print 'location_:avr_rating__id_:05-02'
            return render(req,'info_search/avr_rating.html',dic,)
        else:
            s = search.SEARCH()
            rec = s.avr_rating(0,50)
            if rec==[]:
                dic['error']=1
            else:
                dic['worked']=1
            dic['rank'] = rec
            print 'location_:avr_rating__id_:05-03'
            return render(req,'info_search/avr_rating.html',dic,)
    else:
        print 'location_:avr_rating__id_:05-04'
        s = search.SEARCH()
        rec = s.avr_rating(0,50)
        dic['rank'] = rec
        print 'location_:avr_rating__id_:05-05'
        return render(req,'info_search/avr_rating.html',dic,)
@login_required        
def cou_info(req):
    print 'location_:cou_info__id_:06'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    dic = search.search_user_info(user_id)
    if req.method == 'GET':
        print 'location_:cou_info__id_:06-01'
        if 'a' in req.GET:
            opt = req.GET.get('a')
        else:
            opt = 0
        if opt:
            XN = str(req.COOKIES['XN'])
            XQ = int(str(req.COOKIES['XQ']))
            start = int(opt)*30
            s = search.SEARCH()
            rec = s.search_cou_info(start,30,XN,XQ)
            dic['lst'] = rec
            print 'location_:cou_info__id_:06-02'
            return render(req,'info_search/cou_info.html',dic,)
        else:
            if 'XN' in req.GET:
                XN = req.GET.get('XN').encode('utf-8')
            else:
                XN = '2016-2017'
            if 'XQ' in req.GET:
                XQ = int(req.GET.get('XQ'))
            else:
                XQ = 2
            s = search.SEARCH()
            rec = s.search_cou_info(0,30,XN,XQ)
            print 'location_:cou_info__id_:06-03'
            dic['lst'] = rec
            response = render(req,'info_search/cou_info.html',dic,)
            response.set_cookie('XN',XN)
            response.set_cookie('XQ',XQ)
            print 'location_:cou_info__id_:06-04'
            return response
    else:
        
        if 'XN' in req.GET:
            XN = req.GET.get('XN').encode('utf-8')
        else:
            XN = '2016-2017'
        if 'XQ' in req.GET:
            XQ = int(req.GET.get('XQ'))
        else:
            XQ = 2
        s = search.SEARCH()
        rec = s.search_cou_info(0,30,XN,XQ)
        print 'location_:cou_info__id_:06-05'
        dic['lst'] = rec
        response = render(req,'info_search/cou_info.html',dic,)
        response.set_cookie('XN',XN)
        response.set_cookie('XQ',XQ)
        print 'location_:cou_info__id_:06-06'
        return response
    
@login_required
def spare_time(req):
    print 'location_:spare_time__id_:07'
    if req.method == 'GET':
        username = str(req.user)
        user_id = data_base.get_user_id(username)
        if 'close_help' in req.GET:
            data_base.close_help(user_id)
        flag_dic = data_base.get_user_info_flag(user_id)
        first_log_in = data_base.get_first_log_in_flag(user_id)
        dic = search.search_user_info(user_id)
        print 'location_:spare_time__id_:07-01'
        #if flag_dic['spare_time']:
            #return HttpResponseRedirect('/online/user_cf')
        if 'QK' in req.GET:
            print 'location_:spare_time__id_:07-02-01'
            QK = str(req.GET.get('QK'))
            if QK=='1':
                print 'location_:spare_time__id_:07-02-02'
                col_spare_time.delete_spare_time(user_id)
        time_lst = col_spare_time.get_spare_time(user_id)
        dic['error'] = 1
        dic['time_lst'] = time_lst
        print 'location_:spare_time__id_:07-03'
        if 'WC' in req.GET:
            print 'location_:spare_time__id_:07-04-01'
            return HttpResponseRedirect('/online/user_cf')
        print 'location_:spare_time__id_:07-05'
        if first_log_in==0:
            dic['first_log_in'] = 1 
        return render(req,'info_collect/spare_time_new.html',dic,)
    if req.method == 'POST':
        username = str(req.user)
        user_id = data_base.get_user_id(username)
        dic = req.POST
        col_spare_time.col_spare_time(user_id,dic)
        col_spare_time.write_user_info_flag(user_id)
        print 'location_:spare_time__id_:07-06'
        return HttpResponseRedirect('/online/spare_time')

@login_required
def bind_id(req):
    print 'location_:bind_id__id_:08'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if 'close_help' in req.GET:
        data_base.close_help(user_id)
    dic = {}
    if req.method == 'GET':
        print 'get in GET path'
        first_log_in = data_base.get_first_log_in_flag(user_id)
        print 'location_:bind_id__id_:08-00'
        flag_dic = data_base.get_user_info_flag(user_id)
        print 'location_:bind_id__id_:08-01'
        if flag_dic['bind_id']:
            print 'location_:bind_id__id_:08-02'
            return HttpResponseRedirect('/online/col_rat')
        if 'input' in req.GET:
            print 'location_:bind_id__id_:08-03'
            XH = str(req.GET.get('input'))
            if len(XH)!=10:
                print 'error_len(XH)!=10'
                dic['wrong_XH']=1
                return render(req,'bind_id.html',dic)
            result_dic= XH_confirm.get_cou_list(XH)
            lst = result_dic['result']
            confirm = result_dic['confirm']
            dic['cou_lst']=lst
            if first_log_in ==0:
                dic['first_log_in'] = 1
            response = render(req,'bind_id.html',dic)
            response.set_cookie('confirm',confirm)
            print 'location_:bind_id__id_:08-04'
            return response
        else:
            print 'location_:bind_id__id_:08-05'
            if first_log_in ==0:
                dic['first_log_in'] = 1
            return render(req,'bind_id.html',dic)
    else:
        print 'get_in_POST_path'
        post_dic = dict(req.POST)
        confirm = req.COOKIES['confirm']
        if 'select' in post_dic.keys():
            print 'location_:bind_id__id_:08-06'
            flag = XH_confirm.confirm(post_dic['select'],confirm)
        else:
            return HttpResponseRedirect('/online/bind_id')    
        print 'location_:bind_id__id_:08-07'
        if flag ==1:
            print 'location_:bind_id__id_:08-08'
            if 'input' in req.GET:
                print 'location_:bind_id__id_:08-09'
                bind_id = str(req.GET.get('input'))
            else:
                return HttpResponseRedirect('/online/bind_id')
            # 更新user_info表中绑定的学号
            data_base.update_bind_id(user_id,bind_id)
            print 'location_:bind_id__id_:08-09'
            # 初始化用户选课时间
            data_base.insert_xksj(user_id)
            print 'location_:bind_id__id_:08-10'
            req.session['success'] = 1
            # 初始化用户评分
            data_base.delete_rating(user_id)
            print 'location_:bind_id__id_:08-11'
            return HttpResponseRedirect('/online/col_rat')
        else:
            dic = {'error':'1'}
            print 'location_:bind_id__id_:08-12'
            return render(req,'bind_id.html',dic)
@login_required
def course_detail(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if req.method == 'GET':
        # 获得个人信息并创建网页信息字典
        dic = search.search_user_info(user_id)
        BH = int(req.COOKIES['BH'])
        lst = data_base.search_detail(BH)
        lst = sorted(lst,key=lambda t:t[4],reverse=True)
        dic['detail'] = lst
        return render(req,'detail.html',dic)
    else:
        dic = search.search_user_info(user_id)
        BH = int(req.COOKIES['BH'])
        lst = data_base.search_detail(BH)
        lst = sorted(lst,key=lambda t:t[4],reverse=True)
        dic['detail'] = lst
        return render(req,'detail.html',dic)
        
@login_required
def user_center(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    print 'location_:user_center__id_:09'
    if req.method == 'GET':
        print 'location_:user_center__id_:09-01-00'
        #update_bind_id = str(req.GET.get('update_bind_id'))
        #锁定绑定id,不可以更改绑定的学号
        update_bind_id = 0
        if 'update_rating' in req.GET:
            update_rating = str(req.GET.get('update_rating'))
        else:
            update_rating = 0
        if 'update_spare_time' in req.GET:
            update_spare_time = str(req.GET.get('update_spare_time'))
        else:
            update_spare_time = 0
        print 'location_:user_center__id_:09-01'
        if update_bind_id =='1':
            XH_confirm.delete_bind_id(user_id)
            print 'location_:user_center__id_:09-02'
            return HttpResponseRedirect('/online/bind_id')
        if update_rating =='1':
            col_rat.update_COL_RATING_delete(user_id)
            print 'location_:user_center__id_:09-03'
            return HttpResponseRedirect('/online/col_rat')
        if update_spare_time =='1':
            print 'location_:user_center__id_:09-04'
            return HttpResponseRedirect('/online/spare_time')
        flag_dic = data_base.get_user_info_flag(user_id)
        # 获得个人信息并创建网页信息字典
        dic = search.search_user_info(user_id)
        print 'location_:user_center__id_:09-05'
        return render(req,'user_center.html',dic)
    else:
        flag_dic = data_base.get_user_info_flag(user_id)
        dic = search.search_user_info(user_id)
        print 'location_:user_center__id_:09-06'
        return render(req,'user_center.html',dic)

@login_required
def online_admin(req):
    print 'location_:online_admin_id_:10'
    if req.method =='GET':
        username = str(req.user)
        user_id = data_base.get_user_id(username)
        if username=='admin':
            dic = info_search.user_info()
            dic['worked'] = 1
            return render(req,'online_admin.html',dic,)
        else:
            dic ={}
            dic['error'] = 1
            return render(req,'online_admin.html',dic,)
        
    else:
        return HttpResponseRedirect('/online/admin')
    
