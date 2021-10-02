# STAT/CS 287
# Purpose: Randomly choose manager and scribe rolls
# Author: Nick Hella
# 09/25/21
import random

class Roll:

	# Stores whoever has previously been in this role and who the current roles are
	current_scribe = None
	current_manager = None
	scribe_roll = [] 
	manager_roll = []
	team_members = ['Nick Hella', 'Cal Warshaw', 'Nick Knudsen', 'Jonathan St-Onge']

	# Generates random number between 0 and 3
	def generate_random_number_between_0_and_3(self):
		return random.randint(0,3)

	# Randomly chooses a scribe
	def choose_scribe(self):
		random_team_member = self.team_members[self.generate_random_number_between_0_and_3()]
		if  random_team_member not in self.scribe_roll and \
			random_team_member is not self.current_scribe and \
			random_team_member is not self.current_manager:
			self.current_scribe = random_team_member
			self.scribe_roll.append(random_team_member)
			return random_team_member
		else:
			return self.choose_scribe()

	# Randomly chooses a manager
	def choose_manager(self):
		random_team_member = self.team_members[self.generate_random_number_between_0_and_3()]
		if  random_team_member not in self.scribe_roll and \
			random_team_member is not self.current_scribe and \
			random_team_member is not self.current_manager:
			self.current_manager = random_team_member
			self.manager_roll.append(random_team_member)
			return random_team_member
		else:
			return self.choose_manager()

# Selecting scribe and manager
self = Roll()
self.current_scribe = self.choose_scribe()
self.current_manager = self.choose_manager()
print("Scribe is: " + self.current_scribe)
print("Manager is: " + self.current_manager)

#EOF