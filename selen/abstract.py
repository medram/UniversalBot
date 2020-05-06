import abc
import random

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .utils import MyListeners

server_url = 'http://127.0.0.1:4444/wd/hub'

class AbstractISP(abc.ABC):
	def __init__(self, profile, list_, task):
		self.profile = profile
		self.list = list_
		self.task = task
		self.driver = self.driver_factory()
		self.loggedin = False
		self.actions = {}
		self.register_actions()

	def driver_factory(self):
		# get active servers.
		servers = [ s for s in self.task.servers.all() if s.active ]
		# choose a random server from taskAdapter
		server = random.choice(servers)
		driver = webdriver.Remote(
		   			command_executor=f'http://{server.ip}:{server.port}/wd/hub',
		   			desired_capabilities=DesiredCapabilities.FIREFOX.copy()
		   		)

		# driver = EventFiringWebDriver(driver, MyListeners())
		driver.implicitly_wait(10)
		return driver

	@abc.abstractmethod
	def login(self):
		pass

	@abc.abstractmethod
	def logout(self):
		pass

	def quit(self):
		self.driver.quit()

	@abc.abstractmethod
	def register_actions(self):
		pass



class ActionAbstract(abc.ABC):

	def __init__(self, isp):
		self.isp = isp

	@abc.abstractmethod
	def apply(self):
		pass
