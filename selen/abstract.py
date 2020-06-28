import abc
import random

from selenium import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

from .utils import MyListeners
from universalbot import models


class AbstractISP(abc.ABC):
	def __init__(self, profile, list_, task, server):
		self.profile = profile
		self.list = list_
		self.task = task
		self.server = server
		self.driver = self.driver_factory()
		self.loggedin = False
		self.actions = {}
		self.register_actions()

	def driver_factory(self):
		# # get active servers.
		# servers = [ s for s in self.task.servers.all() if s.active ]
		# # choose a random server from taskAdapter
		# server = random.choice(servers)
		driver = webdriver.Remote(
					# browser_profile=,
		   			command_executor=f'http://{self.server.ip}:{self.server.port}/wd/hub',
		   			desired_capabilities=self.get_capabilities()
		   		)

		# driver = EventFiringWebDriver(driver, MyListeners())
		driver.implicitly_wait(10)
		return driver

	def get_capabilities(self):
		# capabilities = DesiredCapabilities.FIREFOX.copy()
		capabilities = DesiredCapabilities.CHROME.copy()
		# print('get_capabilities')
		proxy = self.profile.proxy

		if proxy is None or not proxy.active:
			# use random default proxy
			proxies = models.Proxy.objects.filter(active=True, default=True).all()
			if proxies:
				proxy = random.choice(proxies)
			else:
				proxy = None

		if proxy:
			# print('setting a proxy')
			# print(proxy)
			prox = Proxy()
			prox.proxy_type = ProxyType.MANUAL
			if proxy.proxy_type == proxy.HTTP:
				# print('HTTP proxy')
				prox.http_proxy = f'{proxy.ip}:{proxy.port}'
				prox.ssl_proxy = f'{proxy.ip}:{proxy.port}'
				prox.ftp_proxy = f'{proxy.ip}:{proxy.port}'
			elif proxy.proxy_type == proxy.SOCKS:
				# print('Socks proxy')
				prox.socks_proxy = f'{proxy.ip}:{proxy.port}'
				prox.socks_username = proxy.username
				prox.socks_password = proxy.password
		
			prox.add_to_capabilities(capabilities)

		# print(capabilities)
		return capabilities


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


class ISP_Factory():
	@staticmethod
	def get_isp(profile, l, task, server):
		# avoiding circular import.
		from selen.ISP.hotmail import Hotmail
		from selen.ISP.gmail import Gmail

		email = profile.email.lower()
		if email.endswith('@hotmail.com') or email.endswith('@outlook.com'): 
			return Hotmail(profile, l, task, server)

		if email.endswith('@gmail.com'):
			return Gmail(profile, l, task, server)
