from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from universalbot.models import List

from . import actions, exceptions

l = List.objects.get(pk=1)
profiles = l.profiles.all()

server_url = 'http://127.0.0.1:4444/wd/hub'

for profile in profiles:
	try:
		actions.CreateProfile(profile)

	except exceptions.EmptyInbox:
		print('Empty Inbox')
	except Exception as e:
		print(e)
	else:
		print('Done')


	# capabilities = {
	# 	"platform" : "Windows 10",
	# 	"browserName" : "Firefox",
	# 	"version" : "75.0"
	# }

	# driver = webdriver.Remote(
	#    			command_executor=server_url,
	#    			desired_capabilities=DesiredCapabilities.FIREFOX.copy()
	#    		)

	# driver.implicitly_wait(30)
	# driver.get('https://google.com')


	# driver.close()
	# driver.quit()