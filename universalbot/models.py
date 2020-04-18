from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator, \
				FileExtensionValidator, validate_email
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import transaction

from background_task.models import Task, CompletedTask

from . import common


class Actions(models.IntegerChoices):
	INBOX_ADD_ALL_TO_ARCHIVE = (1, 'Inbox, add all to archive')
	INBOX_MARK_ALL_AS_READ = (2, 'Inbox, mark all as read')
	SPAM_REPORT_ALL_TO_INBOX = (3, 'Spam, report all to inbox')


class List(models.Model):
	name = models.CharField(max_length=32, unique=True)
	actions = MultiSelectField(max_length=256, choices=Actions.choices)
	file = models.FileField(upload_to='profiles_lists/%Y/%m/', null=True, blank=True, 
		verbose_name='Load profiles from a csv file',
		validators=[FileExtensionValidator(['csv'])]
		)

	profiles = models.ManyToManyField('Profile', blank=True)

	updated 	= models.DateTimeField(auto_now=True)
	created 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.name} ({self.profiles.count()})'

	def save(self, *args, **kwargs):
		old_list = None
		if self.pk:
			try:
				old_list = List.objects.get(pk=self.pk)
			except self.DoesNotExist:
				pass
		pk = self.pk
		super().save(*args, **kwargs)

		# appending profiles from a csv file.
		if (pk is None and self.file):
			transaction.on_commit(lambda: common.create_profiles_from_list(self))
		elif old_list and not bool(old_list.file) and bool(self.file):
			transaction.on_commit(lambda: common.create_profiles_from_list(self))
		elif old_list and bool(old_list.file) and bool(self.file):
			if old_list.file.path != self.file.path:
				transaction.on_commit(lambda: common.create_profiles_from_list(self))
		


		


class Profile(models.Model):
	email = models.CharField(max_length=64, unique=True)
	password = models.CharField(max_length=64)
	status = models.BooleanField(default=False)

	updated 	= models.DateTimeField(auto_now=True)
	created 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email


class Proxy(models.Model):
	proxy = models.GenericIPAddressField()
	port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(0)])
	active = models.BooleanField(default=True, help_text='Active means that the server proxy is up and running and is ready to use.')

	class Meta:
		db_table = 'proxies'
		verbose_name_plural = 'Proxies'

	def __str__(self):
		return f'{self.proxy}:{self.port}'



class TaskAdaptor(models.Model):
	task_name = models.CharField(max_length=255, null=True, unique=True)
	run_at = Task._meta.get_field('run_at')
	repeat = Task._meta.get_field('repeat')
	repeat_until = Task._meta.get_field('repeat_until')

	lists = models.ManyToManyField('List')
	task = models.OneToOneField(Task, null=True, blank=True, default=None, on_delete=models.SET_NULL)
	completed_task = models.OneToOneField(CompletedTask, null=True, blank=True, default=None, on_delete=models.SET_NULL)
	
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'task_adaptors'
		verbose_name = 'Task'
		verbose_name_plural = 'Tasks'

	# def save(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)





# class Task(models.Model):
# 	class Status(models.IntegerChoices):
# 		ACTIVE 		= (1, 'Active')
# 		INACTIVE 	= (2, 'Inactive')
# 		ABORTED 	= (3, 'Aborted')
# 		COMPLETED 	= (4, 'Completed')

# 	name = models.CharField(max_length=42, unique=True)
# 	start = models.DateTimeField()
# 	status = models.IntegerField(choices=Status.choices, default=Status.INACTIVE)

# 	lists = models.ManyToManyField('List')

# 	updated = models.DateTimeField(auto_now=True)
# 	created = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.name