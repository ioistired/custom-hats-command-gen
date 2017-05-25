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
	def __init__(self, score, name, damage=0):
		self.score, self.name, self.damage = score, name, damage


def get_items(items_filename='item names.txt'):
	with open(items_filename) as items_file:
		# score_hat=1 is reserved for players who have run /trigger hat set 1
		for score, item in enumerate(items_file, 2):
			# split tabs and remove final newlines
			item = item.rstrip().split()
			yield Item(score, name=item[0], damage=item[1])


def commands_iter(items):
	
	yield from (
		'scoreboard players set @s[score_hat_min=1,score_hat=1] hat 0 {Inventory:[{Slot:103b}]}',
		'tellraw @s[score_hat_min=0,score_hat=0] {"text":"You already have something on your head.","color":"gray"}',
	)
	
	scoreboard_command='scoreboard players set @a[team=Donator,score_hat_min=1,score_hat=1] hat {score} {{SelectedItem:{{id:"minecraft:{name}",Damage:{damage}s}}}}'
	clear_command='clear @a[score_hat_min={score},score_hat={score}] minecraft:{name} {damage} 1'
	replaceitem_command='replaceitem entity @a[score_hat_min={score},score_hat={score}] slot.armor.head minecraft:{name} 1 {damage}'
	
	for item in get_items('item names.txt'):
		for command in (scoreboard_command, clear_command, replaceitem_command):
			yield command.format(
				score=item.score,
				name=item.name,
				damage=item.damage,
			)
	
	yield from (
		'tellraw @s[score_hat_min=1,score_hat=1] {"text":"Invalid item. You need to hold a custom hat in your hand.","color":"gray"}',
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
		for command in commands_iter(get_items()):
			f.write(command + '\n')



if __name__ == '__main__':
	name = 'null_byte:hat/equip'
	write_function(commands_iter(name), name)
