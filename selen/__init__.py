from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from universalbot.models import List

from . import exceptions
from .ISP.hotmail import Hotmail

l = List.objects.get(pk=1)
profiles = l.profiles.all()


for profile in profiles:
	try:
		isp = Hotmail(profile, l)
		isp.login()
		isp.do_actions()

	except exceptions.EmptyInbox:
		print('Empty Inbox')
	# except Exception as e:
	# 	print(e)
	else:
		print('Done')