"""mysite5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from online import views
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
    #url(r'^pachong/$',views.pachong,name = 'pachong'),
    url(r'^$',views.bind_id,name = 'bind_id'),
    url(r'^col_rat/$',views.col_rating_new,name = 'col_rat'),
    url(r'^user_cf/$',views.user_cf,name = 'user_cf'),
    url(r'^item_cf/$',views.item_cf,name = 'item_cf'),
    url(r'^lfm/$',views.lfm,name = 'lfm'),
    url(r'^base_info/$',views.base_info,name = 'base'),
    url(r'^avr_rating/$',views.avr_rating,name = 'avr_rating'),
    url(r'^cou_info/$',views.cou_info,name = 'cou_info'),
    url(r'^spare_time/$',views.spare_time,name = 'spare'),
    url(r'^bind_id/$',views.bind_id,name = 'bind_id'),
    url(r'^detail.*/$',views.course_detail,name = 'detail'),
    url(r'^user_center/$',views.user_center,name = 'user_center'),
    url(r'^online_admin/$',views.online_admin,name = 'online_admin'),
    
    
    
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
