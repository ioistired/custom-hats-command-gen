#!/usr/bin/env python3
# encoding: utf-8
# 
# MIT Licensed
# https://bmintz.mit-license.org/@2017

"""
command_gen.py: generate commands for custom hat modules

item names.txt format:
name \t damage value (0 if none)
"""

import os
import json


class Item:
	def __init__(self, name, damage_value=0):
		self.name = name
		self.damage_value = damage_value
	
	def __eq__(self, other):
		return self.name, self.damage_value == other.name, other.damage_value


class RestrictedItem(Item):
	def __init__(self, restricted_team_name, *args, **kwargs):
		super(RestrictedItem, self).__init__(*args, **kwargs)
		self.restricted_team_name = restricted_team_name


def get_team_selector(item):
	try:
		return ',team={}'.format(item.restricted_team_name)
	except AttributeError:
		return ''


class ItemConfig(list):
	def __init__(self, filename):
		with open(filename) as config_file:
			
			self._get_restricted_team_name(config_file)
			
			for line in config_file:
				line = line.rstrip()
				prefix = line[0]
				
				if prefix == '#':
					continue # ignore comments
				else:
					if len(line.split('\t')) == 1:
						print(line)
					name, damage = line.split()
					self.append(self._make_item(name, damage))
	
	
	def _make_item(self, name, damage):
		if name[0] == '!':
			return RestrictedItem(
				self.restricted_team_name,
				name[1:],
				damage
			)
		else:
			return Item(name, damage)
	
	
	def _get_restricted_team_name(self, config_file):
		first_line = next(config_file).rstrip()
			
		if len(first_line.split()) == 1: # no \t == not an item
			self.restricted_team_name = first_line


def commands_iter(items_filename='item names.txt'):
	
	yield from (
		'scoreboard players set @s[score_hat_min=1,score_hat=1] hat 0 {Inventory:[{Slot:103b}]}',
		'tellraw @s[score_hat_min=0,score_hat=0] {"text":"You already have something on your head.","color":"gray"}',
	)
	
	scoreboard_command='scoreboard players set @s[score_hat_min=1,score_hat=1{team}] hat {score} {{SelectedItem:{{id:"minecraft:{name}",Damage:{damage}s}}}}'
	clear_command='clear @s[score_hat_min={score},score_hat={score}] minecraft:{name} {damage} 1'
	replaceitem_command='replaceitem entity @s[score_hat_min={score},score_hat={score}] slot.armor.head minecraft:{name} 1 {damage}'
	
	# we start with a score of 2
	# because -1, 0, and 1 are reserved
	for score, item in enumerate(ItemConfig(items_filename), 2):
		for command in (scoreboard_command, clear_command, replaceitem_command):
			
			yield command.format(
				score=score,
				name=item.name,
				damage=item.damage_value,
				team=get_team_selector(item),
			)
	
	yield from (
		'tellraw @s[score_hat_min=1,score_hat=1] {"text":"Either the item you\'re holding is invalid, or you don\'t have permission to equip it.","color":"gray"}',
		'scoreboard players set @s hat -1',
	)



def parse_function_name(name):
	"""Convert an in-game function name to a file path
	
	>>> parse_advancement_name('null_byte:custom_hat')
	null_byte/custom_hat.mcfunction
	>>> parse_advancement_name('null_byte:hat/command')
	null_byte/hat/command.mcfunction
	"""
	
	# namespace:subdir/advancement → namespace/subdir/advancement.json
	fullpath = name.replace(':', '/') + '.mcfunction'
	return os.path.split(fullpath)

	

def write_function(commands, name):
	output_dir, output_filename = parse_function_name(name)
	output_dir = os.path.join('functions', output_dir)
	
	try:
		os.mkdir(output_dir)
	except FileExistsError: # if the dir already exists, great!
		pass
	
	# if there's any other errors, let them propagate
	# (ie halt the module and tell the user)
	
	with open(os.path.join(output_dir, output_filename), 'w') as f:
		for command in commands_iter():
			f.write(command + '\n')



if __name__ == '__main__':
	name = 'null_byte:hat/equip'
	write_function(commands_iter(name), name)
