from django.shortcuts import render ,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
# Create your views here.

from .models import (
	BlogPost, 
	UserProfile,
	Tasks,
	Project,
	Diary,
	)

from .forms import (
	BlogPostModelForm, 
	UserProfileModelForm,
	TasksModelForm,
	ProjectModelForm,
	DiaryModelForm,
	)


####################### BLOG POST ##################################3

@login_required
def blog_post_detail_page(request,post_id=0,post_title=''):


	if post_id!=0:
		obj = get_object_or_404(BlogPost,id=post_id)

	else:
		obj = get_object_or_404(BlogPost,title=post_title)

	template_name = 'blog_post_detail.html'
	context = {"object": obj}
	return render(request, template_name,context)

@login_required
def blog_post_list_view(request):
	#listing out the objects , searching for example

	qs = BlogPost.objects.all()
	#qs = BlogPost.objects.filter(title__icontains='hello') returns object that contain hello in their title
	template_name = 'blog_post_list.html'
	context = {'object_list': qs}
	return render(request, template_name, context)

# @staff_member_required
@login_required
def blog_post_create_view(request): 
	#for creating objects
	#usage of form is needed
	form = BlogPostModelForm(request.POST or None, request.FILES or None)

	if form.is_valid():
		obj = form.save(commit=False)
		obj.user = request.user
		obj.save()
		form = BlogPostModelForm() #for reinitializing i.e. clearing the fields on page
		
	template_name = 'form.html'
	context = {'form': form}
	return render(request, template_name, context)

@login_required
def blog_post_update_view(request,post_id=0,post_title=''):

	if post_id!=0:
		obj = get_object_or_404(BlogPost,id=post_id)
	else:
		obj = get_object_or_404(BlogPost,title=post_title)

	if request.user == obj.user:	

		form = BlogPostModelForm(request.POST or None, instance=obj)

		if form.is_valid():
			form.save()

		template_name = 'form.html'
		context = {'form': form , "title": f"Edit {obj.title}"}
		return render(request, template_name,context)

	else:
		return blog_post_detail_page(request,post_id,post_title)

@login_required
def blog_post_delete_view(request,post_id=0,post_title=''): 

	if post_id!=0:
		obj = get_object_or_404(BlogPost,id=post_id)
	else:
		obj = get_object_or_404(BlogPost,title=post_title)

	if request.user == obj.user:

		if request.method == 'POST':
			obj.delete()
			return redirect('/blog')
		template_name = 'blog_post_delete.html'
		context = {"object": obj}
		return render(request, template_name,context)	

	else:
		return blog_post_detail_page(request,post_id,post_title)


###################### PROFILE ###############################

@login_required
def profile_user(request,user_name):
	user = User.objects.get(username=user_name)
	qs = BlogPost.objects.filter(user=user)
	try:
		profile = UserProfile.objects.get(user=user)
	except UserProfile.DoesNotExist:
		profile = None
	context={'object_list': qs , "user":user , "obj": profile}
	return render(request,'profile.html',context)

def profiles(request):
	
	qs = UserProfile.objects.all()
	return render(request,'profile_all.html',{'profiles':qs})	

@login_required
def edit_profile(request,user_name):
	if user_name == request.user.username.lower():
		user = User.objects.get(username=user_name)
		try:
			profile = UserProfile.objects.get(user=user)
		except:
			profile = None
		if profile:
			form = UserProfileModelForm(request.POST or None, request.FILES or None,instance=profile)
		else:
			form = UserProfileModelForm(request.POST or None, request.FILES or None)	

		
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			form = UserProfileModelForm()
		return render(request,'form.html',{'form':form})
	else:
		redirect('/blog')

#################### TASK VIEWS #########################

@login_required
def task_view(request):

	if request.user.is_superuser:
		tasks = Tasks.objects.all()
		return render(request,'task_list.html',{'tasks': tasks})
	

	elif request.user.is_staff:
		tasks = Tasks.objects.filter(taskgiver=request.user)
		return render(request,'task_list.html',{'tasks': tasks})
	

	elif request.user.is_authenticated:
		projects = Project.objects.filter(projectowners__id__contains=request.user.id)
		tasks = Tasks.objects.filter(associated_project__in=projects)
		return render(request,'task_list.html',{'tasks':tasks})

@login_required  #a good example for allowing the user to change only one field of model by letting him see only one field(HTML file)
#of the corresponding model form then updating with respect to given input
def task_detail(request,task_id,task_name=''):

	obj = get_object_or_404(Tasks,id=task_id)
	form = TasksModelForm(request.POST or None,instance=obj)
	form.fields['startdate'].widget.attrs['readonly'] = 'readonly'
	form.fields['duedate'].widget.attrs['readonly'] = 'readonly'
	accessible_by = obj.associated_project.projectowners.all()

	if request.method == 'POST':
		
		Tasks.objects.filter(pk=obj.pk).update(situation = form.data['situation'])
			
			
	return render(request,'task_detail.html',{'task':obj,'form':form ,'accessible_by':accessible_by})

@staff_member_required
def task_create(request):
	
	if request.user.is_staff:
		form = TasksModelForm(request.POST or None)
		if form.is_valid() and request.method == 'POST':
			
			obj = form.save(commit=False)
			obj.taskgiver = request.user
			obj.save()
			form = TasksModelForm()
			
		return render(request,'form.html',{'form':form})

@staff_member_required
def task_edit(request,task_id,task_name=''):

	obj = get_object_or_404(Tasks,id=task_id)
	form = TasksModelForm(request.POST or None, instance=obj)

	if form.is_valid():
		form.save()

	return render(request,'form.html',{'form':form})

@staff_member_required
def task_delete(request,task_id,task_name=''):

	obj = get_object_or_404(Tasks,id=task_id)

	if request.method == 'POST':
			obj.delete()
			return redirect('/tasks')
	return render(request,'task_delete.html',{'obj':obj})


####################### PROJECT VIEWS ##############################	

@login_required
def project_view(request):

	if request.user.is_superuser:
		projects = Project.objects.all()
		return render(request,'project_list.html',{'projects': projects })
	
	elif request.user.is_staff:
		projects = Project.objects.filter(projectgiver=request.user)
		return render(request,'project_list.html',{'projects': projects })
	
	elif request.user.is_authenticated:
		projects = Project.objects.filter(projectowners__id__contains=request.user.id)
		return render(request,'project_list.html',{'projects':projects})


@staff_member_required
def project_create(request):

	if request.user.is_staff:

		form = ProjectModelForm(request.POST or None)
		form.fields['progress'].widget.attrs['readonly'] = 'readonly'
		if form.is_valid() and request.method == 'POST':

			obj = form.save(commit=False)

			obj.projectgiver = request.user
			obj.save()
			form.save_m2m() # FOR MANY TO MANY FIELDS !!!!! IMPORTANT 
			form = ProjectModelForm()

		return render(request,'form.html',{'form':form})	


		
@login_required  #a good example for allowing the user to change only one field of model by letting him see only one field(HTML file)
#of the corresponding model form then updating with respect to given input
def project_detail(request,project_id,project_name=''):

	obj = get_object_or_404(Project,id=project_id)
	form = ProjectModelForm(request.POST or None,instance=obj)
	form.fields['startdate'].widget.attrs['readonly'] = 'readonly'
	form.fields['duedate'].widget.attrs['readonly'] = 'readonly'
	pid = obj.id
	tasks = Tasks.objects.filter(associated_project = obj)
	prowners = obj.projectowners.all()


	if request.method == 'POST':
		
		Project.objects.filter(pk=obj.pk).update(progress=form.data['progress'])
			
	return render(request,'project_detail.html',{'project':obj,'form':form , 'tasks' : tasks , 'prowners':prowners})

def project_edit(request,project_id,project_name=''):
	
	obj = get_object_or_404(Project,id=project_id)
	form = ProjectModelForm(request.POST or None,instance=obj)

	if form.is_valid():
		form.save()

	return render(request,'form.html',{'form':form})

def project_delete(request,project_id,project_name=''):
	
	obj = get_object_or_404(Project,id=project_id)

	if request.method == 'POST':
			obj.delete()
			return redirect('/projects')
	return render(request,'project_delete.html',{'obj':obj})				


#########################DIARY###########################

def diary_view(request):

	if request.user.is_superuser:
		diaries = Diary.objects.all()
		return render(request,'diary_list.html',{'diaries': diaries})

	elif request.user.is_authenticated:
		diaries = Diary.objects.filter(user=request.user)
		return render(request,'diary_list.html',{'diaries':diaries})

@login_required
def diary_detail(request,diary_id=0,diary_title=''):


	if diary_id!=0:
		obj = get_object_or_404(Diary,id=diary_id)

	else:
		obj = get_object_or_404(Diary,title=diary_title)

	template_name = 'diary_detail.html'
	context = {"object": obj}
	return render(request, template_name,context)		

def diary_create(request):

	form = DiaryModelForm(request.POST or None, request.FILES or None)

	if form.is_valid() and request.method == 'POST':

		obj = form.save(commit=False)

		obj.user = request.user
		obj.save() 
		form = DiaryModelForm()

	return render(request,'form.html',{'form':form})


@login_required
def diary_update(request,diary_id=0,diary_title=''):

	if diary_id!=0:
		obj = get_object_or_404(Diary,id=diary_id)
	else:
		obj = get_object_or_404(Diary,title=diary_title)

	if request.user == obj.user:	

		form = DiaryModelForm(request.POST or None, instance=obj)

		if form.is_valid():
			form.save()

		template_name = 'form.html'
		context = {'form': form , "title": f"Edit {obj.title}"}
		return render(request, template_name,context)

	else:
		return diary_detail_page(request,diary_id,diary_title)

@login_required
def diary_delete(request,diary_id=0,diary_title=''): 

	if diary_id!=0:
		obj = get_object_or_404(Diary,id=diary_id)
	else:
		obj = get_object_or_404(Diary,title=diary_title)

	if request.user == obj.user:

		if request.method == 'POST':
			obj.delete()
			return redirect('/diaries')
		template_name = 'blog_post_delete.html'
		context = {"object": obj}
		return render(request, template_name,context)	

	else:
		return diary_detail_page(request,diary_id,diary_title)