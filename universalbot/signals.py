import json

from django.db import transaction
from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from background_task.models import Task, CompletedTask
from background_task.signals import task_created, task_rescheduled
from background_task.tasks import DBTaskRunner

from . import common
from .models import TaskAdaptor, List
from .tasks import run_lists

def on_transaction_commit(func):
    ''' Create the decorator '''
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner



# create the task automatically
@receiver(post_save, sender=TaskAdaptor)
@on_transaction_commit
def create_task(sender, instance, created, **kwargs):
	if created:
		# Create a task
		task = run_lists(
					{
						'task_id': instance.pk
					},
					schedule=instance.run_at,
					repeat=instance.repeat,
					verbose_name=instance.task_name,
					repeat_until=instance.repeat_until
				)
		instance.task = task
		instance.save()


# Update the task automatically
@receiver(post_save, sender=TaskAdaptor)
@on_transaction_commit
def save_task(sender, instance, created, **kwargs):
	if not created:
		if instance.task:
			# update a task
			instance.task.run_at = instance.run_at
			instance.task.verbose_name = instance.task_name
			instance.task.repeat = instance.repeat
			instance.task.repeat_until = instance.repeat_until
			instance.task.save()
		else:
			# Create a task
			task = run_lists(
						{
							'task_id': instance.pk
						},
						schedule=instance.run_at,
						repeat=instance.repeat,
						verbose_name=instance.task_name,
						repeat_until=instance.repeat_until
					)
			instance.task = task
			instance.save()

# Delete the task automatically
@receiver(post_delete, sender=TaskAdaptor)
def delete_task(sender, instance, **kwargs):
	try:
		if instance.task:
			instance.task.delete()
		if instance.completed_task:
			instance.completed_task.delete()
	except:
		pass


# append Task to a taskAdapter
@receiver(post_save, sender=Task)
def update_taskadaptor(sender, instance, created, **kwargs):
	# print('> update_taskadaptor')
	if created:
		# print('> do something at creation.')
		TaskAdaptor.objects.filter(task_name=instance.verbose_name).update(task=instance)

	# print('> do something at update.')
	TaskAdaptor.objects.filter(task_name=instance.verbose_name).update(
			run_at = instance.run_at,
			repeat = instance.repeat,
			repeat_until = instance.repeat_until
		)



# append CompletedTask to a taskAdapter
@receiver(post_save, sender=CompletedTask)
def update_taskadaptor2(sender, instance, created, **kwargs):
	if created:
		try:
			task_adaptor = TaskAdaptor.objects.get(task_name=instance.verbose_name)
			task_adaptor.completed_task = instance
			task_adaptor.save()
		except TaskAdaptor.DoesNotExist:
			pass
