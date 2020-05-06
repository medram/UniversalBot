from django.dispatch import receiver
from universalbot import tasks_signals as ts
from universalbot.models import Profile

@receiver(ts.each_profile_end, sender=Profile)
def update_progress(sender, profile, list_, task, **kwargs):
	all_profiles = sum([ l.profiles.count() for l in task.lists.all() ])
	task.current += 1
	task.progress = round(task.current / all_profiles * 100, 2)
	task.save()