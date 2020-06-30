import queue

from django.db import models
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator,\
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

	profiles = models.ManyToManyField('Profile', limit_choices_to={'status': True}, blank=True)

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
	proxy = models.ForeignKey('Proxy', on_delete=models.SET_NULL,
		limit_choices_to={'active': True}, null=True, blank=True)

	updated 	= models.DateTimeField(auto_now=True)
	created 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email


class Proxy(models.Model):

	HTTP = 1
	SOCKS = 2

	Type = [
		(HTTP, 'HTTP/HTTPS'),
		(SOCKS, 'Socket4/Socket5')
	]

	ip = models.GenericIPAddressField(verbose_name='Proxy IP Address')
	port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(1)])
	username = models.CharField(max_length=40, null=True, blank=True)
	password = models.CharField(max_length=40, null=True, blank=True)
	active = models.BooleanField(default=True, help_text='Active means that the server proxy is up and running and is ready to use.')
	default = models.BooleanField(default=False, help_text='Will be used for profiles that don\'t have their proxies.')
	proxy_type = models.IntegerField(choices=Type, default=HTTP, verbose_name='Type')

	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'proxies'
		verbose_name_plural = 'Proxies'

	def __str__(self):
		return f'{self.ip}:{self.port}'


class TaskAdaptor(models.Model):
	class QUEUE_STATUS(models.IntegerChoices):
		PROCESSING 	= (0, 'Processing')
		COMPLETED 	= (1, 'Completed')
		EMPTY		= (2, 'Empty')


	task_name = models.CharField(max_length=255, null=True, unique=True)
	run_at = Task._meta.get_field('run_at')
	repeat = Task._meta.get_field('repeat')
	repeat_until = Task._meta.get_field('repeat_until')
	# progress = models.IntegerField(default=0, null=True, blank=True)
	# number of processed profiles.
	qsize 			= models.IntegerField(default=0, null=True, blank=True)
	total_qsize 	= models.IntegerField(default=0, null=True, blank=True)
	queue_status 	= models.IntegerField(choices=QUEUE_STATUS.choices, default=QUEUE_STATUS.EMPTY)

	lists = models.ManyToManyField('List')
	task = models.OneToOneField(Task, null=True, blank=True, default=None, on_delete=models.SET_NULL)
	completed_task = models.OneToOneField(CompletedTask, null=True, blank=True, default=None, on_delete=models.SET_NULL)
	servers = models.ManyToManyField('Server', limit_choices_to={'active': True}, verbose_name='Servers/RDPs')

	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'task_adaptors'
		verbose_name = 'Task'
		verbose_name_plural = 'Tasks'

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self._queue = queue.Queue()


class Server(models.Model):
	name = models.CharField(max_length=32, verbose_name='Server name', null=True, blank=True)
	ip = models.GenericIPAddressField(verbose_name='IP Address')
	port = models.PositiveIntegerField(validators=[MaxValueValidator(65535), MinValueValidator(1)])
	active = models.BooleanField(default=True, help_text='Active means that the server is up and running and is ready to use.')
	capacity = models.IntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(50)],
				help_text='How many profiles this server can handle concurrently, (from 1 to 50).')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'servers'

	def __str__(self):
		# status = 'Active' if self.active else 'Inactive'
		return f'{self.ip}:{self.port} (capacity: {self.capacity})'


class ATM(models.Model):
	""" Hhhhh, not the ATM you know, it's ApprovedTaskManagerModel """
	task = models.ForeignKey('TaskAdaptor', on_delete=models.CASCADE)


class Deleted_queue(models.Model):
	""" Queues to be deleted by ApprovedTaskManagerModel """
	task = models.ForeignKey('TaskAdaptor', on_delete=models.CASCADE)
