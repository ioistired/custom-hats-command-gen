#!/usr/bin/env python3
# encoding: utf-8
# 
# MIT Licensed
# https://bmintz.mit-license.org/@2017

SCOREBOARD_COMMAND='/scoreboard players set @a[team=Donator,score_equiphat_min=0,score_equiphat=0] equiphat {score} {{SelectedItem:{{id:minecraft:{item_name},Damage:{item_damage}s}}}}'

CLEAR_COMMAND='/clear @a[score_equiphat_min={score},score_equiphat={score}] minecraft:{item_name} 1 {item_damage}'

REPLACEITEM_COMMAND='/replaceitem entity @a[score_equiphat_min={score},score_equiphat={score}] slot.armor.head minecraft:{item_name} 1 {item_damage}'


def commands_iter(input_filename='item names.txt'):
	with open(input_filename) as items_file:
		for score, item in enumerate(items_file, 1):
			item = item.rstrip().split()
			
			for command in (SCOREBOARD_COMMAND, CLEAR_COMMAND, REPLACEITEM_COMMAND):
				yield command.format(
						score=score,
						item_name=item[0],
						item_damage=item[1],
				)

def write_commands(input_filename='', output_filename='commands.txt'):
	with open(output_filename, 'w') as outfile:
		if not len(input_filename):
			for command in commands_iter():
				outfile.write(command + '\n')
		else:
			# TODO deduplicate
			for command in commands_iter(input_filename):
				outfile.write(command + '\n')


if __name__ == '__main__':
	write_commands()
