# Home creation tool, converts 2D building plans into 3D virtual walkthroughs - Desigining and simulation
# Can upload any images, add textures, easily modify code, etc
# Copyright (c) 2023-2026 henrymcneill
# Accompanying mentor for giving ray casting theory: Eric VON AARBURG
# Licensed under the MIT License - See the LICENSE document,
# more details on GitHub at https://github.com/mcneill-h/Home-Designer

from Final_Simulation_3D_definition import*
# import code file with definitions (functions)

import pygame

## OPTIONAL: VALUE TO CHANGE FOR DEVELOPPERS:
Nb_walls = 50 # numbers of walls on each x and y axis (can easily go up to 500)
# determines how big the simulation will be

## Starting Parameters:
wall_length = 600/Nb_walls # length of walls

watch_angle_degrees = 0 # the direction of the player's field of view

beta_fisheye = 80 # beta angle to correct fishbowl effect (search on internet) (very particular)
wall_distance_constant = 12500/Nb_walls # value to determine the height of the walls --> distance of player to fictive wall * height of wall
# proportionally changes in function of the height of the walls

sprite_pos_x = 200
sprite_pos_y = 200

sprite_speed = 32/Nb_walls


##Image analysis to scan the building plan:
blur_image()

bloc_liste = scan_image(Nb_walls, wall_length)
# func to scan image and determine the position of walls

H_walls_pos, V_walls_pos = walls_liste(Nb_walls, bloc_liste)
# func to create lists composed of the position of all horizontal and vertical walls


## Variables to launch pygames:
fps = 30
clock = pygame.time.Clock() # raccourci pour mettre en place les fps (temps)
screen_size = [600,600] # in pixel
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Wall editing menue')


## Launch the editing screen for walls and textures (can add and delete walls)

print(" ")
print("Welcome to the editing menu!")
print("Add, Remove or texturise walls by clicking on them with your mouse!")
print("White --> no wall")
print("Black --> wall (with no textures)")
print("Blue --> wall with the texture of a living room window")
print("Purple --> wall with the texture of a cobbled basement wall")
print(" ")

print("Press the Enter key to launch the 3D simulation!")
print(" ")

run = True
while run==True:
    clock.tick(fps)
    
    screen.fill( (252, 252, 252)) # background color
    
    H_walls_pos, V_walls_pos, run = walls_modifications(Nb_walls, wall_length, H_walls_pos, V_walls_pos, run, screen)
    # displays the walls and enable their modifications
    
    pygame.display.update()


## Launching the 3D Simulation:
screen_size = [1200,600] # in pixel
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Ray casting 3D Simulation')

print("################")
print("Here is a digital 3D simulation (based on an building plan we scanned)")
print("(you can change which image is scanned in the Final_Simulation_3D_definition.py code in line 25)")
print("Use WASD keys for movement")
print("O and K keys to increase/decrease the height of the walls")
print("P and L keys to increase/decrease the player's mouvement speed")

print("")
print("Go visit the floor!")

run = True  
while run==True:
    clock.tick(fps)
    
    background_3D(screen)
    # draw ground and ceiling background
    
    sprite_pos_x, sprite_pos_y, sprite_speed, watch_angle_degrees, wall_distance_constant, run= user_interactions(sprite_pos_x, sprite_pos_y,
                                                                                        sprite_speed, watch_angle_degrees, wall_distance_constant, run, screen)
    # detects player inputs
    
    simulation_3D(watch_angle_degrees, wall_length, H_walls_pos, V_walls_pos, sprite_pos_x, sprite_pos_y,
                                        Nb_walls, beta_fisheye, wall_distance_constant, screen)
    # ray casting math operations (determines collisions and displays the 3D walls)
    
    mini_map_2D(Nb_walls, wall_length, H_walls_pos, V_walls_pos, screen)
    # displays the 2D mini-map
    
    pygame.draw.circle(screen, "black",[sprite_pos_x/3, sprite_pos_y/3],3)
    # draws the player on the mini map
    
    pygame.display.update()


pygame.quit()
quit()
