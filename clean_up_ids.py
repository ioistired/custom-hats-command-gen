#!/usr/bin/env python3
# encoding: utf-8

"""
Remove block ID numbers from item ids.txt
"""

with open("item ids.txt") as inf, open("item ids no ids.txt", 'w') as outf:
	for line in inf:
		line = line.rstrip().split('\t')
		
		# item id \t item name → item name 0 (no damage)
		if len(line) == 2:
			outf.write(line[1] + " 0" + '\n')
		# item id \t damage \t item name → item name damage
		if len(line) == 3:
			outf.write(line[2] + " " + line[1] + '\n')
