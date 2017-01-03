#!/usr/bin/env python3
# -*- coding: utf-8 -*-

scoreboard_command='/scoreboard players set @a[team=Donator,score_equiphat_min=0,score_equiphat=0] equiphat {item_id} {{SelectedItem:{{id:minecraft:{item_name},Damage:{item_damage},tag:{{display:{{Name:"Custom Hat"}}}}}}}}'

clear_command='/clear @a[score_equiphat_min={item_id},score_equiphat={item_id}] minecraft:{item_name} {item_damage} 1 {{display:{{Name:"Custom Hat"}}}}'

replaceitem_command='/replaceitem entity @a[score_equiphat_min={item_id},score_equiphat={item_id}] slot.armor.head minecraft:{item_name} 1 {item_damage} {{display:{{Name:"Custom Hat"]}}}}'

# http://stackoverflow.com/questions/10664856/make-dictionary-with-duplicate-keys-in-python
class Dictlist(dict):
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)

with open("item ids.txt") as item_ids_file:
	item_name_list = []
	item_id_list = []
	
	for line in item_ids_file:
		
		current_line=line[:-1].split("\t")
		
#		if len(current_line) == 3:
#			item_name_list.append(current_line[2])
#			
#			item_id_list.append((current_line[0], current_line[1]))
		if len(current_line) == 2:
			item_name_list.append(current_line[1])
			
			item_id_list.append(current_line[0]) # data value is assumed to be 0 if not present
			
	names_and_ids_dict = Dictlist(dict(zip(item_name_list, item_id_list)))
	
#	for item_name in item_name_list:
#	
#		for item_id in item_id_list:
#		
#			names_and_ids_dict.update({item_name: item_id})
			
with open("commands.txt", "w") as output_file:
	
	for item_id_name in names_and_ids_dict.keys():
		
		def write_command(command):
			output_file.write(command.format(item_name=item_id_name,
item_id=int(names_and_ids_dict.get(item_id_name)) + 1,
#item_damage=names_and_ids_dict.get(item_id_name)[1]) + "\n")
item_damage="0") + "\n")
		
		for command in [scoreboard_command, clear_command, replaceitem_command]:
			
			write_command(command)
			
		output_file.write("\n")
		
print(len(item_id_list))
		

