# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
from raspcloud import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.login),
    url(r'^img/(?P<path>.*)$','django.views.static.serve',
        {'document_root':'/home/pi/RaspCloud/py/raspcloud/static/img/'}),
    url(r'^css/(?P<path>.*)$','django.views.static.serve',
        {'document_root':'/home/pi/RaspCloud/py/raspcloud/static/css/'}),
    url(r'^js/(?P<path>.*)$','django.views.static.serve',
        {'document_root':'/home/pi/RaspCloud/py/raspcloud/static/js/'}),
    url(r'^main/$',views.main),
    url(r'^main/uploadfile/$',views.uploadfile),
    url(r'^main/downloadurl/',views.get_downloadurl),
    url(r'^main/changecurrentdir/',views.change_current_dir),
    url(r'^main/logout/$',views.logout),
    url(r'^main/filelist/$',views.ret_file_list),
    url(r'^main/getcurrentpath/$',views.ret_current_path),
    url(r'^main/delete/',views.delete),
    url(r'^main/newdir/',views.new_dir),
    url(r'^main/backhome/$',views.backhome),
    url(r'^main/share/$',views.share),
    url(r'^main/sharefile/$',views.sharefile),
    url(r'^main/share/cancelshare/$',views.cancelshare),
    url(r'^main/share/downloadurl/$',views.share_downloadurl),
    url(r'^main/about/$',views.about),
    url(r'^main/chatroom/$',views.chatroom),
    url(r'^main/chatroom/chatinput/$',views.chatinput),
    url(r'^main/userinfo/$',views.userinfo),
    url(r'^main/userinfo/changepassword/$',views.changepassword),
    url(r'^main/userinfo/logout/$',views.logout),
    url(r'^main/offline/$',views.offline),
    url(r'^main/offline/dirindir/$',views.get_dir_in_dir),
    url(r'^main/offline/delofflinefile/$',views.del_offline_file),
    url(r'^main/message/$',views.message),
    url(r'^main/sendmessage/$',views.send_message),
)
