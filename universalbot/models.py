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
	INBOX_SELECT_ALL_MARK_AS_READ 		= (1, '(Inbox), Select all mark as read.')
	SPAM_SELECT_ALL_MARK_AS_READ 		= (2, '(Spam), Select all mark as read.')
	SPAM_REPORT_ALL_TO_INBOX 			= (4, '(Spam), Report all to inbox.')
	INBOX_ARCHIVE_ALL 					= (5, '(Inbox), Archive all.')
	INBOX_OPEN_MESSAGES 				= (3, '(Inbox), Open messages.')


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
	servers = models.ManyToManyField('Server')

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'task_adaptors'
		verbose_name = 'Task'
		verbose_name_plural = 'Tasks'


# class Task_server(models.Model):
# 	task = models.ForeignKey('TaskAdaptor', on_delete=models.CASCADE)
# 	server = models.ForeignKey('Server', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return f'{self.task} - {self.server}'


class Server(models.Model):
	ip = models.GenericIPAddressField(verbose_name='IP Address')
	port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(0)])
	active = models.BooleanField(default=True, help_text='Active means that the server is up and running and is ready to use.')

	class Meta:
		db_table = 'servers'

	def __str__(self):
		return f'{self.ip}:{self.port}'