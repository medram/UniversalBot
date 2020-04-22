from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
	help = 'print the current timezone.'

	def add_arguments(self, parser):
		pass
		# parser.add_argument('loop', type=int, help='Indicates the number of loops.')
		# parser.add_argument('-p', '--prefix', help='this is just a normal prefix')

	def handle(self, *args, **kwargs):
		import selen