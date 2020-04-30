from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
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

	except WebDriverException as e:
		if 'Message: Reached error page' in str(e):
			print(f'Please check your internet connection of your server/RDP')
	# except Exception as e:
	# 	print(e)
	else:
		print('Done')