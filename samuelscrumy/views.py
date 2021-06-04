from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse 
from .models import *
import random
from django.contrib.auth.models  import User
from .forms import SignupForm, CreateGoalForm, UpdateGoalForm, SelectGroupForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic



def is_developer(user):
    return user.groups.filter(name='Developer').exists()
  
@user_passes_test(is_developer)
def test_group(request):
      print(request.user.groups.all())
      all = request.user.groups.all()
      for item in all:
            if item.name == 'Developer':
                  print("good")
            else:
                  print("bad")
      print('yes')
      return HttpResponse("hello")
    
    
def index(request): 
  if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
              user = form.save()
              my_group = Group.objects.get(name='Developer') 
              my_group.user_set.add(user)
              user.save()
            #   group = form.cleaned_data['group']        
            #   group.user_set.add(user)
              return redirect('samuelscrumy:creation')
  else:
    form = SignupForm()
  return render(request, 'samuelscrumy/index.html', {'form': form})
  
def creation(request):
  return render(request, 'samuelscrumy/creation.html')
  


def move_goal(request, goal_id): 
      obj = ScrumyGoals.objects.get(goal_id=goal_id)
      if request.method == 'POST':
            form = UpdateGoalForm(request.POST, instance=obj)
            if form.is_valid():
                user = form.save(commit=False)
                all = request.user.groups.all()
                for item in all:
                  # print(item)     
                  
                  # for developer 
                  if item.name == 'Developer':
                      if obj.goal_status.status_name == 'Done Goal':
                        return render(request, 'samuelscrumy/done.html')
                      else:
                        print("user goal status failed")                   
                  
                  # for quality assurance
                  elif item.name == 'Quality-Assurance':
                        print("Quality Assurance")
                        if request.user == obj.user:
                              form.save()
                        elif obj.goal_status.status_name == 'Weekly Goal' or obj.goal_status.status_name == 'Daily Goal':
                            return render(request, 'samuelscrumy/QA.html')
                        else:
                              print("user goal status failed")    
                  #  for admin
                  elif item.name == 'Admin':
                        if request.user == obj.user:
                              form.save()
                        else:
                              print("yeah baby")
                                      
                user.save()  
            return redirect('samuelscrumy:home')            
      else:
          form = UpdateGoalForm(instance=obj)
          return render(request, 'samuelscrumy/movegoal.html', {'form': form, 'obj':obj,})
      # else:
      #     return render(request, 'samuelscrumy/exception.html')


def add_goal(request):
      all = request.user.groups.all()
      if request.method == 'POST':
            form = CreateGoalForm(request.POST)
            if form.is_valid():
                  user = form.save(commit=False)
                  user.goal_status_id = 1
                  all = request.user.groups.all()
                  for item in all:
                        if item.name != 'owner':
                              user.user = User.objects.get(username=request.user.username)
                              user.save()
                        else:
                              user.save()                  
                  return redirect('/samuelscrumy/home')
      else:
            form = CreateGoalForm()
      return render(request, 'samuelscrumy/addgoal.html', {'form': form})


def home(request):
  users = User.objects.all()
  weekly = ScrumyGoals.objects.filter(goal_status=1)
  Daily = ScrumyGoals.objects.filter(goal_status=2)
  Verify = ScrumyGoals.objects.filter(goal_status=3)
  Done = ScrumyGoals.objects.filter(goal_status=4)
  context = {'users':users, 'weekly':weekly, 'Daily':Daily, 'Verify':Verify, 'Done':Done,  }      
  return render(request, 'samuelscrumy/home.html', context)

      
      
def add_group(request, id):
      
      new_user = request.user
      old_user_group = new_user.groups.all()      
      if request.method == 'POST':
            form = SelectGroupForm(request.POST)
            if form.is_valid():
                  new_user_group = User.groups.through.objects.get(user=new_user)
                  group_from_form = form.cleaned_data['group']
                  new_user_group.group = group_from_form
                  new_user_group.save()
            return redirect('/samuelscrumy/home')
      else:
            form = SelectGroupForm() 
      return render(request, 'samuelscrumy/group.html', {'form': form}) 