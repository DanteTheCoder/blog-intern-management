from django import forms
from .models import BlogPost, UserProfile, Tasks, Project, Diary
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

USERS = User.objects.all()

PROJECTS = Project.objects.all()

class BlogPostModelForm(forms.ModelForm):

	class Meta:
		model =	BlogPost
		fields = ['title','image','is_private','content']

	def __init__(self, *args, **kwargs):
		super(BlogPostModelForm, self).__init__(*args, **kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })
			self.fields[field].label = ''

		self.fields['title'].widget.attrs['placeholder'] = 'Title'
		self.fields['content'].widget.attrs['placeholder'] = 'Content'



class UserProfileModelForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields=['startdate','duedate','image','trait','content']

	def __init__(self, *args, **kwargs):
		super(UserProfileModelForm, self).__init__(*args, **kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })
			self.fields[field].label = ''

		self.fields['trait'].widget.attrs['placeholder'] = 'Trait'
		self.fields['content'].widget.attrs['placeholder'] = 'Content'
		self.fields['startdate'].widget.attrs['placeholder'] = 'Internship Period Start // Year-Month-Day'
		self.fields['duedate'].widget.attrs['placeholder'] = 'Internship Period End // Year-Month-Day'

class UserCreateForm(UserCreationForm):

	#username = forms.CharField(label=(""),widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}))

	#password1 = forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

	#password2 = forms.CharField(label=(""),widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password Confirm'}))

	name = forms.CharField(max_length=30)
	surname = forms.CharField(max_length=30)
	

	class Meta:
		model = User
		fields=('name','surname','username','password1','password2')

	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)

		for fieldname in self.fields:
			self.fields[fieldname].help_text = None	
			self.fields[fieldname].widget.attrs['class'] = 'form-control'
			self.fields[fieldname].label = ''

		self.fields['username'].widget.attrs['placeholder'] = 'User Name'			
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirm'
		self.fields['name'].widget.attrs['placeholder'] = 'Your First Name'
		self.fields['surname'].widget.attrs['placeholder'] = 'Your Last Name'

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.first_name = self.cleaned_data['name']
		user.last_name = self.cleaned_data['surname']
		if commit:
			user.save()
		return user	


class TasksModelForm(forms.ModelForm):
	

	class Meta:
		model = Tasks
		fields=['associated_project','situation','title','content','startdate','duedate']
		taskowner = forms.ChoiceField(choices=USERS)
		#associated_project = forms.ChoiceField(choices=PROJECTS)

	def __init__(self, *args, **kwargs):
		super(TasksModelForm, self).__init__(*args, **kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })

		self.fields['situation'].label = 'Status'
		self.fields['title'].label=""
		self.fields['content'].label=""	
		self.fields['title'].widget.attrs['placeholder'] = 'Title'
		self.fields['content'].widget.attrs['placeholder'] = 'Content'



class ProjectModelForm(forms.ModelForm):

	

	class Meta:
		model = Project
		fields = ['projectowners','title','progress','content','startdate','duedate']


	def __init__(self, *args, **kwargs):
		super(ProjectModelForm, self).__init__(*args, **kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })

		self.fields['title'].label=""
		self.fields['content'].label=""	
		self.fields['progress'].label = "Progress"
		self.fields['progress'].max_value = 100
		self.fields['title'].widget.attrs['placeholder'] = 'Title'
		self.fields['content'].widget.attrs['placeholder'] = 'Content'
		self.fields['startdate'].widget.attrs['placeholder'] = 'Project Start // Year-Month-Day'
		self.fields['duedate'].widget.attrs['placeholder'] = 'Project End // Year-Month-Day'
		

class DiaryModelForm(forms.ModelForm):

	class Meta:
		model = Diary
		fields = ['associated_task','title','content','file']

	def __init__(self,*args,**kwargs):
		super(DiaryModelForm,self).__init__(*args,**kwargs)

		for field in iter(self.fields):
			self.fields[field].widget.attrs.update({
				'class': 'form-control'	
        })

		self.fields['title'].label=''
		self.fields['content'].label=''
		self.fields['title'].widget.attrs['placeholder'] = 'Title'
		self.fields['content'].widget.attrs['placeholder'] = 'Content'