#!/usr/bin/env python3
# -*- coding: utf-8 -*-

scoreboard_command='/scoreboard players set @a[team=Donator,score_equiphat_min=0,score_equiphat=0] equiphat {score} {{SelectedItem:{{id:minecraft:{item_name},Damage:{item_damage}s}}}}'

clear_command='/clear @a[score_equiphat_min={score},score_equiphat={score}] minecraft:{item_name} {item_damage} 1'

replaceitem_command='/replaceitem entity @a[score_equiphat_min={score},score_equiphat={score}] slot.armor.head minecraft:{item_name} 1 {item_damage}'

# http://stackoverflow.com/questions/10664856/make-dictionary-with-duplicate-keys-in-python
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        else:
			self[key].append(value)

with open("item ids.txt") as item_ids_file:
	#num_lines = sum(1 for line in item_ids_file)
	items = []
	
	num_lines = 0

	for line in item_ids_file:
		
		print(line)
		current_line=line[:-1].split("\t")
		
		print(current_line)		

		if len(current_line) == 3:
			item_name, item_damage = current_line[2], current_line[1]
		else:
			item_name, item_damage = current_line[1], 0

		items.append({"id":item_name,"Damage":item_damage})

		num_lines += 1
			
	names_and_ids_dict = dict(zip([x + 2 for x in range(num_lines)], items))
	
#	for item_name in item_name_list:
#	
#		for item_id in item_id_list:
#		
#			names_and_ids_dict.update({item_name: item_id})

	
with open("commands.txt", "w") as output_file:
	
	for score in names_and_ids_dict.keys():
		
		def write_command(command):

			item = names_and_ids_dict.get(score)
			

			line = command.format(item_name=item.get("id"),
score=score, item_damage=item.get("Damage")) + "\n\n"


			"""Minecraft is a bit peculiar about tags: items with no damage don't
			have the Damage tag at all, rather than having a value of 0.
			So if the damage is 0, remove the tag altogether. This way the
			item we put on the player's head will be the same as one they created
			themselves."""
			line = line.replace("Damage:0s,", "")

			output_file.write(line)
			
			
		for command in [scoreboard_command, clear_command, replaceitem_command]:
			
			write_command(command)

