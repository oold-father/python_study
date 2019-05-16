from django import forms
from django.template.loader import get_template
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from web01.models import User,Problem,Course_Python,Level_list,Level,User_Problem
import os
import sys
from django.template import RequestContext

def get_problem_answer(id):
    answer = Problem.objects.get(id=id).answer
    answer = answer.replace('\n',' ').replace(',',' ')
    answer = answer.split(' ')
    return answer

def get_user_answer():
    f = open('stdout.txt','r')
    value = f.read()
    value = value.replace('\n',' ').replace(',',' ')
    value = value.split(' ')
    return value

def censor(user_answer,problem_answer):
    for i in user_answer:                                       #遍历用户答案，标记答案正确与否
        if i in problem_answer:
            problem_answer.remove(i)
    if problem_answer:                                       #正确答案剩余不为空则没有做对
        return 0
    else:
        return 1
        
def update_correct(request,id):
    if 'userid' in request.session:
        userid = request.session['userid']
        correct = User_Problem.object.get(user_id=userid,problem_id=id)
        user_answer = get_user_answer()
        problem_answer = get_problem_answer(id)
        correct.is_correct = censor(user_answer,problem_answer)
        correct.save()

def update_corrrects(request,id):
    if 'userid' in request.session:
        userid = request.session['userid']
        user = User.objects.get(user_id=userid)
        corrects = User_Problem.object.get(user_id=userid)
        user.correct = corrects
        user.seve()

def update_dones(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        user = User.objects.get(user_id=userid)
        nums = User_Problem.objects.filter(is_done=True,userid=userid)
        user.is_done = len(nums)
        user.save()

def update_accuracy(request):
    if 'userid' in request.session:
        userid = request.session['userid']
        user = User.objects.get(user_id=userid)
        nums = User_Problem.objects.filter(is_done=True,userid=userid)
        num = User_Problem.objects.filter(is_accuracy=True,userid=userid)
        if 0 == len(nums):
            user.accuracys = 0
            user.save()
        else:
            user.accuracys = len(num)/len(nums)
            user.save()
