# THIS IS THE SECONDARY CODE FILE, DEVELOPERS NEED TO LAUNCH THE SIMULATION FROM THE MAIN FILE: "Final_simulation_3D.py"
# Home creation tool, converts 2D building plans into 3D virtual walkthroughs - Desigining and simulation
# Can upload any images, add textures, easily modify code, etc
# Copyright (c) 2023-2026 henrymcneill
# Accompanying mentor for giving ray casting theory: Eric VON AARBURG
# Licensed under the MIT License - See the LICENSE document, more details on GitHub at https://github.com/mcneill-h/Home-Designer

import pygame

from pygame.locals import (K_w, K_a, K_d, K_s, K_p, K_l, K_o, K_k, K_SPACE, K_ESCAPE, K_RETURN)

import math

from PIL import Image, ImageFilter
#librairie pour modifier une image

import imageio.v3 as imageio
#librairie pour identifier le RGB d'un pixel 

## Listes des definitions ##
def blur_image(): # flouter l'image

    ######### OPTIONAL: ###########
    # CHANGE THE NAME OF THE IMAGE TO LOAD IN OTHER BUILDING FLOORS YOU WANT TO RECREATE IN THE SIMULATION
    image = Image.open('Image11.png').convert('RGB')

    image = image.resize((1500, 1500))
    blurImage = image.filter(ImageFilter.BLUR)
    blurImage = blurImage.resize((600, 600)) # redimensionner l'image
    blurImage.save('blurImage.png')
    

def scan_image(Nb_walls,wall_length): # scan image and digitalise the building plan into a list
    # Theory: when a pixel (from the building plan) is scanned and identified as being part of a wall, the program will add a "block" of walls on top of the pixel in the simulation
    # this "bloc" is equivalent as having 4 walls surrounding the pixel in a square shape.
    # Therefore, this function makes a list of the location of all "block of walls", which will later be divided into individual walls.
    # WHY not diretly add a wall where the obstacle is? instead of using "block of walls" and converting them into walls?
    # ANSWER: --> "blocks of walls" guarantees that we can have straight and uniform walls in our simulation. When adding a single wall instead of a "block", we do not know in which direction we should place it (horizontally or vertically). Making the resulat chaotic.

    ## SIGNIFICATIONS:
    ## 0 --> a bloc of walls is not present
    ## 1 --> a bloc of walls is present
    
    bloc_liste= [] # list to define where all blocs of walls are placed
    # fills bloc_liste based on the number of walls the simulation will have
    for i in range (Nb_walls * Nb_walls):
        bloc_liste.append(0) 
    
    blurImage = imageio.imread('blurImage.png')
    x = int(wall_length/2) # horizontal position of the pixel we are scanning
    y = int(wall_length/2) # vertical position of the pixel we are scanning
    
    # checks RGB of pixels to know if there is a block of wall:
    for row in range (Nb_walls):
        for column in range (Nb_walls):
            
            if (int(blurImage[y,x,0])+int(blurImage[y,x,1])+int(blurImage[y,x,2])) <= 350:

                bloc_liste [(row*Nb_walls) + column] =1
                
            x += int(wall_length)
        x = int(wall_length/2)
        y += int(wall_length)
        
    return (bloc_liste) 
    

def walls_liste(Nb_walls,bloc_liste):
    # divides the "block of walls" liste into 2 lists with all: 1. horizontal walls 2. vertical walls
    # so that we can add and delete every single walls of the simulation

    ## SIGNIFICATIONS:
    ## 0 --> a bloc of walls is not present
    ## 1 --> a bloc of walls is present
    
    V_walls_pos = [1] # V_walls_pos represents Vertical walls from left to right, row by row
    H_walls_pos = [1] # H_walls_pos represents Horizontal walls from top to bottom, column by column

    offset_correction = 0

    # For vertical walls:
    for n_th_bloc in range (len(bloc_liste)):

        if bloc_liste[n_th_bloc]==1:
            V_walls_pos[n_th_bloc+offset_correction]= 1
        
        # If we are at the beginning of a row:
        if (n_th_bloc)%(Nb_walls)== 0 and n_th_bloc !=0 :
            V_walls_pos[n_th_bloc+offset_correction]= 1
            V_walls_pos.append(1) # adds a wall at the external border of the simulation
            offset_correction += 1

        V_walls_pos.append(bloc_liste[n_th_bloc])
        
    V_walls_pos [len(V_walls_pos)-1] = 1

    
    offset_correction = 0

    # For horizontal walls:
    for n_th_column in range (Nb_walls):
        for n_th_row in range (Nb_walls):
            

            if bloc_liste[(Nb_walls*n_th_row)+ n_th_column]==1:
                H_walls_pos[n_th_row+offset_correction+(n_th_column*Nb_walls)]= 1
            
            # If we are at the beginning of a column:
            if (n_th_row)%(Nb_walls)==0 and n_th_column !=0:
                H_walls_pos[n_th_row+offset_correction+(n_th_column*Nb_walls)]= 1 # activer le mur de fin de colonne (celle précédente)
                H_walls_pos.append(1) # adds a wall at the external border of the simulation
                offset_correction+=1

            H_walls_pos.append(bloc_liste[n_th_column+(Nb_walls*n_th_row)])
            
    H_walls_pos [len(H_walls_pos)-1]=1
    
    return (H_walls_pos,V_walls_pos)
    

def walls_modifications(Nb_walls,wall_length,H_walls_pos,V_walls_pos,run,screen):
    # for the editing menue before strating the simulation
    # lets user add, remove and give textures to walls

    ## SIGNIFICATIONs:
    ## 0 --> no wall
    ## 1 --> wall is activated (with plain texture)
    ## 2 --> wall is activated (with pre-made "window" texture)
    ## 3 --> wall is activated (with pre-made "cobblestone" texture)
    
    keys = pygame.key.get_pressed()
    
    x, y = -500, -500
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

        if keys[K_SPACE]==True or keys[K_RETURN]==True or keys[K_ESCAPE]==True:
            run = False

    # Generate and change values for vertical walls:
    for n_th_column in range (Nb_walls):
        for n_th_row in range (Nb_walls+1):
            # 1 If the wall is activated (with plain texture):
            if H_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row]==1:
                
                line = pygame.draw.line(screen,"black",[(wall_length)*n_th_column,(wall_length)*n_th_row],
                                        [(wall_length)+(wall_length)*n_th_column,(wall_length)*n_th_row],8)
                
                if line.collidepoint(x, y):
                    H_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row]=2
                    # changer la texture du mur au numéro 2:
                    
            # 2 If the wall is activated (with pre-made "window" texture):
            elif H_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row]==2:
                
                line = pygame.draw.line(screen,"blue",[(wall_length)*n_th_column,(wall_length)*n_th_row],
                                        [(wall_length)+(wall_length)*n_th_column,(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    H_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row]=3

            # 3 If the wall is activated (with pre-made "cobblestone" texture):
            elif H_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row]==3:
                
                line = pygame.draw.line(screen,"purple",[(wall_length)*n_th_column,(wall_length)*n_th_row],
                                        [(wall_length)+(wall_length)*n_th_column,(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    H_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row] = 0
                    
            # 0 If there is no wall (desactivated):
            else:
                
                line = pygame.draw.line(screen,"white",[(wall_length)*n_th_column,(wall_length)*n_th_row],
                                        [(wall_length)+(wall_length)*n_th_column,(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    H_walls_pos[n_th_row+((Nb_walls+1)*n_th_column)]=1
                    
            
    # Generate and change values for vertical walls:
    for n_th_row in range (Nb_walls):
        for n_th_column in range (Nb_walls+1):
            # 1 If the wall is activated (with plain texture):
            if V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]==1:
                
                line = pygame.draw.line(screen,"black",[(wall_length)*n_th_column, (wall_length)*n_th_row],
                                        [(wall_length)*n_th_column,(wall_length)+(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]=2

            # 2 If the wall is activated (with pre-made "window" texture):
            elif V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]==2:
                
                line = pygame.draw.line(screen,"blue",[(wall_length)*n_th_column, (wall_length)*n_th_row],
                                        [(wall_length)*n_th_column,(wall_length)+(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]=3

            # 3 If the wall is activated (with pre-made "cobblestone" texture):
            elif V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]==3:
                
                line = pygame.draw.line(screen,"purple",[(wall_length)*n_th_column, (wall_length)*n_th_row],
                                        [(wall_length)*n_th_column,(wall_length)+(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]=0

            # 0 If there is no wall (desactivated):
            else:
                
                line = pygame.draw.line(screen,"white",[(wall_length)*n_th_column, (wall_length)*n_th_row],
                                        [(wall_length)*n_th_column,(wall_length)+(wall_length)*n_th_row],8)

                if line.collidepoint(x, y):
                    
                    V_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]=1

    
    return (H_walls_pos,V_walls_pos,run)

    
def background_3D(screen):

    screen.fill((210,210,190))
    pygame.draw.rect(screen, (128,128,128), pygame.Rect(0, 0, 1200, 300),  width=0)


def user_interactions(sprite_pos_x,sprite_pos_y,sprite_speed,watch_angle_degrees,wall_distance_constant,run,screen):

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if keys[K_ESCAPE]==True:
            run = False
    
    if keys[K_p]==True:
        sprite_speed = sprite_speed*1.2
    
    elif keys[K_l]==True:
        sprite_speed = sprite_speed/1.2
    
    
    if keys[K_o]==True:
        wall_distance_constant = wall_distance_constant*1.2
    
    elif keys[K_k]==True:
        wall_distance_constant = wall_distance_constant/1.2
    
    pygame.mouse.set_pos([600, 300])
    pygame.mouse.set_visible(False)

    # FOV angle:
    mouse_mouvement  = pygame.mouse.get_rel()

    if mouse_mouvement[0]>0:
        watch_angle_degrees += 2*mouse_mouvement[0]
    
    elif mouse_mouvement[0]<0:
        watch_angle_degrees += 2*mouse_mouvement[0]


    if watch_angle_degrees>=3600:
        watch_angle_degrees-=3600
    
    elif watch_angle_degrees<0:
        watch_angle_degrees+=3600

    angle_centre=(watch_angle_degrees+600)/10

    if angle_centre>=360:
        angle_centre-=360
    
    elif angle_centre<0:
        angle_centre+=360
    
    # Mouvement
    if keys[K_w]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_centre))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_centre))

    elif keys[K_s]==True:
        sprite_pos_x -= sprite_speed* math.cos(math.radians(angle_centre))
        sprite_pos_y -= sprite_speed* math.sin(math.radians(angle_centre))

    elif keys[K_d]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_centre+90))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_centre+60))

    elif keys[K_a]==True:
        sprite_pos_x += sprite_speed* math.cos(math.radians(angle_centre-90))
        sprite_pos_y += sprite_speed* math.sin(math.radians(angle_centre-90))
    

    return (sprite_pos_x,sprite_pos_y, sprite_speed, watch_angle_degrees, wall_distance_constant,run)


def mini_map_2D(Nb_walls,wall_length,H_walls_pos,V_walls_pos,screen):
    # generates minimap that is on the top left of the simulation

    # Generates horizontal walls:
    for n_th_column in range (Nb_walls):
        for n_th_row in range (Nb_walls+1):

            if V_walls_pos[((Nb_walls+1)*n_th_column)+n_th_row]:
                pygame.draw.aaline(screen,"black",[((wall_length)*n_th_row)/3, ((wall_length)*n_th_column)/3],
                                   [((wall_length)*n_th_row)/3,((wall_length)+(wall_length)*n_th_column)/3],3)

    # Generates vertical walls:
    for n_th_row in range (Nb_walls):
        for n_th_column in range (Nb_walls+1):

            if H_walls_pos[((Nb_walls+1)*n_th_row)+n_th_column]:
                pygame.draw.aaline(screen,"black",[((wall_length)*n_th_row)/3,((wall_length)*n_th_column)/3],
                                   [((wall_length)+(wall_length)*n_th_row)/3,((wall_length)*n_th_column)/3],3)

 
def simulation_3D(watch_angle_degrees,wall_length,H_walls_pos,V_walls_pos,sprite_pos_x,sprite_pos_y,Nb_walls,beta_fisheye,
                 wall_distance_constant,screen):
    # Ray casting computations & 3D wall generator
    
    # For every rays that forms the FOV:
    for n_th_angle in range (watch_angle_degrees, watch_angle_degrees +1200, 1):
        # number of rays used to create the simulation --> 1200 (120 degree FOV)
        # we cannot use float numbers for "for i in range", therefore we are converting 120 degrees in 1200 to have "decimals"

        n_th_angle_degree = n_th_angle - watch_angle_degrees

        n_th_angle = n_th_angle/10 #real degree value

        if n_th_angle >= 360:
            n_th_angle -= 360
        
        elif n_th_angle<0:
            n_th_angle += 360

        wall_distance = 100000
        
        if_vertical_collision = False
        if_horizontal_collision = False


        Y_distance_constant = wall_length * math.tan(math.radians(n_th_angle))
        # regular Y distance between each intersection

        ## Detect vertical wall collisions:
        # if the ray is oriented towards the right side of the map:
        if n_th_angle < 90 or n_th_angle > 270:
            
            first_coords_X = int(sprite_pos_x/wall_length)*wall_length + wall_length
            # X value of the first intersection
            
            first_coords_Y = sprite_pos_y + (sprite_pos_x-first_coords_X)* math.tan(math.radians(-n_th_angle))
            # Y coords of the first intersection
            
            n_th_column = int(first_coords_X/wall_length) -1

            # Check if there is a wall on each possible intersection:
            while n_th_column <= (Nb_walls-1):
                
                n_th_row = int(first_coords_Y/wall_length)

                # if there is a wall placed there:
                if 0 <= n_th_row < Nb_walls and V_walls_pos[n_th_row*(Nb_walls+1)+n_th_column+1]!=0:
                    
                    wall_distance = (((sprite_pos_x - (n_th_column*(wall_length)+ wall_length))**2)
                                                  + ((sprite_pos_y- first_coords_Y)**2))**(1/2)

                    n_th_column_sauvegarde = n_th_column
                    n_th_row_sauvegarde = n_th_row
                    
                    if_vertical_collision = True
                    n_th_column= Nb_walls+ 1 # To go out of the "while" loop
                    
                    # Correct the fishbowl effect:
                    if n_th_angle > 270:

                        alpha_mur_vertical= beta_fisheye

                    else:

                        alpha_mur_vertical= -beta_fisheye

                else:

                    n_th_column+=1
                    first_coords_Y += Y_distance_constant

        # if the ray is oriented towards the left side of the map:
        elif n_th_angle !=90 and 270:
            
            first_coords_X = int(sprite_pos_x/wall_length)*wall_length
            # X coords of the first intersection
            
            first_coords_Y = sprite_pos_y + (sprite_pos_x-first_coords_X)* math.tan(math.radians(-n_th_angle))
            # Y coords of the first intersection
            
            n_th_column= int(first_coords_X/wall_length) -1

            # Check if there is a wall on each possible intersection:
            while n_th_column >= -1:
                
                n_th_row = int(first_coords_Y/wall_length)

                # if there is a wall placed there:
                if 0<=n_th_row< Nb_walls and V_walls_pos[n_th_row*(Nb_walls+1)+n_th_column+1]!=0:
                
                    wall_distance= (((sprite_pos_x-(n_th_column*(wall_length)+ wall_length))**2)
                                                  +((sprite_pos_y- first_coords_Y)**2))**(1/2)

                    n_th_column_sauvegarde = n_th_column
                    n_th_row_sauvegarde = n_th_row
                    
                    if_vertical_collision = True
                    n_th_column = -2 # pour sortir de la boucle "while"
                    
                    # correct fishbowl effect:
                    if n_th_angle < 180:

                        alpha_mur_vertical= beta_fisheye

                    else:

                        alpha_mur_vertical= -beta_fisheye

                else:

                    n_th_column-=1
                    first_coords_Y -= Y_distance_constant
        
        
        ## Détecter les murs horizontaux:
        n_th_row = int(sprite_pos_y/(wall_length))

        Xa = round(wall_length/math.tan(math.radians(360-n_th_angle)),2)
        
        # if the ray is oriented towards the top side of the map:
        if n_th_angle>180:
            
            dis_wall = sprite_pos_y%(wall_length)

            first_X_coords= -round(dis_wall/math.tan(math.radians(n_th_angle)),2) + sprite_pos_x
            # first intersection's X coords of the
            
            # Check if there is a wall on each possible intersection:
            while n_th_row>=0:
                
                n_th_column= int((first_X_coords)/(wall_length))


                if 0<=n_th_column<Nb_walls and H_walls_pos[n_th_column*(Nb_walls+1)+n_th_row]!=0:
                    
                    distance_sprite_murhorizontal= (((sprite_pos_x-first_X_coords)**2)+
                                                    ((sprite_pos_y- (n_th_row*(wall_length)))**2))**(1/2)

                    # if there is a wall:
                    if distance_sprite_murhorizontal <= wall_distance:
                        
                        if_horizontal_collision=True

                        # Correct fishbowl effect
                        if n_th_angle < 270:
                            alpha_horizontal_wall = beta_fisheye
                        
                        else:
                            alpha_horizontal_wall = -beta_fisheye
                            
                        distance_correcte= (distance_sprite_murhorizontal)*math.cos(math.radians(alpha_horizontal_wall))

                        
                        # To not have division with 0:
                        if distance_correcte==0:
                            distance_correcte=0.001
                        
                        wall_height = (wall_distance_constant/distance_correcte)

                        # trace the foc lines for the minimap
                        pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],
                                           [first_X_coords/3, (n_th_row*(wall_length))/3],3)
                        
                        wall_X_coords = first_X_coords-(n_th_column*wall_length)

                        distance_illusion_effect = (distance_correcte/120)
                        # fading distance illusion effect
                        
                        textures(wall_X_coords,H_walls_pos,n_th_column,n_th_row,n_th_angle_degree,wall_height,
                                 wall_length,Nb_walls,distance_illusion_effect,screen)
                        
                    n_th_row=-1

                n_th_row-=1
                first_X_coords+= Xa

        # if the ray is oriented towards the bottom side of the map:
        elif n_th_angle!=0:
            dis_wall= (wall_length)-sprite_pos_y%(wall_length)

            first_X_coords= round(dis_wall/math.tan(math.radians(n_th_angle)),2) + sprite_pos_x
            
            # Check if there is a wall on each possible intersection:
            while n_th_row<= (Nb_walls-1):
                
                n_th_column= int((first_X_coords)/(wall_length))

                # verifie if the wll is activated
                if 0<=n_th_column<Nb_walls and H_walls_pos[n_th_column*(Nb_walls+1)+n_th_row+1]!=0:
                    
                    distance_sprite_murhorizontal= (((sprite_pos_x-first_X_coords)**2)+
                                                    ((sprite_pos_y- (n_th_row*(wall_length)+wall_length))**2))**(1/2)
                    if distance_sprite_murhorizontal <= wall_distance:
                        
                        if_horizontal_collision = True

                        # Correct fishbowl effect
                        if n_th_angle < 90:
                            alpha_horizontal_wall= beta_fisheye
                        else:
                            alpha_horizontal_wall= -beta_fisheye
                            
                        distance_correcte= (distance_sprite_murhorizontal)*math.cos(math.radians(alpha_horizontal_wall))

                        # To not do a division by 0
                        if distance_correcte==0:
                            distance_correcte=0.001
                            
                        wall_height = (wall_distance_constant/distance_correcte)
                        
                        pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],
                                           [first_X_coords/3, (n_th_row*(wall_length)+wall_length)/3],3)
                        # trace lines on mini-map
                        
                        wall_X_coords = first_X_coords-(n_th_column*wall_length)

                        distance_illusion_effect = (distance_correcte/120)

                        textures(wall_X_coords,H_walls_pos,n_th_column,n_th_row+1,n_th_angle_degree,wall_height,
                                 wall_length,Nb_walls,distance_illusion_effect,screen)

                    n_th_row=Nb_walls+ 1

                n_th_row+=1
                first_X_coords-= Xa
        
        ## if there was no collision for horizontal walls, display the results of the vertical wall
        if if_vertical_collision == True and if_horizontal_collision==False:
                        
            distance_correcte= (wall_distance)*math.cos(math.radians(alpha_mur_vertical))
            # correct fishbowl effect

            # To not divide by 0
            if distance_correcte==0:
                distance_correcte=0.001
                
            wall_height = (wall_distance_constant/distance_correcte)
            
            pygame.draw.aaline(screen,"red",[sprite_pos_x/3, sprite_pos_y/3],
                               [(n_th_column_sauvegarde*(wall_length)+ wall_length)/3,first_coords_Y/3],3)
            # trace FOV lines on the mini-map
            
            wall_X_coords= first_coords_Y-(n_th_row_sauvegarde*wall_length)

            distance_illusion_effect = (distance_correcte/120)

            textures(wall_X_coords,V_walls_pos,n_th_row_sauvegarde,n_th_column_sauvegarde+1,n_th_angle_degree,wall_height,
                     wall_length,Nb_walls,distance_illusion_effect,screen)

        
def textures(wall_X_coords,liste_VH,n_ième_1,n_ième_2,n_th_angle_degree,wall_height,wall_length,Nb_walls,distance_illusion_effect,screen):

    # texture number 1 (normal uni-color texture):
    if liste_VH[n_ième_1*(Nb_walls+1)+n_ième_2]==1:
          
        pygame.draw.aaline(screen,(90 * distance_illusion_effect+ 165, 213 * distance_illusion_effect+42, 213 * distance_illusion_effect+42),[n_th_angle_degree,300+wall_height],
                               [n_th_angle_degree,300-wall_height],1)

    # texture number 2 (the wall with a window):
    elif liste_VH[n_ième_1*(Nb_walls+1)+n_ième_2]==2:
        
        pygame.draw.aaline(screen,(255,26 * distance_illusion_effect+ 229, 51 * distance_illusion_effect + 204),[n_th_angle_degree,300+wall_height],
                           [n_th_angle_degree,300-wall_height],1)
        # draw background
        
        # draw the horizontal lines that are on the top and bottom of the wall:
        pygame.draw.aaline(screen,(255,55 * distance_illusion_effect+ 200, 105 * distance_illusion_effect + 150),[n_th_angle_degree,300+wall_height],
                           [n_th_angle_degree,(300+wall_height)-(wall_height/15)],1)
        pygame.draw.aaline(screen,(255,55 * distance_illusion_effect+ 200,105 * distance_illusion_effect+ 150),[n_th_angle_degree,300-wall_height],
                           [n_th_angle_degree,(300-wall_height)+(wall_height/15)],1)
        pygame.draw.aaline(screen,(255,77 * distance_illusion_effect+ 178,153 * distance_illusion_effect+ 102),[n_th_angle_degree,300+wall_height],
                           [n_th_angle_degree,(300+wall_height)-(wall_height/25)],1)
        
        # draw the windows
        if (wall_length/4)<wall_X_coords< (wall_length/2.3) or (wall_length-(wall_length/2.3))<wall_X_coords<(wall_length-(wall_length/4)):
            pygame.draw.aaline(screen,(102 * distance_illusion_effect+ 153,255,255),
                               [n_th_angle_degree,300+(wall_height/2)],[n_th_angle_degree,300-(wall_height/2)],1)
            # draw the sky that is outside the window
            
            # centre_window_1 --> left window
            # centre_window_2 --> right window
            centre_window_1= ((wall_length/4)+(wall_length/2.3))/2
            centre_window_2= ((wall_length-(wall_length/2.3))+(wall_length-(wall_length/4)))/2
            
            # thickness of the sides of the windows
            epaisseur_cadre_vertical = (wall_length/3.93)-(wall_length/4)
            epaisseur_cadre_horizontal=(wall_height/2)-(wall_height/2.1)
            
            # race the vertical outline of windows
            if wall_X_coords< (wall_length/3.93) or (wall_length/2.3)-epaisseur_cadre_vertical<wall_X_coords<(wall_length/2.3) or (wall_length-(wall_length/2.3))<wall_X_coords<(wall_length-(wall_length/2.3))+epaisseur_cadre_vertical or wall_length-(wall_length/3.93)<wall_X_coords or centre_window_1 - (epaisseur_cadre_vertical/2) <wall_X_coords< centre_window_1 + (epaisseur_cadre_vertical/2) or centre_window_2 - (epaisseur_cadre_vertical/2) <wall_X_coords< centre_window_2 + (epaisseur_cadre_vertical/2):
                pygame.draw.aaline(screen,(244 + distance_illusion_effect, 224 + distance_illusion_effect, 224 + distance_illusion_effect),
                                   [n_th_angle_degree,300+(wall_height/2)],[n_th_angle_degree,300-(wall_height/2)],1)
            
            # draw the horizontal outline of windows
            else:
                pygame.draw.aaline(screen,(224 + distance_illusion_effect, 224 + distance_illusion_effect,224 + distance_illusion_effect),
                                   [n_th_angle_degree,300+(wall_height/2)],[n_th_angle_degree,300+(wall_height/2.4)],1)
                pygame.draw.aaline(screen,(224 + distance_illusion_effect, 224 + distance_illusion_effect,224 + distance_illusion_effect),
                                   [n_th_angle_degree,300-(wall_height/2)],[n_th_angle_degree,300-(wall_height/2.1)],1)
                pygame.draw.aaline(screen,(224 + distance_illusion_effect, 224 + distance_illusion_effect,224 + distance_illusion_effect),
                                   [n_th_angle_degree,300-(epaisseur_cadre_horizontal/2)],[n_th_angle_degree,300+(epaisseur_cadre_horizontal/2)],1)
            
            # black bordure at the bottom of the windows
            pygame.draw.aaline(screen,(40 * distance_illusion_effect+ 215,40 * distance_illusion_effect+ 215,40 * distance_illusion_effect+ 215),
                               [n_th_angle_degree,300+(wall_height/2)],[n_th_angle_degree,300+(wall_height/2.1)],1)


    # texture number 2 (the wall with a cobblestone, like in a cave):
    else:
        
        pygame.draw.aaline(screen,(170 * distance_illusion_effect + 85,179 * distance_illusion_effect + 76,179 * distance_illusion_effect + 76),
                           [n_th_angle_degree,300+wall_height],[n_th_angle_degree,300-wall_height],1)
        # draw background
        
        # draw horizontal lines that are at the bottom
        pygame.draw.aaline(screen,(225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30),
                           [n_th_angle_degree,300+wall_height-(wall_height/18)],[n_th_angle_degree,300+wall_height-(wall_height/19)],1)
        pygame.draw.aaline(screen,(225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30),
                           [n_th_angle_degree,300+wall_height],[n_th_angle_degree,300+wall_height],1)
        
        # draw vertical lines that are at the bottom
        if round(wall_X_coords,1)%(wall_length/40)==0:
            pygame.draw.aaline(screen,(225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30),
                               [n_th_angle_degree,300+wall_height],[n_th_angle_degree,300+wall_height-(wall_height/19)],1)

        # draw vertical lines of the wall
        if round(wall_X_coords,1)%(wall_length/12)==0:
            
            position_verticale= 300+wall_height-(wall_height/19)

            while position_verticale-(2*(wall_height/19*4))>=300-wall_height:
                pygame.draw.aaline(screen,(197 * distance_illusion_effect + 58,202 * distance_illusion_effect + 53,202 * distance_illusion_effect + 53),
                                   [n_th_angle_degree,position_verticale],[n_th_angle_degree,position_verticale-(wall_height/19*4)],1)
                position_verticale-= 2*(wall_height/19*4)
        
        # same algorithm as before (draw vertical lines of the wall), but with a slight offset
        elif round(wall_X_coords-(wall_length/12/2),1)%(wall_length/12)==0:
            
            position_verticale= 300+wall_height-(wall_height/19*5)

            while position_verticale-(2*(wall_height/19*4))>=300-wall_height:
                pygame.draw.aaline(screen,(197 * distance_illusion_effect + 58,202 * distance_illusion_effect + 53,202 * distance_illusion_effect + 53),
                                   [n_th_angle_degree,position_verticale],[n_th_angle_degree,position_verticale-(wall_height/19*4)],1)
                position_verticale-= 2*(wall_height/19*4)

        position_verticale= 300+wall_height-(wall_height/19*5)

        while position_verticale-(2*(wall_height/19*2))>=300-wall_height:
            pygame.draw.aaline(screen,(197 * distance_illusion_effect + 58,202 * distance_illusion_effect + 53,202 * distance_illusion_effect + 53),
                               [n_th_angle_degree,position_verticale],[n_th_angle_degree,position_verticale],1)
            position_verticale-= 2*(wall_height/19*2)
        
        
        pygame.draw.aaline(screen,(225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30),
                           [n_th_angle_degree,position_verticale+2*(wall_height/19*2)],[n_th_angle_degree,position_verticale+2*(wall_height/19*2)],1)
        # draw horizontal lines at the top
        
        # draw vertical lines at the top
        if round(wall_X_coords,1)%(wall_length/40)==0:
            pygame.draw.aaline(screen,(225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30,225 * distance_illusion_effect + 30),
                               [n_th_angle_degree,position_verticale+2*(wall_height/19*2)],[n_th_angle_degree,300-wall_height],1)