from django.dispatch import receiver
from universalbot import tasks_signals as ts
from universalbot.models import Profile
from selen.manager import ApprovedTaskManager

# @receiver(ts.each_profile_end, sender=Profile)
# def update_progress(sender, profile, list_, task, **kwargs):
# 	all_profiles = sum([ l.profiles.filter(status=True).count() for l in task.lists.all() ])
# 	task.current += 1
# 	task.progress = round(task.current / all_profiles * 100, 2)
# 	task.save()


@receiver(ts.on_approved_task_manager_refresh_list, sender=ApprovedTaskManager.__class__)
def update_qsize(sender, lists, **kwargs):
	# print('==========> Updating_qsize')
	for task_id in lists:
		task_adapter = sender._get_taskAdaptor(task_id)
		if task_adapter:
			# update TaskAddapter progress
			qsize = len(lists[task_id][1])
			task_adapter.qsize = qsize
			task_adapter.save()
