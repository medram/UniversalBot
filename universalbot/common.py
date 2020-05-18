import csv
from django.core.validators import validate_email, validate_ipv4_address, validate_integer
from django.core.exceptions import ValidationError

# from . import models

# parse the csv file & create profiles form it.
def create_profiles_from_list(l):
	# print('>>> Creating profiles from csv...')
	from .models import Profile, Proxy
	try:
		if bool(l.file):
			with open(l.file.path) as f:
				reader = csv.DictReader(f)
				for line in list(reader):
					try:
						validate_email(line['email'])
					except ValidationError as e:
						pass
						# print(e)
					else:
						# get the profile if does exist
						try:
							profile = Profile.objects.get(email=line['email'])
							# print('use existing profile.')
						except Profile.DoesNotExist:
							# print(f"create {line['email']}...")
							profile = Profile.objects.create(email=line['email'], password=line.get('password', None), status=True)
						l.profiles.add(profile)

						# assign proxy to its profile. 
						try:
							ip, port, *_ = line['proxy'].split(':')
							port = int(port)
						
							validate_ipv4_address(ip)
							if port < 1 or port > 65535:
								raise ValidationError('Invalid port number')
							
							try:
								p = Proxy.objects.get(ip=ip, port=port)
							except Proxy.DoesNotExist:
								p = Proxy.objects.create(ip=ip, port=port)
							
							profile.proxy = p
							profile.save()
						except (ValidationError, KeyError, ValueError) as e:
							pass
	except IOError as e:
		pass
		# print(e)