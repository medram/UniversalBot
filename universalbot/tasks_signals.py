from django.dispatch import Signal, receiver
from .models import TaskAdaptor

task_started 		= Signal(providing_args=['task'])
task_finished 		= Signal(providing_args=['task'])
task_errors 		= Signal(providing_args=['task'])
each_profile_start 	= Signal(providing_args=['profile', 'list_', 'task']) 
each_profile_end 	= Signal(providing_args=['profile', 'list_', 'task'])


@receiver(task_started, sender=TaskAdaptor)
def start(sender, task, **kwargs):
	print('starting...')



@receiver(task_finished, sender=TaskAdaptor)
def end(sender, task, **kwargs):
	print('finishing...')


