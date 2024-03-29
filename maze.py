import sys
import os
from random import randint
import random
import time
from time import sleep
import os
import sys
import scenes
import functions
import inventory
health = 100
CRED = '\033[91m'
CEND = '\033[0m'
CSTART = "\33[37m"

class TinyMazeEnv():

	# define status codes
	stepped = 1
	blocked = 2
	tree = 3
	character = 4
	won = 5
	quit = 6
	# define mazes
	mazes =	{ 
			  13: [ [ 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
			  		[ 4, 4, 4, 1, 0, 4, 4, 4, 4, 4, 4, 1, 1],
			  		[ 1, 0, 0, 0, 0, 1, 4, 4, 0, 4, 4, 1, 0],
			  		[ 1, 0, 1, 1, 3, 1, 0, 0, 0, 4, 1, 1, 0],
			  		[ 1, 0, 0, 1, 0, 0, 2, 1, 0, 0, 0, 0, 0],
			  		[ 4, 4, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],
			  		[ 4, 4, 0, 0, 1, 1, 0, 0, 0, 1, 3, 0, 0],
			  		[ 4, 1, 0, 0, 1, 1, 0, 2, 0, 0, 0, 1, 1],
			  		[ 4, 1, 1, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0],
			  		[ 0, 2, 0, 0, 1, 1, 3, 0, 0, 0, 1, 1, 1],
			  		[ 1, 0, 0, 0, 1, 1, 0, 0, 3, 0, 1, 0, 1],
			  		[ 1, 0, 1, 0, 0, 0, 2, 1, 1, 0, 1, 0, 1],
			  		[ 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0] ]
	
			}

	
	def __init__(self,maze_size=13):
		# initialize starting position and maze
		self.x = 6
		self.y = 8
		self.total_steps = 0
		if maze_size in self.mazes.keys():
			self.maze = self.mazes[maze_size]
		else:
			self.maze = self.mazes[5]
		self.maze_size = len(self.maze)

	def display_maze(self,move='None'):
		# display the maze in its current state
		functions.clear_screen()  	# clear screen
		functions.current_location(" ","x"," "," ",2)
		offset = " " * int((self.maze_size-5) * 1.5)
		functions.display_health(health)
		print("---" * (self.maze_size + 2))
		print("       w: up s: down a: left d: right\n")
		print(offset + "     b: backpack")
		print("---" * (self.maze_size + 2))
		for i in range(self.maze_size):
			row = "   "
			for j in range(self.maze_size):
				if i == self.y and j == self.x: 
					row += CRED+" U "+CEND
				elif self.maze[i][j] == 1: 
					row += " # "
				elif self.maze[i][j] == 2:
					row += " T "
				elif self.maze[i][j] == 3:
					row += CSTART+" x "+CEND
				elif self.maze[i][j] == 4:
					row += "   "
				else: 
					row += " . "
			print(row)
			
	def step(self,move):
		# process a single action
		offset = " " * int((self.maze_size-5) * 1.5)
		self.total_steps += 1
		status = self.blocked
		if move == "a":
			if (self.x > 0) and (self.maze[self.y][self.x-1] != 1) and (self.maze[self.y][self.x-1] != 4): 
				self.x -= 1
				status = self.stepped
		elif move == "d":
			if (self.x < self.maze_size-1) and (self.maze[self.y][self.x+1] != 1) and (self.maze[self.y][self.x+1] != 4): 
				self.x += 1
				status = self.stepped
		elif move == "w":
			if (self.y > 0) and (self.maze[self.y-1][self.x] != 1) and (self.maze[self.y-1][self.x] != 4): 
				self.y -= 1
				status = self.stepped
		elif move == "s":
			if (self.y < self.maze_size-1) and (self.maze[self.y+1][self.x] != 1) and (self.maze[self.y+1][self.x] != 4): 
				self.y += 1
				status = self.stepped
		elif move == "b":
			os.system('cls')
			inventory.display_inventory()
			self.maze[self.y][self.x] = 10
		elif move == "Q":
			status = self.quit

		#Check for tree
		if self.maze[self.y][self.x] == 2:
			status=self.tree
			self.maze[self.y][self.x] = 10

		#Check for character 
		if self.maze[self.y][self.x] == 3:
			status=self.character

		return status

	def play(self):
		self.display_maze()
		offset = " " * int((self.maze_size-5) * 1.5)
		while True:
			if sys.version_info[0] < 3:
				move = raw_input("command: ")
			else:
				move = input("command: ")
			status = self.step(move)

			if status == self.quit: 
				print("You quit.")
				break
			elif status == self.tree:
				randomwood = randint(3, 15)
				randomfruit = randint(0, 2)
				print("You found "+str(randomwood)+" wood")
				print("You found "+str(randomfruit)+" fruit")
				inventory.add_item("wood", randomwood)
				inventory.add_item("fruit", randomfruit)
			elif status == self.character:
				scenes.meetCaptainJack()
			else: 
				self.display_maze(move)

