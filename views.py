#-*-coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from account.decorators import login_required
from django import forms
from django.forms import fields
from django.forms import widgets
import jiaowu
import data_base
from info_search import search
from recommend import recommend
from XH_confirm import XH_confirm
from django.core.mail import send_mail
from collect_info import col_rat
from collect_info import col_spare_time
from info_search import info_search

#表单
class UserForm(forms.Form): 
    username = forms.CharField(label='__用户名',max_length=100)
    password = forms.CharField(label='____密码',widget=forms.PasswordInput())
    #password_confirm = forms.CharField(label='确认密码',widget=forms.PasswordInput())
class UserForm1(forms.Form): 
    username = forms.CharField(label='__用户名',max_length=100)
    password = forms.CharField(label='____密码',widget=forms.PasswordInput())
    password_confirm = forms.CharField(label='确认密码',widget=forms.PasswordInput())
class UserForm3(forms.Form): 
    username = forms.CharField(label='__用户名',max_length=20)
    password = forms.CharField(label='____密码',widget=forms.PasswordInput())
    check_code = forms.CharField(label='__验证码',max_length=4)
class Collect_Form(forms.Form): 
    value1 = forms.CharField(label='年级序号',max_length=2)
    value2 = forms.CharField(label='院系序号',max_length=3)
class Collect_Form1(forms.Form): 
    value1 = forms.CharField(label='专业序号',max_length=3)
class Collect_Form2(forms.Form): 
    value1 = forms.CharField(label='课程评分',max_length=1)
    value2 = forms.CharField(label='课程评分',max_length=1)
    value3 = forms.CharField(label='课程评分',max_length=1)
    value4 = forms.CharField(label='课程评分',max_length=1)
    value5 = forms.CharField(label='课程评分',max_length=1)
class xuanke1(forms.Form):
    option = fields.ChoiceField(choices =(('user_cf', '基于用户推荐'), ('item_cf', '基于课程推荐'),),
        initial=2,
        widget=widgets.RadioSelect,
     )  


#登陆成功
@login_required
def index(req):
    #print req.user
    username = req.user
    xuanke = 'xuanke'
    return render(req,'index.html' ,{'username':username,'xuanke':xuanke})

@login_required
def pachong(req):
    if req.method == 'GET':
        uf = UserForm3()
        jiaowu.method_1()
        return render(req,'pachong.html',{'uf':uf},)
    if req.method == 'POST':
        uf = UserForm3(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            check_code = uf.cleaned_data['check_code']
            jiaowu.method_2(username,password,check_code)
            return render_to_response('kebiao/kebiao_%s.html'%str(username),)
@login_required
def col_fac(req):
    if req.user.is_authenticated():
        username = str(req.user)
    else:
        return HttpResponseRedirect('/')
    user_id = data_base.get_user_id(username)
    bind = data_base.get_bind_id(user_id)
    COL_GRA_MAJ = data_base.get_COL_GRA_MAJ(user_id)
    if req.method == 'GET':
        print bind
        if bind ==None:
            if COL_GRA_MAJ ==0:
                dic = {}
                fac_lst = data_base.search_fac()
                #dic = data_base.search_fac()
                dic.setdefault('lst',fac_lst)
                return render(req,'shouji.html',dic,)
            else:
                dic = {}
                fac_lst = data_base.search_fac()
                dic.setdefault('lst',fac_lst)
                dic.setdefault('error','您已填写过基础信息,无需重复填写。')
                return render(req,'shouji.html',dic,)
        else:
            return HttpResponseRedirect('/online/col_rat')
    if req.method == 'POST':
        gra = req.POST.get('gra')
        fac = req.POST.get('fac')
        data_base.user_info_update_gra_fac(user_id,str(gra),str(fac))
        return HttpResponseRedirect('/online/col_maj')
@login_required
def col_maj(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if req.method == 'GET':
        dic = {}
        gra,fac,maj = data_base.get_gra_fac_maj(user_id)
        maj_lst = data_base.search_maj(fac)
        dic.setdefault('lst',maj_lst)
        return render(req,'shouji1.html',dic,)
    if req.method == 'POST':
        maj = req.POST.get('maj')
        data_base.user_info_update_maj(user_id,maj)
        return HttpResponseRedirect('/online/xuanke')
@login_required
def col_rating(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    bind_id = data_base.get_bind_id(user_id)
    if req.method == 'GET':
        COL_RATING = data_base.get_COL_RATING(user_id)
        if COL_RATING == 0:
            dic = {}
            gra,fac,maj = data_base.get_gra_fac_maj(user_id)
            if bind_id ==None:
                cou_lst = data_base.search_cou_dic(gra,maj)
                dic['lst'] = cou_lst
            else:
                cou_lst = data_base.search_cou_bind_id(bind_id)
                dic['lst'] = cou_lst
            return render(req,'shouji2.html',dic,)
        else:
            dic = {}
            if bind_id ==None:
                gra,fac,maj = data_base.get_gra_fac_maj(user_id)
                cou_lst = data_base.search_cou_dic(gra,maj)
                dic.setdefault('error','您已经填写过评分信息 ！ 无需重复填写')
                dic.setdefault('lst',cou_lst)
            else:
                cou_lst = data_base.search_cou_bind_id(bind_id)
                dic.setdefault('error','您已经填写过评分信息 ！ 无需重复填写')
                dic.setdefault('lst',cou_lst)
            return render(req,'shouji2.html',dic,)
    if req.method == 'POST':
        #print req.POST
        if bind_id ==None:
            gra,fac,maj = data_base.get_gra_fac_maj(user_id)
            cou_lst = data_base.search_cou_dic(gra,maj)
            rat_lst = []
            for num,name,jsxx in cou_lst:
                d = dict(req.POST)
                select = d[num]
                xkkh = select[0]
                rating = select[1]
                rat_lst.append([xkkh,rating])
            #print rat_lst
            data_base.delete_rating(user_id)
            data_base.update_rating(user_id,rat_lst)
            return HttpResponseRedirect('/online/xuanke')
        else:
            cou_lst = data_base.search_cou_bind_id(bind_id)
            rat_lst = []
            for num,name,jsxx in cou_lst:
                d = dict(req.POST)
                select = d[num]
                xkkh = select[0]
                rating = select[1]
                rat_lst.append([xkkh,rating])
            #print rat_lst
            data_base.delete_rating(user_id)
            data_base.update_rating(user_id,rat_lst)
            return HttpResponseRedirect('/online/xuanke')
@login_required
def col_rating_new(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    # 绑定学号成功后提示成功success
    success = int(req.session.get('success',0))
    # 获得个人信息并创建网页信息字典
    dic = search.search_user_info(user_id)
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
def col_xuanxiu_rating(req):
    username = str(req.user)
    user_id = data_base.get_user_id(username)
    if req.method == 'GET':
        COL_RATING = data_base.get_COL_RATING(user_id)
        if COL_RATING == 0:
            dic = {}
            #年级未使用，待完善
            gra = 2
            maj = 999#选修课标识
            cou_lst = data_base.search_cou_dic(gra,999)
            dic.setdefault('lst',cou_lst)
            return render(req,'shouji3.html',dic,)
        else:
            dic = {}
            #年级未使用，待完善
            gra = 2
            maj = 999#选修课标识
            cou_lst = data_base.search_cou_dic(gra,999)
            dic.setdefault('error','您已经填写过评分信息 ！ 无需重复填写')
            dic.setdefault('lst',cou_lst)
            return render(req,'shouji3.html',dic,)
    if req.method == 'POST':
        #print req.POST
        gra = 2
        cou_lst = data_base.search_cou_dic(gra,999)
        rat_lst = []
        for num,name in cou_lst:
            rating = req.POST.get(num)
            rat_lst.append([num,rating])
        #print rat_lst
        data_base.update_rating(user_id,rat_lst)
        data_base.user_info_update_COL_RATING(user_id)
        return HttpResponseRedirect('/online/xuanke')
        
def muban(req):
    if req.method == 'GET':
        return render(req,'muban/index.html',)
@login_required  
def xuanke(req):
    if req.method == 'GET':
        username = str(req.user)
        user_id = data_base.get_user_id(username)
        # 获得个人信息并创建网页信息字典
        dic = search.search_user_info(user_id)
        success = int(req.session.get('success',0))
        if success:
            dic['success'] = '1'
            req.session['success'] = 0
            return render(req,'index3.html',dic,)
        else:
            return render(req,'index3.html',dic,)

@login_required
def user_cf(req):
    print 'location_:user_cf__id_:02'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
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
        no_time_conflicit =req.GET.get('no_time_conflicit')
        dic = search.search_user_info(user_id)
        print 'location_:user_cf__id_:02-01'
        if no_time_conflicit:
            rec = recommend.get_2016_2017_2_XXK(user_id)
            dic['rank'] = rec
            print 'location_:user_cf__id_:02-02'
            flag = data_base.get_spare_time_flag(user_id)
            if flag ==0:
                dic['no_spare_time'] = 1
            else:
                dic['spare_time'] = 1
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
        if rec =='less_than_standard' :
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
        return render(req,'recommend/tuijian.html',dic,)
    else:
        return HttpResponseRedirect('/online/user_cf')
@login_required
def item_cf(req):
    print 'location_:item_cf__id_:03'
    username = str(req.user)
    user_id = data_base.get_user_id(username)
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
        no_time_conflicit =req.GET.get('no_time_conflicit')
        print 'location_:item_cf__id_:03-01'
        if no_time_conflicit:
            rec = recommend.get_2016_2017_2_XXK(user_id)
            dic['rank'] = rec
            print 'location_:item_cf__id_:03-02'
            flag = data_base.get_spare_time_flag(user_id)
            if flag ==0:
                dic['no_spare_time'] = 1
            else:
                dic['spare_time'] = 1
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
        if rec =='less_than_standard' :
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
        return render(req,'recommend/item_cf.html',dic,)
    else:
        return HttpResponseRedirect('/online/item_cf')        
        
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
        flag_dic = data_base.get_user_info_flag(user_id)
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
    if req.method == 'GET':
        print 'get in GET path'
        # 获得个人信息并创建网页信息字典
        dic = search.search_user_info(user_id)
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
            response = render(req,'bind_id.html',dic)
            response.set_cookie('confirm',confirm)
            print 'location_:bind_id__id_:08-04'
            return response
        else:
            print 'location_:bind_id__id_:08-05'
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
    
