from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.

User = settings.AUTH_USER_MODEL
CHOICES = [('1','Private'),('2','Public')]
SITUATION = [('1','Working On...'),('2','Finished'),('3','Cancelled')]


class BlogPost(models.Model):

	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL)
	image = models.ImageField(upload_to='image/',blank=True,null=True)
	title = models.CharField(max_length=35,null=True)
	is_private = models.CharField(choices=CHOICES,default='2',max_length=10)
	content = models.TextField(null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
	updated = models.DateTimeField(auto_now=True) 

	class Meta:
		ordering=['-updated','-timestamp']

	def get_absolute_url(self):
		slugged_title = slugify(self.title)
		return f"{slugged_title}/{self.id}" # str(slugged_title) + "/" + str(self.id)

	def __str__(self):
		return '%s' % (self.title)
		


class UserProfile(models.Model):
	
	user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
	startdate = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)
	duedate = models.DateField(auto_now=False,auto_now_add=False,null=True,blank=True)
	image = models.ImageField(upload_to='image/',blank=True,null=True)
	trait = models.CharField(max_length=35,null=True)
	content = models.TextField(null=True, blank=True)

class Project(models.Model):
	
	projectowners = models.ManyToManyField(User,related_name="powner",blank=False)
	projectgiver = models.ForeignKey(User,null=True,related_name="pgiver",on_delete=models.SET_NULL,blank=False)
	progress = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)],blank=False)
	title = models.CharField(max_length=30,null=True,blank=False)
	content = models.TextField(null=True,blank=False)
	startdate = models.DateField(auto_now=False,auto_now_add=False, null=True,blank=True)
	duedate = models.DateField(auto_now=False,auto_now_add=False, null=True,blank=True)

	class Meta:
		ordering=['-duedate']

	def get_absolute_url(self):
		slugged_title = slugify(self.title)
		return f"{slugged_title}/{self.id}"

	def __str__(self):
		return '%s' % (self.title)


class Tasks(models.Model):

	associated_project = models.ForeignKey(Project,null=True,on_delete=models.SET_NULL,blank=False)
	taskgiver = models.ForeignKey(User,null=True,related_name="giver",on_delete=models.SET_NULL,blank=False)
	situation = models.CharField(choices=SITUATION,max_length=10,blank=False)
	title = models.CharField(max_length=30,null=True,blank=False)
	content = models.TextField(null=True,blank=False)
	startdate = models.DateField(auto_now=False,auto_now_add=False, null=True,blank=True)
	duedate = models.DateField(auto_now=False,auto_now_add=False, null=True,blank=True)

	class Meta:
		ordering=['duedate']

	def get_absolute_url(self):
		slugged_title = slugify(self.title)
		return f"{slugged_title}/{self.id}"

	def __str__(self):
		return '%s' % (self.title)


class Diary(models.Model):

	associated_task = models.ForeignKey(Tasks,null=True,on_delete=models.SET_NULL,blank=False)
	user = models.ForeignKey(User,default=1,null=True,on_delete=models.SET_NULL)
	title = models.CharField(max_length=30,null=True,blank=False)
	content = models.TextField(null=True,blank=False)
	file = models.FileField(upload_to='files/',blank=True,null=True)
	date = models.DateField(auto_now=False,auto_now_add=True)

	class Meta:
		ordering=['-date']

	def get_absolute_url(self):
		slugged_title = slugify(self.title)
		return f"{slugged_title}/{self.id}"

	def __str__(self):
		return '%s' % (self.title)