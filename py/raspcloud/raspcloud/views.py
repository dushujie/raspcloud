# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.contrib.auth.models import User
from userdb.models import userinfo,fileshared,chatroomitem
from shutil import rmtree
from file import rasp_file
from mail import mail
import time,os,ctypes,socket,fcntl,struct 

user_file_map={}
def get_ip_address(ifname): 
    #获取本机IP地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
                s.fileno(), 
                0x8915, # SIOCGIFADDR 
                struct.pack('256s', ifname[:15]) 
                )[20:24]) 

local_ip = get_ip_address('eth0')

def getdirsize(dir):
    #获取目录大小
    size = 0L
    for root, dirs, files in os.walk(dir):
        size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
    return size

class file_list_item:
    def __init__(self, filename = ''):
        self.filename=filename
        self.filesize=''
        self.changetime=''
        self.kind=''

class shared_file_item:
    def __init__(self):
        self.user = ''
        self.filename = ''
        self.path = ''

class chat_item:
    def __init__(self):
        self.user = ''
        self.content = ''
        self.time = ''

def login(request):
    return render_to_response('login.html')

def logout(request):
    auth.logout(request)
    if request.session.has_key('username'):
        del request.session['username']
    return HttpResponse('Logout seccessfully!')

def main(request):
    if request.POST.has_key("usernameinput"):
        name = request.POST['usernameinput']
        passwd = request.POST['passwordinput']
        user = auth.authenticate(username=name,password=passwd)

        if user is None:
            return HttpResponse("用户名或密码错误！")
        else:
            auth.login(request,user)
            request.session['username'] = name
            user_file_map[name] = rasp_file('/cloud/' + name +'/')

    if request.user.is_authenticated():
        name = request.session['username']
        user_file_map[name] = rasp_file('/cloud/' + name +'/')
        file_list=get_file_list(name)
        return render_to_response('main.html',{'current_path':user_file_map[name].get_dir(), 'info':file_list})

    else:
        return login(request)

def get_file_list(name):
    tmp_list = user_file_map[name].list_file().split('\n')
    tmp_list = tmp_list[:-1]
    tmp_list.sort()
    file_list=[]
    for i in tmp_list:
        t=file_list_item(i.split('\t')[0])
        s = user_file_map[name].get_file_size(t.filename)
        times = 0
        times_arr = ['Byte','KB','MB','GB']
        while s > 1024:
            s /= 1024
            times += 1
        t.filesize=str(s)+times_arr[times]
        ctime=user_file_map[name].get_file_change_time(t.filename)
        ctime += (8*60*60)
        x=time.localtime(ctime)
        t.changetime=time.strftime('%Y-%m-%d %H:%M:%S',x)

        if i.split('\t')[1] == 'dir':
            t.kind='文件夹'
            t.filesize = ''
        else:
            t.kind='文件'
        file_list.append(t)
    return file_list

#上传处理部分    
@csrf_exempt
def uploadfile(request):
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    ret="0"
    file = request.FILES.get("Filedata",None)
    if file:
        result,new_name=profile_upload(file,request)
        if result:
            ret="1"
        else:
            ret="2"                    
    json={'ret':ret,'save_name':new_name}
    return HttpResponse(simplejson.dumps(json,ensure_ascii = False))

@csrf_exempt
def profile_upload(file,request):
    if file:
        name = request.session['username']
        path = user_file_map[name].get_dir()
        path=os.path.join(path,'')
        file_name=file.name
        path_file=os.path.join(path,file_name)
        fp = open(path_file, 'wb')
        for content in file.chunks(): 
            fp.write(content)
        fp.close()
        return (True,file_name) #change
    return (False,file_name)   #change
@csrf_exempt
#用户管理-添加用户-删除附件
def profile_delte(request):
    del_file=request.POST.get("delete_file",'')
    if del_file:
        path_file=os.path.join(settings.MEDIA_ROOT,'upload',del_file)
        os.remove(path_file)

#上传处理部分结束
def get_downloadurl(request):
    #获得下载地址
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    request.encoding = 'gb2312'
    p = request.path
    p.encode('utf-8')
    filename = p.split('/')[-1]
    p = user_file_map[name].get_dir()
    for i in range(1,len(p)-1):
        if p[i] == '/':
            p = p[i:]
            break

    return HttpResponse(local_ip + ':8001' + p + filename)

def change_current_dir(request):
    #更改当前路径
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    t = request.path
    dirname = t.split('/')[-1]
    if dirname == 'parentdir':
        user_file_map[name].exit_dir()
    else:
        path = user_file_map[name].get_dir() + str(dirname) + '/'
        if os.path.isdir(path):
            user_file_map[name].set_dir(path)
    return ret_file_list(request)

def ret_file_list(request):
    #返回文件列表
    ret = "<tr>\n<th width='50px'><a id='selectall' style='cursor:pointer;'>全选</a></th>\n<th>文件名</th>\n<th>类型</th>\n<th>大小</th>\n<th>修改时间</th>\n</tr>"
    if request.user.is_authenticated():
        name = request.session['username']
        fl = get_file_list(name)
        for i in fl:
            ret = ret + '<tr><td><input type="checkbox" value="' + i.filename + \
                '"></td>\n<td><a href="#" style="color: #EEE" filename="' + i.filename \
                + '">' + i.filename + '</a></td>\n<td>' + i.kind + '</td>\n' + '<td>' 
            if i.filesize == 0:
                ret += '</td>\n'
            else:
                ret = ret + str(i.filesize) + '</td>\n'

            ret = ret + '<td>' + i.changetime + '</td><tr>\n'

    return HttpResponse(ret)

def ret_current_path(request):
    #返回当前路径
    if request.user.is_authenticated():
        name = request.session['username']
        return HttpResponse(u'当前路径:' + user_file_map[name].get_dir())
    else:return HttpResponse('Please login first.')

def delete(request):
    #删除
    if request.user.is_authenticated():
        name = request.session['username']
        path = user_file_map[name].get_dir()
        request.encoding = 'gb2312'
        p = request.path
        p.encode('utf-8')
        p = p.split("/")[-1]
        p = p.split(",")
        for i in p:
            t = path + i
            if os.path.isdir(t):
                rmtree(t,True)
            else:
                os.remove(t)
        return HttpResponse('1')
    else:return HttpResponse('Please login first.')

def new_dir(request):
    #创建新文件夹
    if request.user.is_authenticated():
        name = request.session['username']
        dir_name = request.POST['dirname']
        re = user_file_map[name].new_dir(dir_name)
        return HttpResponse(str(re))
    else:return HttpResponse('Please login first.')

def backhome(request):
    #返回初始页面
    if request.user.is_authenticated():
        name = request.session['username']
        user_file_map[name].set_dir('/cloud/' + name +'/')
        return HttpResponse('1')
    else:return HttpResponse('Please login first.')

def sharefile(request):
    #处理要分享的文件列表
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    file = []
    for i in request.POST:
        file.append(request.POST[i])
    name = request.session['username']
    for i in file:
        for n in fileshared.objects.filter(filename = i,user = name,path = user_file_map[name].get_dir()):
            n.delete()
        t = fileshared(filename = i,path = user_file_map[name].get_dir(),user = name)
        t.save()
    return HttpResponse("1")

def share(request):
    #文件分享页面
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    list = fileshared.objects.all()
    shared_file_list = []
    for i in list:
        t = shared_file_item()
        t.filename = i.filename
        t.user = i.user
        t.path = i.path
        shared_file_list.append(t)
    return render_to_response('share.html',{'sharelist':shared_file_list,'username':name})

def cancelshare(request):
    #取消分享
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    filename = request.POST['filename']
    path = request.POST['path']
    t = fileshared.objects.filter(user = name,filename = filename,path = path)
    if len(t) == 0:return HttpResponse("failed")
    for i in t:
        i.delete()
    return HttpResponse(u'取消成功！')

def share_downloadurl(request):
    #分享文件的下载连接
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    filename = request.POST['filename']
    path = request.POST['path']
    for i in range(1,len(path)-1):
        if path[i] == '/':
            path = path[i:]
            break

    return HttpResponse(local_ip + ':8001' + path + filename)


def about(request):
    #返回关于信息
    return render_to_response('about.html')

def chatroom(request):
    #进入聊天室
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    chat = chatroomitem.objects.order_by("-time")[0:10]
    chat_list = []
    for i in chat:
        t = chat_item()
        t.user = i.user
        t.content = i.content
        t.time = i.time
        chat_list.append(t)
    return render_to_response('chatroom.html',{'chatlist':chat_list})

def chatinput(request):
    #保存用户的信息
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    t = time.strftime('%Y-%m-%d,%H:%M:%S %a',time.localtime(time.time()+8*3600))
    tmp = chatroomitem(content = request.POST['text'], user = name, time = t)
    tmp.save()
    return HttpResponse('success')

def userinfo(request):
    #返回用户基本信息
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    room = getdirsize('/cloud/' + name)
    times = 0
    times_arr = ['Byte','KB','MB','GB']
    while room > 1024:
        room /= 1024
        times += 1
    room = str(room) + times_arr[times]
    return render_to_response('userinfo.html',{'username':name,"room_used":room})

def changepassword(request):
    #更新密码
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    orig_pwd = request.POST['orig_pwd']
    new_pwd = request.POST['new_pwd']
    user = auth.authenticate(username=name,password=orig_pwd)

    if user is None:
        return HttpResponse(u"原密码错误！")
    else:
        user = User.objects.get(username=name)
        user.set_password(new_pwd)
        user.save()
        return HttpResponse(u'修改成功')

def offline(request):
    #离线下载页面
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    if name != 'xiadong':
        return HttpResponse('Not Administrator.')
    file_list = get_file_list(name)
    first_file_list = []
    for i in file_list:
        if i.kind == "文件" or i.filename == '.':
            continue
        if i.filename == '..':
            i.filename = u'上一级'
        first_file_list.append(i)

    return render_to_response('offline.html',{'username':user_file_map[name].get_dir(),'first_file_list':first_file_list})

def get_dir_in_dir(request):
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']

    if name != 'xiadong':
        return HttpResponse('Not Administrator.')

    dir = request.POST['dir']
    path = user_file_map[name].get_dir() + dir + '/'
    if dir == u'上一级':
        user_file_map[name].exit_dir()
    elif os.path.isdir(path):
        user_file_map[name].set_dir(path)

    file_list = get_file_list(name)
    ret = ''
    for i in file_list:
        if i.kind == "文件" or i.filename == '.':
            continue
        if i.filename == '..':
            i.filename = u'上一级'  
        ret = ret + i.filename + '\n'

    return HttpResponse(ret)

def del_offline_file(request):
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    if name != 'xiadong':
        return HttpResponse('Not Administrator.')

    name = request.session['username']
    path = request.POST['path']
    filename = request.POST['filename']
    if os.path.isdir(path):
        os.remove(os.path.join(path,filename))
        os.remove(path+filename+'.aria2')
    return HttpResponse('OK')

def message(request):
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    name = request.session['username']
    return render_to_response('message.html')

def send_message(request):
    if not request.user.is_authenticated():
        return HttpResponse('Please login first.')
    username = request.session['username']
    name = request.POST['name']
    email = request.POST['email']
    msg = request.POST['message']

    content = 'Name:'+name+'\nE-mail:'+email+'\nContent:'+msg
    mail('xiadong1994@126.com',content)
    return HttpResponse(u"感谢您的反馈！")
