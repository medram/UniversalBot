import json

from django.db import transaction
from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from background_task.models import Task, TaskManager

from . import common
from .models import TaskAdaptor, List


def on_transaction_commit(func):
    ''' Create the decorator '''
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner



# create the task automatically
@receiver(post_save, sender=TaskAdaptor)
def create_task(sender, instance, created, **kwargs):
	if created:
		# task_name = f'{__package__}.tasks.run_lists' # function that going to be fired
		task_name = f'hotmailbot.views.notify_user' # function that going to be fired

		args = None
		kwargs = {
			# 'lists': [l.pk for l in instance.lists]
		}
		run_at = instance.run_at
		verbose_name = instance.task_name
		repeat = instance.repeat
		repeat_until = instance.repeat_until

		task = TaskManager().new_task(task_name=task_name, args=args, kwargs=kwargs,
				 run_at=run_at, priority=0, queue=None, verbose_name=verbose_name,
				 creator=None, repeat=repeat, repeat_until=repeat_until,
				 remove_existing_tasks=False
				 )
		task.save()
		instance.task = task
		instance.save()


# Append the lists ids to the task as a parameters.
@receiver(m2m_changed, sender=TaskAdaptor.lists.through)
def add_params_to_task(sender, instance, action, model, pk_set, **kwargs):

	if action == 'post_add':
		args = (2,)
		kwargs = {
			# 'lists': tuple(pk_set)
		}
		instance.task.task_params = json.dumps((args, kwargs), sort_keys=True)
		instance.task.save()


# @receiver(post_save, sender=List)
# @on_transaction_commit
# def add_profiles_to_list(sender, instance, created, **kwargs):
# 	print('> add_profiles_to_list')
# 	if (created and instance.file):
# 		print('> at creation')
# 		common.create_profiles_from_list(instance)
# 	# elif not created and instance.file: 
# 	# 	# adding file at edit mode
# 	# 	print('> at editing')
# 	# 	common.create_profiles_from_list(instance)
# 	else:
# 		try:
# 			old_list = List.objects.get(pk=instance.pk)
			
# 			if old_list.file and old_list.file.path != instance.file.path:
# 				print('> at file changed')
# 				common.create_profiles_from_list(instance)
# 		except List.DoesNotExist:
# 			pass

# Update the task automatically
@receiver(post_save, sender=TaskAdaptor)
def save_task(sender, instance, **kwargs):
	instance.task.run_at = instance.run_at
	instance.task.verbose_name = instance.task_name
	instance.task.repeat = instance.repeat
	instance.task.repeat_until = instance.repeat_until
	instance.task.save()


# Delete the task automatically
@receiver(post_delete, sender=TaskAdaptor)
def delete_task(sender, instance, **kwargs):
	instance.task.delete()
