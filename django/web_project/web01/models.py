from django.db import models

class User(models.Model):
    '''用户名、密码、进度、专注度、注册时间、当前时间、学习总时间、做过的题数、对的题数、错题率、在线天数、上次登录是哪一天'''
    user_id = models.CharField(primary_key=True,max_length=10)
    user_passwd = models.CharField(max_length=10)
    user_progress = models.CharField(max_length=10,default=0)
    focus = models.FloatField(default=0) #学习的天数/从注册到现在的时间
    register_time = models.CharField(max_length=100,default=0)
    current_time = models.CharField(max_length=100,default=0)
    sum_time = models.IntegerField(default=0)
    dones = models.FloatField(default=0)#做过的题数
    correct = models.FloatField(default=0)#做对的题数
    accuracy = models.FloatField(default=0)#正确率
    online_days = models.IntegerField(default=0)
    last_online_day = models.CharField(max_length=100,default=0)
    class Meta:
        db_table = 'user'

class Problem(models.Model):
    problem_id = models.IntegerField()
    problem_text = models.CharField(max_length=500)
    problem_answer = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = 'problem'

class Course_Python(models.Model):
    '''python课表'''
    chapter = models.CharField(max_length=40)#章节
    video = models.IntegerField()
    ppt = models.IntegerField()
    class Meta:
        db_table = 'course_python'


class Level(models.Model):
    '''阶段表''''''阶段名''''讲义个数'''
    level_name = models.CharField(max_length=20)
    note_nums = models.IntegerField()
    class Meta:
        db_table = 'level'


class Level_list(models.Model):
    '''阶段里面的知识点''' '''主键'''   '''讲义名'''
    level = models.ForeignKey("Level",on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    class Meta:
        db_table = 'level_list'


class OnlineTime(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    today = models.CharField(max_length=100,null=True)
    online_time = models.CharField(max_length=100,null=True,default=0)
    class Meta:
        db_table = 'onlinetime'


class Progress(models.Model):
    '''学习进度表'''
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    chapter = models.ForeignKey('Course_Python',on_delete=models.CASCADE)#所有章节
    learned = models.BooleanField(default=False)
    class Meta:
        db_table = 'progress'

class User_Problem(models.Model):
    '''用户题目关联表'''
    user = models.ForeignKey('User',on_delete=models.CASCADE)
    problem = models.ForeignKey('Problem',on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    is_correct = models.BooleanField(default=False)
    class Meta:
        db_table = 'user_problem'