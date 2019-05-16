from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from web01.models import User,Problem,Course_Python,Level_list,Level,OnlineTime,Progress,User_Problem
import time,datetime
from django.db.models import Avg,Count,Sum
import os


#------------------------------------------------------这些函数基本都是在调用学习统计页面时调用---------------------

def update_user_progress(userid):
    '''将进度更新到user表中，并得到该用户看过的章节，用li存储,返回li,进度，之后不需要再当前页面显示进度时可以不要进度'''
    user = User.objects.get(user_id=userid)
    status = Progress.objects.filter(user=user,learned=True)
    li = []
    for i in status:
        li.append(i.chapter.id)
    sc_list = Course_Python.objects.all()  # 做这一步是想得到章节的个数
    se = set(li)
    progress = len(se) / len(sc_list) * 100
    user = User.objects.get(user_id=userid)
    user.user_progress = progress
    user.save()
    return li,progress

def update_focus(userid):
    """
       计算时间差
       :param time1: 较小的时间（datetime类型）
       :param time2: 较大的时间（datetime类型）
       :param type: 返回结果的时间类型（暂时就是返回相差天数）
       :return: 相差的天数
       """
    user = User.objects.get(user_id=userid)
    #user.register_time =  datetime.datetime.now().strftime('%Y-%m-%d')  格式
    day1 =  time.strptime(str(user.register_time), '%Y-%m-%d')
    day2 = time.strptime(str(user.current_time), '%Y-%m-%d')
    day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60)
    # 防止今天刚注册，那么今天-注册天=0，分母不能为0，所以如果今天刚注册，则专注度为1.0,加1是因为今天减昨天为1
    # 但是在线了两天，不加1，专注度就为2/1=2了，不符逻辑
    if abs(int(day_num)) > 0:
        user.focus = user.online_days / abs(int(day_num)+1) * 100
    else:
        user.focus = 100
    user.save()
    #总的在线天数/（注册时间-当前登陆时间）= 专注度

def insert_register_time(userid):
    user = User.objects.get(user_id=userid)
    user.register_time = datetime.datetime.now().strftime('%Y-%m-%d')
    user.save()

def update_current_time(userid):
    '''获取当前时间，在调用学习统计页面时执行'''
    user = User.objects.get(user_id=userid)
    user.current_time = datetime.datetime.now().strftime('%Y-%m-%d')
    user.save()

def update_sum_time(userid,today_online_time):#在learn函数里面调用，更新user的总学习时长
    user = User.objects.get(user_id=userid)
    user.sum_time += today_online_time
    user.save()

def update_accuracy(userid):
    pass

# def update_online_days(user):#在登录的时候调用,并且在登录时判断上次登录的日期是否是今天
#     '''统计一共在线的天数'''
#     user.online_days += 1
#     user.save()

def select_today_sum_times(userid):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user = User.objects.get(user_id=userid)
    online = OnlineTime.objects.filter(today=list(current_time.split(' '))[0], user=user).aggregate(Sum('online_time'))
    sum_time = online['online_time__sum']
    if not sum_time:
       sum_time = 0
    return sum_time

def stop_time(request):
    '''停止计时，并把时间加入OnlineTime表中'''
    end_time = list(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split('-')[2].split(' ')[1].split(':'))
    start_time = list(request.session.get('start_time').split('-')[2].split(' ')[1].split(':'))
    start_time[0] = int(start_time[0])
    start_time[1] = int(start_time[1])

    end_time[0] = int(end_time[0])
    end_time[1] = int(end_time[1])

    h, m = 0, 0
    if start_time[0] == end_time[0]:
        h = 0
        if start_time[1] == end_time[1]:
            m = 0
        else:
            m = end_time[1] - start_time[1]
    else:
        h = end_time[0] - start_time[0]
        if start_time[1] == end_time[1]:
            m = 0
        else:
            m = end_time[1] - start_time[1]
    mintues = h * 60 + m
    return mintues

def create_one_record_to_OnlineTime(request,userid,mintues):
    '''向OnlineTime表中插入一条记录，表示这次学习的记录，包括日期2019-4-28，学习分钟数mintues,用户名'''
    user = User.objects.get(user_id=userid)
    online = OnlineTime.objects.create(online_time=mintues, user=user)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    online.today = list(current_time.split(' '))[0]
    online.save()
    request.session['start_time'] = 0

def create_one_record_to_Progress(request,userid):
    '''向Progress表中插入一条记录，表示这次学习进度的记录，包括是否看完True，看完的是哪一章节,用户名'''
    finish_or_unfinish = request.POST.get('data')  # 隐藏表单域的值，都是True
    chapter_data = request.POST.get('chapter_data')  # 当前看的视频所属的章节的id,是从视频播放页面传回来的

    # 取出课表中章节id为传回来的值的章节对象，因为外键关系，我们进度表中存储的章节字段的值必须是一个对象
    chapter = Course_Python.objects.get(id=chapter_data)
    user = User.objects.get(user_id=userid)  # 效果同上

    # 向进度表中添加数据，内容包括是否学完的值为True,看完的是哪个章节，看这个视频的哪个用户
    progress = Progress.objects.create(learned=finish_or_unfinish, user=user,chapter=chapter)
    progress.save()

def run_code(request):
    '''run代码，返回对和错的结果'''
    code = request.POST['textarea']
    f = open('code.py', 'w', encoding='utf-8')
    model = "import sys\n" \
            "import os\n" \
            "stdout = open('stdout.txt','w',encoding='utf-8')\n" \
            "stderr = open('stderr.txt','w',encoding='utf-8')\n" \
            "sys.stdout = stdout\n" \
            "sys.stderr = stderr\n" \
            + code + \
            "\nstdout.close()\n" \
            "stderr.close()\n" \
        # "os.system('code.py')\n"
    f.write(model)
    f.close()
    com = 'python "code.py"'
    os.system(com)
    f_out = open('stdout.txt', 'r', encoding='utf-8')
    f_err = open('stderr.txt', 'r', encoding='utf-8')
    answer = f_out.read()
    error = f_err.read()
    f_out.close()
    f_err.close()
    return answer,error

def rank(userid):
    user = User.objects.get(user_id=userid)
    rankking_progress = list(User.objects.order_by('-user_progress')).index(user) + 1
    rankking_sum_time = list(User.objects.order_by('-sum_time')).index(user) + 1
    rankking_online_days = list(User.objects.order_by('-online_days')).index(user) + 1
    rankking_accuracy = list(User.objects.order_by('-accuracy')).index(user) + 1
    rankking_focus = list(User.objects.order_by('-focus')).index(user) + 1
    rankking_register_time = list(User.objects.order_by('register_time')).index(user) + 1
    return rankking_progress,rankking_sum_time,rankking_online_days,rankking_accuracy,rankking_focus,rankking_register_time

def get_test_info(userid,id):
    '''在提交的时候调用，将该用户对这个题目的信息存进user_problem表中'''
    user = User.objects.get(user_id=userid)
    problem = Problem.objects.get(problem_id=id)
