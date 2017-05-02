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


def commands_iter(input_filename='item names.txt'):
	
	# 3 initial commands are static
	yield from (
		'scoreboard players set @s[score_equiphat_min=0,score_equiphat=0] equiphat -1 {Inventory:[{Slot:103b}]}',
		'tellraw @s[score_equiphat_min=-1,score_equiphat=-1] {"text":"You already have something on your head.","color":"gray"}',
	)
	
	scoreboard_command='/scoreboard players set @a[team=Donator,score_equiphat_min=0,score_equiphat=0] equiphat {score} {{SelectedItem:{{id:"minecraft:{item_name}",Damage:{item_damage}s}}}}'
	clear_command='/clear @a[score_equiphat_min={score},score_equiphat={score}] minecraft:{item_name} {item_damage} 1'
	replaceitem_command='/replaceitem entity @a[score_equiphat_min={score},score_equiphat={score}] slot.armor.head minecraft:{item_name} 1 {item_damage}'
	
	with open(input_filename) as items_file:
		# score_equiphat=0 is reserved as
		# "@s has run the hat command and has nothing in slot.armor.head"
		for score, item in enumerate(items_file, 1):
			# split tabs and remove final newlines
			item = item.rstrip().split()
			
			for command in (scoreboard_command, clear_command, replaceitem_command):
				yield command.format(
						score=score,
						item_name=item[0], # JSON strings must be quoted
						item_damage=item[1],
				)
	
	# 2 final commands are also static
	yield from (
		'tellraw @s[score_equiphat_min=0,score_equiphat=0] {"text":"Invalid item. You need to hold a custom hat in your hand.","color":"gray"}',
		'scoreboard players reset @s[score_equiphat_min=-1] equiphat',
	)


def write_commands(input_filename='', output_filename='commands.txt'):
	"""Write commands from commands_iter() to a file
	
	Useful for <1.12.x servers, which do not support advancements.
	"""
	
	with open(output_filename, 'w') as outfile:
		# if input filename is not specified, use default
		if not len(input_filename):
			for command in commands_iter():
				outfile.write(command + '\n')
		else:
			# TODO deduplicate
			for command in commands_iter(input_filename):
				outfile.write(command + '\n')


def to_advancement(name='null_byte:custom_hat', iterable=commands_iter()):
	"""Convert commands from iterable to an advancement JSON object
	
	name is the in-game name of the advancement
	iterable is something that provides commands
	(the iterable should not provide 'advancement revoke ...')
	"""
	
	# set up a basic command-based advancement as a python dict
	# this is a template applicable to all similar
	# advancements
	advancement = {
		'criteria': {
			'run': {
				'trigger': 'minecraft:impossible'
			}
		},
		
		'rewards': {
			'commands': [
				'advancement revoke @s only {}'.format(name)
			]
		}
	}
	
	# add the commands to the commands reward
	advancement['rewards']['commands'].extend(iterable)
	
	return advancement

	
def write_advancement(contents: str, name='null_byte:custom_hat'):
	# in the advancements directory, files are laid out as
	# namespace:advancement → namespace/advancement.json
	output_dir, output_filename = name.split(':')
	
	try:
		os.mkdir(output_dir)
	except FileExistsError: # if the dir already exists, great!
		pass
	
	# if there's any other errors, let them propagate
	# (ie halt the module and tell the user)
	
	with open(os.path.join(output_dir, output_filename + '.json'), 'w') as f:
		json.dump(contents, f)

if __name__ == '__main__':
	write_advancement(to_advancement())
