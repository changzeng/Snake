import curses,time
from random import randint

#initiall data
print("initiall data")
border_size = (22,22)
border = [[0 for i in range(border_size[0])] for j in range(border_size[1])]
print("initiall data done")

def map_border(input_num):
	if input_num == 0:
		return "  "
	elif input_num == 1:
		return "o "
	elif input_num == 2:
		return "@ "
	else:
		return "H "

def show_border():
	global ms
	global border
	global border_size
	for i in range(border_size[1]):
		#once I face a question is over the range of the region it can display
		#it make me puzzle and waste a lot of time
		ms.addstr(i+1,1,"".join(map(map_border,border[i])))
	ms.refresh()

class Snake(object):
	def __init__(self):
		global border_size
		global border
		border_width = border_size[0]
		border_height = border_size[1]
		self.body = []
		self.x = randint(0,border_height-1)
		self.y = randint(0,border_width-1)
		self.body.append([self.x,self.y])
		border[self.x][self.y] = 3

	def rand_egg(self):
		global score
		global border
		global border_size
		score += 1
		self.egg_x = randint(0,border_size[1]-1)
		self.egg_y = randint(0,border_size[0]-1)
		while border[self.egg_x][self.egg_y] != 0:
			self.egg_x = randint(0,border_size[1]-1)
			self.egg_y = randint(0,border_size[0]-1)
		border[self.egg_x][self.egg_y] = 2

	def move(self,direction):
		def next_step(x,y,x_i,y_i):
			global border_size
			return [(x+x_i+border_size[1])%border_size[1],(y+y_i+border_size[0])%border_size[0]]
		def go_to_next(x,y,x_i,y_i):
			global border
			tmp_next = next_step(x,y,x_i,y_i)
			if border[tmp_next[0]][tmp_next[1]] == 0:
				tmp_pop = self.body.pop(len(self.body)-1)
				border[tmp_pop[0]][tmp_pop[1]] = 0
				if len(self.body) == 0:
					self.body = [tmp_next,]
				else:
					border[self.body[0][0]][self.body[0][1]] = 1
					self.body.insert(0,tmp_next)
				border[self.body[0][0]][self.body[0][1]] = 3
			else:
				border[self.body[0][0]][self.body[0][1]] = 1
				self.body.insert(0,tmp_next)
				border[self.body[0][0]][self.body[0][1]] = 3
				self.rand_egg()
		def can_go(x,y,x_i,y_i):
			global ms
			global border
			if border[(x+x_i+border_size[1])%border_size[1]][(y+y_i+border_size[0])%border_size[0]]==0 or border[(x+x_i+border_size[1])%border_size[1]][(y+y_i+border_size[0])%border_size[0]]==2:
				ms.addstr(2,border_size[0]*2 + 2,"             ")
				ms.addstr(2,border_size[0]*2 + 2,"avialable")
				return True
			else:	
				ms.addstr(2,border_size[0]*2 + 2,"             ")
				ms.addstr(2,border_size[0]*2 + 2,"inavialable")
				return False
		if direction == 1:
			if can_go(self.body[0][0],self.body[0][1],-1,0):
				go_to_next(self.body[0][0],self.body[0][1],-1,0)
		elif direction == 2:
			if can_go(self.body[0][0],self.body[0][1],1,0):
				go_to_next(self.body[0][0],self.body[0][1],1,0)
		elif direction == 3:
			if can_go(self.body[0][0],self.body[0][1],0,1):
				go_to_next(self.body[0][0],self.body[0][1],0,1)
		elif direction == 4:
			if can_go(self.body[0][0],self.body[0][1],0,-1):
				go_to_next(self.body[0][0],self.body[0][1],0,-1)
	def get_direction(self):
		global ms
		ch_input = ms.getch()
		if ch_input == 65:
			self.move(1)
			return "up"
		elif ch_input == 66:
			self.move(2)
			return "down"
		elif ch_input == 67:
			self.move(3)
			return "right"
		elif ch_input == 68:
			self.move(4)
			return "left"
		else:	
			self.move(5)
			return "     "
	def get_way_BFS(self,des_x,des_y):
		global border
		global border_size
		direction = [[-1,0],[1,0],[0,1],[0,-1]]
		visited = []
		BFS_list = []
		x,y = self.body[0]
		BFS_list.append([[x,y],-1,-1])
		visit_tmp = []

		while len(BFS_list)>0:
			tmp = BFS_list.pop(0)
			visited.append(tmp)
			visit_tmp.append(tmp[0])
			for index,item in enumerate(direction):
				next_x = (tmp[0][0]+item[0]+border_size[1])%border_size[1]
				next_y = (tmp[0][1]+item[1]+border_size[0])%border_size[0]
				#sta = border[next_x][next_y]
				data = [[next_x,next_y],index+1,len(visited)-1]
				if next_x == des_x and next_y == des_y:	
					path = str(index + 1)
					if len(visited) == 1:
						return index + 1,path
					back_tmp = visited[-1]
					while self.body[0] != back_tmp[0]:
						back_tmp_t = back_tmp
						path += str(back_tmp[1])
						back_tmp = visited[back_tmp[2]]
					return back_tmp_t[1],path[::-1]
				else:
					if border[next_x][next_y]==0:
						if [next_x,next_y] not in visit_tmp:
							BFS_list.append(data)
							visit_tmp.append(data[0])
		return None,None

		
	def automaticly_move(self):
		des,path = self.get_way_BFS(self.egg_x,self.egg_y)
		if des == None:
			des = randint(1,4)
			path = des
		self.move(des)
		return des,path

def map_dire(dire):
	if dire == 1:
		return "up"
	elif dire == 2:
		return "down"
	elif dire == 3:
		return "right"
	elif dire == 4:
		return "left"
	else:
		return "None"
		
try:
	score = -1
	ms = curses.initscr()
	ms.border(0)
	s = Snake()
	s.rand_egg()
	show_border()
	ms.getch()
	step = 1
	direction = [[-1,0],[1,0],[0,1],[0,-1]]
	while True:
		#tmp_i = randint(1,4)
		#direc = s.get_direction()
		#ms.addstr(1,border_size[0]*2 + 2,direc)
		ms.addstr(3,border_size[0]*2 + 2,"step:"+str(step))
		dire,path = s.automaticly_move()
		ms.addstr(1,border_size[0]*2 + 2,"          ")
		ms.addstr(1,border_size[0]*2 + 2,"dir:"+map_dire(dire))
		ms.addstr(4,border_size[0]*2 + 2,"                              ")
		ms.addstr(4,border_size[0]*2 + 2,"path:"+str(path))
		ms.addstr(5,border_size[0]*2 + 2,"             ")
		if dire == None:
			next = None
			next_x = None
			next_y = None
			next_value = None
		else:		
			next = direction[dire-1]
			next_x = next[0]
			next_y = next[1]
			next_value = border[(s.body[0][0]+next[0]+border_size[1])%border_size[1]][(s.body[0][1]+next[1]+border_size[0])%border_size[0]]
		ms.addstr(5,border_size[0]*2 + 2,"next value:"+str(next_value))
		ms.addstr(6,border_size[0]*2 + 2,"     	  ")
		ms.addstr(6,border_size[0]*2 + 2,"dir:"+str(next_x)+"  "+str(next_y))
		ms.addstr(7,border_size[0]*2 + 2,"                      ")
		ms.addstr(7,border_size[0]*2 + 2,"Head:"+str(s.body[0][0])+" "+str(s.body[0][1]))
		ms.addstr(8,border_size[0]*2 + 2,"                      ")
		ms.addstr(8,border_size[0]*2 + 2,"Tail:"+str(s.body[-1][0])+" "+str(s.body[-1][1]))
		ms.addstr(9,border_size[0]*2 + 2,"               ")
		ms.addstr(9,border_size[0]*2 + 2,"score:"+str(score))
		show_border()
		time.sleep(0.02)
		step += 1
finally:
	curses.endwin()
