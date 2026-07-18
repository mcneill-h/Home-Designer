
# <p align="center"> 3D Ray casting Engine for Architectural Design </p>
<p align="center">
<img width="580" height="318" alt="1111" src="https://github.com/user-attachments/assets/04023e4a-19f6-4a3a-9745-105d9441e3c5" />
</p>
<p align="center">
<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">  <img src="https://img.shields.io/badge/Pygame-2.6-00AA00?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame">  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License">  <img src="https://img.shields.io/badge/Release-v2.0.0-blue?style=for-the-badge" alt="Release">  <img src="https://img.shields.io/badge/Open_Source-Yes-success?style=for-the-badge" alt="Open Source">
</p>

# What is this 3D engine?

The objective of this program is to help architects in their work by creating a tool that converts 2D architectural blueprints into a real-time 3D virtual walkthrough tool. Anyone can draw a sketch of whatever building floor they want to reproduce it virtually. Moreover, I wanted to use **ray casting**, a 3D rendering technique that was used for the first computers in the 80s, to discover how good it fares on modern computers. 

The program was to built from scratch and without the use of external code, expect for the use of a few libraries such as Pygame that generates geometric shapes.

The final program can scan both digital blueprints and hand-drawn floor plans. It is capable of rendering up to 22,000 walls simultaneously while consuming only about 12% of the CPU on a MacOs (Intel Core i5 processor). With a more powerful
processor, it can render up to a quarter of a million walls. 

Despite its effectiveness, the program has several limitations. It currently only supports single-floor buildings and places walls in a grid-based, horizontally and vertically. We can reproduce approximated diagonal or curved walls by combining multiple small segments, but this remains a workaround rather than a true solution.

# Broad Program explanation

I computed collisions by taking advantage of the geometry of the environment. By creating a grid-based representation of wall placement, I could exploit repeating patterns and trigonometry to determine the positions of possible intersections. The program then only needed to check whether a wall existed at a given intersection with the ray. The program send over 1200 rays, at an fov of 120 degrees, in order to generate the 3D walls

To store information of where the walls are placed, I used a list in which each binary value determines whether a square “block” contains a wall. “1” indicates the presence of a wall, while “0” indicates empty space. Through an algorithm this list is then divided into two: one containing information about all horizontal walls and the other about vertical walls. This transformation is necessary so that, after scanning a blueprint, the environment can be reproduced in a uniform structure.
<img width="248" height="75" alt="Screenshot 2026-07-16 at 20 40 08" src="https://github.com/user-attachments/assets/d88e1ecb-9e11-43ff-afb2-79065d458638" />


# How to use the program?

By default, the program is set to analyse and reproduce in 3D the "Image11.png" image. To change which image, go into the "Final_Simulation_3D_definition.py" code file and change the "Image11.png" path to another image of your choice. Moreover, users can choose how many walls are generated on each row and column by changing the "Nb_murs" value (It is set at 50 by default. 

Launch the "Final_Simulation_3D.py" code to start the program. An editing menu will then appear, allowing the walls to be placed, removed, or textured. Hence the user can reproduce any house's floor. <img width="90" height="89" alt="Screenshot 2026-07-16 at 20 40 18" src="https://github.com/user-attachments/assets/5122a8a8-34b9-4605-8df9-7f8382405f4c" />

Finally, press the “enter” key to get close the editing menu and launch the simulation. 

- Use WASD keys to move.
- Press O or K to change the height of the walls.
- Press P or L to change the player's moving speed


<p align="center">
<img width="264" height="100" alt="2222" src="https://github.com/user-attachments/assets/bdb049c1-0b73-4014-b28d-fa55bb6a302e" /> <img width="333" height="89" alt="3333" src="https://github.com/user-attachments/assets/af0ef5d5-6044-4ade-a352-572bb76cf505" />
</p>


# Installation

Download the "Final_simulation_3D" folder and play the "Final_simulation_3D.py" code. I personally use Thonny 4.1.7 with Python 3.10 to run the script. The following libraries are downloaded on my computer: Pygame (2.6.1), math, PIL (1.1.6) and ImageIO (2.37.0).

# License
Licensed under the MIT License - See the LICENSE document
