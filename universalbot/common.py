import csv
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# import hotmailbot.models as models

# parse the csv file & create profiles form it.
def create_profiles_from_list(l):
	# print('>>> Creating profiles from csv...')
	from .models import Profile
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
							profile = Profile.objects.create(email=line['email'], password=line.get('password', None))
						l.profiles.add(profile)
	except IOError as e:
		pass
		# print(e)