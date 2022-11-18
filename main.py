import pygame as pg
from random import randint, random
from node import Node
import math
import pygame_gui

pg.freetype.init()

width, height = 800, 600
screen = pg.display.set_mode((width, height), pg.RESIZABLE)
manager = pygame_gui.UIManager((width, height))
clock = pg.time.Clock()

pg.font.init()

nodes = []
node_amount = 0
node_range = 200
node_speed_mult = 1
node_size = 3
node_last_spdmult = node_speed_mult
custom_color = (255,255,255)

font = pg.font.SysFont('Lucida Console', 14)

pause = False
show_dist = True

color_current = 0
scheme_amount = 5

for i in range(node_amount):
	nodes.append(Node( 
		(randint(100, width-100), randint(100, height-100)), # Pos x and y
		(random()-.5, random()-.5), # direction
		randint(60,100))) # speed

win_setup = pygame_gui.elements.UIWindow(rect=pg.Rect( (10,10), (270,500) ), manager=manager,
	window_display_title='[ESC] Setup' )

# wtf that worked?
def dont_kill():
	win_setup.hide()

win_setup.on_close_window_button_pressed = dont_kill
# ¯\_(ツ)_/¯

lbl_node_amount = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (10,10),(90,30) ),
	manager=manager, container=win_setup, text='Node Amount')
txt_node_amount = pygame_gui.elements.UITextEntryLine(relative_rect=pg.Rect( (110,10),(40,30) ),
	manager=manager, container=win_setup)
txt_node_amount.set_allowed_characters('numbers')
txt_node_amount.length_limit=3
btn_set = pygame_gui.elements.UIButton(relative_rect=pg.Rect( (150, 10),(80,30) ),
	manager=manager, container=win_setup, text='SET')


lbl_node_range = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (10,45),(230,30) ),
	manager=manager, container=win_setup, text='Node Range')
lbl_current_range = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (5,70),(48,30) ),
	manager=manager, container=win_setup, text='200')
slider_node_range = pygame_gui.elements.UIHorizontalSlider(relative_rect=pg.Rect( (60,70),(170,30) ),
	manager=manager, container=win_setup, start_value=200,
	value_range=(50, 1000), click_increment=10)

lbl_speed = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (0,105),(250,30) ),
	manager=manager, container=win_setup, text='Node Speed')
lbl_current_speed = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (5,130),(48,30) ),
	manager=manager, container=win_setup, text='1')
slider_speed = pygame_gui.elements.UIHorizontalSlider(relative_rect=pg.Rect( (60,130),(170,30) ),
	manager=manager, container=win_setup, start_value=1.0,
	value_range=(0.25, 10), click_increment=0.25)

lbl_size = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (0,165),(240,30) ),
	manager=manager, container=win_setup, text='Node Size')
lbl_current_size = pygame_gui.elements.UILabel(relative_rect=pg.Rect( (5,190),(48,30) ),
	manager=manager, container=win_setup, text='3')
slider_size = pygame_gui.elements.UIHorizontalSlider(relative_rect=pg.Rect( (60,190),(170,30) ),
	manager=manager, container=win_setup, start_value=3.0,
	value_range=(0.0, 10.0), click_increment=1)

check_distances = pygame_gui.elements.UIButton(relative_rect=pg.Rect( (10,230),(220,30) ),
	manager=manager, container=win_setup, text='[X] Show Distances')

current_color = 'Red/Green'
drop_color = pygame_gui.elements.UIDropDownMenu(relative_rect=pg.Rect( (10,270), (220,30) ),
	manager=manager, container=win_setup, options_list=['Red/Green', 'Cyan', 'Magenta', 'Yellow', 'White', 'Custom'], starting_option=current_color)

btn_pickcolor = pygame_gui.elements.UIButton(relative_rect=pg.Rect( (10,300), (220,30) ), 
	text='Pick Color', manager=manager, container=win_setup)
btn_pickcolor.disable()
# print(drop_color.selected_option)

btn_pause = pygame_gui.elements.UIButton(relative_rect=pg.Rect( (10,340), (220,30) ), 
	text='Pause', manager=manager, container=win_setup, tool_tip_text='Pause simulation')

# btn_start = pygame_gui.elements.UIButton(relative_rect=pg.Rect( (125,210), (105,30) ), 
# 	text='Start', manager=manager, container=win_setup, tool_tip_text='Start simulation')



while True:
	dt = clock.tick()/1000
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			exit()
		elif event.type == pg.VIDEORESIZE:
			width, height = event.w, event.h
			screen = pg.display.set_mode((width, height), pg.RESIZABLE)
			manager.set_window_resolution((width, height))

		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				if win_setup.visible:
					win_setup.hide()
				else:
					win_setup.show()

			elif event.key == pg.K_SPACE:
				# pause
				if node_speed_mult == 0:
					node_speed_mult = node_last_spdmult
					btn_pause.set_text('Pause')
				else:
					node_last_spdmult = node_speed_mult
					node_speed_mult = 0
					btn_pause.set_text('Resume')

			elif event.key == pg.K_F1:
				show_dist = not show_dist
				if show_dist:
					check_distances.set_text('[X] Show Distances')
				else:
					check_distances.set_text('[ ] Show Distances')

			elif event.key == pg.K_F2:
				color_current += 1
				if color_current >= scheme_amount:
					color_current = 0
	
		elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
			if event.ui_element == slider_speed:
				lbl_current_speed.set_text(str(slider_speed.get_current_value()))
				node_speed_mult = slider_speed.get_current_value()
				btn_pause.set_text('Pause')
			elif event.ui_element == slider_node_range:
				lbl_current_range.set_text(str(slider_node_range.get_current_value()))
				node_range = slider_node_range.get_current_value()
			elif event.ui_element == slider_size:
				lbl_current_size.set_text(str(slider_size.get_current_value()))
				node_size = slider_size.get_current_value()

						
		elif event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == check_distances:
				show_dist = not show_dist
				if show_dist:
					check_distances.set_text('[X] Show Distances')
				else:
					check_distances.set_text('[ ] Show Distances')
			elif event.ui_element == btn_pause:
				if node_speed_mult == 0:
					node_speed_mult = node_last_spdmult
					btn_pause.set_text('Pause')
				else:
					node_last_spdmult = node_speed_mult
					node_speed_mult = 0
					btn_pause.set_text('Resume')
			elif event.ui_element == btn_set:
				node_amount = int(txt_node_amount.get_text())
				nodes.clear()
				for i in range(node_amount):
					nodes.append(Node(
						(randint(100, width-100), randint(100, height-100)), # Pos x and y
						(random()-.5, random()-.5), # direction
						randint(60,100))) # speed
			elif event.ui_element == btn_pickcolor:
				colorpicker = pygame_gui.windows.UIColourPickerDialog(pg.Rect(160, 50, 420, 400),
                                                              manager,
                                                              window_title='Change Colour...',
                                                              initial_colour=pg.Color(custom_color))
											
		elif event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
			custom_color = event.colour

		elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
			if event.ui_element == drop_color:
				current_color = event.text
				if event.text == 'Custom':
					btn_pickcolor.enable()
				else:
					btn_pickcolor.disable()

		manager.process_events(event)
	# if pause:
	# 	continue
	screen.fill((0,0,0))


	for node1 in nodes:
		dist = 0
		for node2 in nodes:
			if node1 != node2:
				dist = (node2.pos.x - node1.pos.x)**2 + (node2.pos.y - node1.pos.y)**2
				if dist < node_range**2:
					c = int(( (dist*255) / node_range**2) )
					d = c
					c = 255-c
					if show_dist:
						txt =  font.render(str(int(math.sqrt(dist))), True, (255,255,255))
						screen.blit(txt, ( (node1.pos.x + node2.pos.x)//2, (node1.pos.y + node2.pos.y)//2 ))
					if current_color == 'Custom':
						r, g, b = ( custom_color[0] - int(( (dist*custom_color[0]) / node_range**2) ), 
									custom_color[1] - int(( (dist*custom_color[1]) / node_range**2) ), 
									custom_color[2] - int(( (dist*custom_color[2]) / node_range**2) ))
						pg.draw.line(screen, (r, g, b), node1.pos, node2.pos)
					elif current_color == 'Red/Green':
						pg.draw.line(screen, (d,c,40), node1.pos, node2.pos)
					elif current_color == 'Cyan':
						pg.draw.line(screen, (0,c,c), node1.pos, node2.pos)
					elif current_color == 'Magenta':
						pg.draw.line(screen, (c,0,c), node1.pos, node2.pos)
					elif current_color == 'Yellow':
						pg.draw.line(screen, (c,c,0), node1.pos, node2.pos)
					elif current_color == 'White':
						pg.draw.line(screen, (c,c,c), node1.pos, node2.pos)



	for node in nodes:
		node.update(screen, dt, node_speed_mult, node_size)

	manager.update(dt)
	manager.draw_ui(screen)
	pg.display.update()