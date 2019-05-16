from django.shortcuts import render
from django import forms
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse,HttpResponseRedirect
from web01.models import User,Problem,Course_Python,Level_list,Level,OnlineTime,Progress,User_Problem
import os
import time
from django.db.models import Avg,Count,Sum
from web01 import user_portrait,censor

class UserForm(forms.Form):
    userid = forms.CharField(widget=forms.TextInput({'placeholder':'用户名',}),label='')
    passwd = forms.CharField(widget=forms.PasswordInput({'placeholder':'密码',}),label='')
    passwd1 = forms.CharField(widget=forms.PasswordInput({'placeholder':'确认密码',}),label='')
    eamin = forms.EmailField(widget=forms.EmailInput({'placeholder':'邮箱',}),label='')


class UserForm_login(forms.Form):
    userid = forms.CharField(widget=forms.TextInput({'placeholder':'用户名',}),label='')
    passwd = forms.CharField(widget=forms.PasswordInput({'placeholder':'密码',}),label='')


def home(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        #调用函数返回当天总学习时间
        sum_time = user_portrait.select_today_sum_times(userid)
        return render(request,'home.html',locals())
    return render(request,'index.html')


def index(request):
    return render(request,'index.html',locals())

def register(request):
    if request.method == 'POST':
        rg = UserForm(request.POST)
        if rg.is_valid():
            if rg.cleaned_data['passwd'] != rg.cleaned_data['passwd1']:
                msg = '两次密码输入不一致！'
                return render(request,'register.html',locals())
            else:
                userid = rg.cleaned_data['userid']
                passwd = rg.cleaned_data['passwd']
            try:
                User.objects.get(user_id=userid)
                msg = '此用户名已被注册！'
                return render(request,'register.html',locals())
            except:
                u = User()
                u.user_id = userid
                u.user_passwd = passwd
                u.save()
                #将用户注册时间存入user表
                user_portrait.insert_register_time(userid)
                #登录进去还是login的原因是，这个post请求是交给login本页面处理的，如果放到home页面就可以了
                return HttpResponseRedirect('/login/')
    else:
        rg = UserForm()
        return render(request,'register.html',locals())

def login(req):
    if req.method == 'POST':
        log = UserForm_login(req.POST)
        if log.is_valid():
            userid = log.cleaned_data['userid']
            passwd = log.cleaned_data['passwd']
            try:
                user = User.objects.get(user_id=userid)
                if user.user_passwd == passwd:
                    req.session['userid'] = userid
                    req.session['start_time'] = 0  # 创建session，将开始时间设置为0，表示还没有进行学习
                    req.session.set_expiry(0)
                    #如果上次登录日期不是今天，总在线天数+1
                    if user.last_online_day != time.strftime("%Y-%m-%d", time.localtime()):
                        user.online_days += 1
                        user.save()
                    return render(req, 'learn.html', locals())
                else:
                    msg = '密码错误！'
                    return render(req, 'login.html', locals())
            except:
                msg = '该用户名未注册！'
                return render(req, 'login.html', locals())
    else:
        log = UserForm_login()
        return render(req,'login.html',locals())

def logout(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        #退出的时候将当前时间设置为上次登录时间
        user = User.objects.get(user_id=userid)
        user.last_online_day = time.strftime("%Y-%m-%d", time.localtime())
        user.save()
        try:
            del request.session['userid']
            del request.session['start_time']
            return render(request,'index.html')
        except:
            return redirect(reverse('login'))
    return redirect(reverse('index'))

def learn(request):
    if 'userid' in request.session:
        userid = request.session['userid']

        # 当离开学习页面时，如果session里面的start_time为0，这说明是从其他页面过来的，不做任何
        # 操作，否则，是从学习页面过来的，就应该记录当前时间，然后减去session里面的start_time，得出分钟数，然后存入数据库
        if request.session.get('start_time') != 0:
            mintues = user_portrait.stop_time(request)

            #将mintues存入用户表的总时间字段,调用update_sum_time,将mintues当做参数传入函数
            user_portrait.update_sum_time(userid,mintues)
            user_portrait.create_one_record_to_OnlineTime(request,userid,mintues)

        # 这部分是当视频看完之后提交完成按钮，将该章节和用户以及看完视频存入Progress进度数据表
        if request.method == 'POST':
            user_portrait.create_one_record_to_Progress(request,userid)

        li,progress = user_portrait.update_user_progress(userid)

        course = Course_Python.objects.all()
        return render(request,'learn.html',locals())

def note(request):
    if 'userid' in request.session:
        userid = request.session['userid']

        note = Level_list.objects.all()
        level = Level.objects.all()
        L1 = level[0]
        L2 = level[1]
        L3 = level[2]
        level_1 = Level_list.objects.filter(level__level_name__contains='基础')
        level_2 = Level_list.objects.filter(level__level_name__contains='对象')
        level_3 = Level_list.objects.filter(level__level_name__contains='实战')
        l_len = len(level)
        return render(request,'note.html',locals())

def noteinfo(request, id):
    if 'userid' in request.session:
        userid = request.session['userid']

        level_html =Level_list.objects.get(id=id)
        # 然后在这里返回该html的地址--------------------------------------------------------------------------------------------------
        return render(request, 'noteinfo.html', locals())

def problem(request):
    if 'userid' in request.session:
        userid = request.session['userid']

        pros = Problem.objects.all()#获取所有题目数据
        pros_len = len(pros)
        return render(request, 'problem.html', locals())

def probleminfo(request,id):
    if 'userid' in request.session:
        userid = request.session['userid']
    pro = Problem.objects.get(id=id)#返回单个题的数据信息用来显示该id的信息
    pros = Problem.objects.all()#返回所有题目，用来显示列表
    pros_len = len(pros)

    if request.method == 'POST':
        if 'run' in request.POST:#如果点击的是运行，则只将结果编译出来就好
            answer,error = user_portrait.run_code(request)
            if answer and error:
                answer_error = []
                answer_error.append(answer)
                answer_error.append('\n')
                answer_error.append(error)
                return HttpResponse(answer_error)
            elif answer:
                return HttpResponse(answer)
            else:
                return HttpResponse(error)
        if 'submit' in request.POST:
            return HttpResponse('正在提交')
    else:
        return render(request, 'probleminfo.html',locals())
    
    update_correct(request,id)
    update_dones(request)
    update_right_censor(request)


def total(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        user_portrait.update_current_time(userid)
        user_portrait.update_focus(userid)
        user = User.objects.get(user_id=userid)
        rankking_progress, rankking_sum_time, rankking_online_days, rankking_accuracy,rankking_focus, rankking_register_time = user_portrait.rank(userid)
        return render(request,'total.html',locals())


def learninfo(request,id):
    # 在进入学习页面的时候将当前时间存入session
    request.session['start_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    course = Course_Python.objects.get(id=id)
    return render(request, 'video.html',{'range_video': range(course.video), 'range_ppt': range(course.ppt), 'course': course})

