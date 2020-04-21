from django.dispatch import Signal, receiver
from .models import TaskAdaptor

task_started = Signal(providing_args=['tasks_ids'])
task_finished = Signal(providing_args=['tasks_ids'])
task_errors = Signal(providing_args=['tasks_ids'])


@receiver(task_started, sender=TaskAdaptor)
def start(sender, tasks_ids, **kwargs):
	print('starting...')



@receiver(task_finished, sender=TaskAdaptor)
def end(sender, tasks_ids, **kwargs):
	print('finishing...')