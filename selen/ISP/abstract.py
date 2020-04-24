from abc import ABC

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from ..utils import MyListeners

server_url = 'http://127.0.0.1:4444/wd/hub'

class AbstractISP(ABC):
	def __init__(self, profile):
		self.profile = profile
		self.driver = self.driver_factory()
		self.loggedin = False

	def driver_factory(self):
		driver = webdriver.Remote(
		   			command_executor=server_url,
		   			desired_capabilities=DesiredCapabilities.FIREFOX.copy()
		   		)

		# driver = EventFiringWebDriver(driver, MyListeners())
		driver.implicitly_wait(10)
		return driver

	def login(self):
		pass

	def logout(self):
		pass

	def spam__report_all_to_inbox(self):
		pass

	def inbox__mark_all_as_read(self):
		pass