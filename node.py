import pygame as pg


class Node:
	def __init__(self, pos, direction, speed):
		self.pos = pg.math.Vector2(pos)
		self.dir = pg.math.Vector2(direction)
		# self.c = initial_c
		self.c = 255
		self.c_inc = 0.2
		self.speed = speed
		# self.screen_size = screen_size


	def update(self, screen, dt, speed_mult=1, size=3):
		self.move(screen, dt, speed_mult)

		pg.draw.circle(screen, (int(self.c), int(self.c), int(self.c)), self.pos, size)


	def move(self, screen, dt, speed_mult):
		if 5 >= self.pos.x:
			self.dir.x *= -1
			self.pos.x = 6
		if self.pos.x >= screen.get_size()[0]-5:
			self.dir.x *= -1
			self.pos.x = screen.get_size()[0]-6
		if 5 >= self.pos.y:
			self.dir.y *= -1
			self.pos.y = 6
		if self.pos.y >= screen.get_size()[1]-5:
			self.dir.y *= -1
			self.pos.y = screen.get_size()[1]-6

		if self.dir.magnitude() > 0:
			self.pos += self.dir.normalize() * (self.speed*speed_mult) * dt

		
