import sys
import os
import random
import time
from time import sleep
import os
import sys
import scenes
import functions
import inventory

class TinyMazeEnv():
	
	# define status codes
	stepped = 1
	blocked = 2
	raining = 3
	won = 4
	quit = 5
	rain = False
	health = 100
	#Define colors
	CBLUE = '\33[34m'
	CRED = '\033[91m'
	CSTART = "\33[37m"
	CBEIGE = '\33[93m'
	CEND = '\033[0m'
	# define mazes
	mazes =	{ 
			  13: [ [ 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4],
			  		[ 4, 4, 3, 3, 3, 4, 0, 4, 4, 0, 4, 1, 1],
			  		[ 4, 0, 3, 3, 3, 1, 0, 4, 0, 0, 4, 2, 1],
			  		[ 4, 0, 1, 1, 3, 1, 0, 0, 0, 4, 1, 0, 1],
			  		[ 4, 4, 0, 1, 0, 0, 0, 1, 0, 3, 3, 3, 4],
			  		[ 3, 3, 1, 0, 0, 1, 0, 1, 1, 1, 3, 3, 4],
			  		[ 3, 3, 0, 0, 1, 1, 0, 0, 0, 1, 3, 4, 4],
			  		[ 3, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 4],
			  		[ 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
			  		[ 0, 0, 1, 0, 1, 1, 3, 0, 0, 0, 1, 0, 1],
			  		[ 4, 0, 1, 0, 1, 1, 3, 3, 3, 4, 1, 0, 1],
			  		[ 4, 0, 1, 0, 0, 0, 3, 3, 3, 4, 4, 0, 4],
			  		[ 4, 4, 1, 0, 1, 0, 0, 4, 4, 4, 4, 4, 4] ],

			}

	
	def __init__(self,maze_size=13):
		# initialize starting position and maze
		self.x = 1
		self.y = 11
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
		functions.display_health(self.health)
		print("---" * (self.maze_size + 2))
		print("       w: up s: down a: left d: right\n")
		print("         b: backpack  f: eat fruit")
		print("---" * (self.maze_size + 2))
		for i in range(self.maze_size):
			row = "   "
			for j in range(self.maze_size):
				if i == self.y and j == self.x: 
					row += self.CRED+" U "+self.CEND
				elif self.maze[i][j] == 1: 
					row += self.CSTART+" # "+self.CEND
				elif self.maze[i][j] == 2:
					row += "\33[37m"+" x "+self.CEND
				elif self.maze[i][j] == 3:
					row += self.CBEIGE+" c "+self.CEND
				elif self.maze[i][j] == 4:
					row += "   "
				else: 
					row += self.CSTART+" . "+self.CEND
			if(self.total_steps <= 10):
				print(row)
			#RAINING
			elif(self.total_steps <= 20):
				self.CSTART = self.CBLUE 
				self.rain = True
				print(row)	
			else:
				self.CSTART = "\33[37m"
				self.total_steps = 0
				self.rain = False

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
			inventory.display_inventory()
			self.maze[self.y][self.x] = 10

		elif move == "f":
			inventory.remove_item("fruit", 1)
			self.health += 5

		elif move == "Q":
			status = self.quit

		#Check if user is not the cave
		if self.maze[self.y][self.x] != 3 and self.rain == True and move != "f":
			self.health -= 5


		return status

	def play(self):
		self.display_maze()
		offset = " " * int((self.maze_size-5) * 1.5)
		while True:
			if sys.version_info[0] < 3:
				move = raw_input("Command: ")
			else:
				move = input("Command: ")
			status = self.step(move)

			if status == self.quit: 
				print("You quit.")
				break
			elif status == self.raining:
				print("Seek shelter")
			else: 
				self.display_maze(move)

