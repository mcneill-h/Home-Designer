
# <p align="center"> 3D Ray casting Engine for Architectural Design </p>
<p align="center">
<img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">  <img src="https://img.shields.io/badge/Pygame-2.6-00AA00?style=for-the-badge&logo=pygame&logoColor=white" alt="Pygame">  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License">  <img src="https://img.shields.io/badge/Release-v2.0.0-blue?style=for-the-badge" alt="Release">  <img src="https://img.shields.io/badge/Open_Source-Yes-success?style=for-the-badge" alt="Open Source">
</p>

# What is this Sisyphus game?

The objective of this program is to help architects in their work by creating a tool that converts 2D architectural blueprints into a real-time 3D virtual walkthrough tool. Anyone can draw a sketch of whatever building floor they want to reproduce it virtually. Moreover, I wanted to use **ray casting**, a 3D rendering technique that was used for the first computers in the 80s, to discover how good it fares on modern computers. 



Built from scratch, no external code, and minimal set of libraries (ex:Pygame). 
The
objective was to build from scratch, without using external code, and relying only on
a few libraries such as Pygame to generate geometric shapes.


<p align="center">
<img width="580" height="318" alt="1111" src="https://github.com/user-attachments/assets/04023e4a-19f6-4a3a-9745-105d9441e3c5" />
</p>

# How it works?


Ray casting has an
elegant way to transpose 2D top-down environment into 3D. The picture below
shows this transformation between the dimensions, however, it is worth noting that
the 3D simulation uses 1200 different rays.

While starting to code, I realised that Pygame did not offer any tools to determine
whether two lines (a ray and a wall) intersect. To compute and determine the
closest collision, I could have for instance used brute forcing techniques to
mathematically check if there is an intersection between each ray and wall, but it
would not be optimised.

Instead, I computed collisions by taking advantage of the
geometry of the environment. By creating a grid-based
representation of wall placement, I could exploit repeating
patterns and trigonometry to determine the positions of
possible intersections. The program then only needed to
check whether a wall existed at a given intersection with
the ray.


Next, I had to find a way to store information of where the walls are placed. I used a
list in which each binary value determines whether a square “block” contains a wall.
“1” indicates the presence of a wall, while “0” indicates empty space. Through
algorithms this list is then divided into two: one
containing information about all horizontal walls
and the other about vertical walls. This
transformation is necessary so that, after
scanning a blueprint, the environment can be
reproduced in a uniform structure.

By analysing the RGB of the blueprint’s pixels, we can then digitally store the
information where the obstacles are. Below is an example of a real building
blueprint that the program has digitally reproduced.

Users may also wish to directly modify the environment within the program, so I
added an editing menu that allows walls to be placed, removed, or textured.
Texturing walls is difficult to implement directly using sprites, so I designed an
alternative approach that changes the colour of the lines composing a wall based
on their position. For instance, if the player is viewing the first quarter of a wall from
the left, yellow lines are generated to form that section.

Finally, certain numerical parameters had to be adjusted to correct for the fisheye
effect.
The final program can scan both digital blueprints and hand-drawn floor plans. It is
capable of rendering up to 22,000 walls simultaneously while consuming only about
12% of the CPU on a MacOs (Intel Core i5 processor). With a more powerful
processor, it can render up to a quarter of a million walls. This was the moment
when mathematics stopped being abstract and computer science stopped being
just code.
Despite its effectiveness, the program has several limitations. It currently only
supports single-floor buildings and places walls in a grid-based, horizontally and
vertically. We can reproduce approximated curved walls by combining multiple
small segments, but this remains a workaround rather than a true solution.

+ talk about textures?

<p align="center">
<img width="264" height="100" alt="2222" src="https://github.com/user-attachments/assets/bdb049c1-0b73-4014-b28d-fa55bb6a302e" /> <img width="333" height="89" alt="3333" src="https://github.com/user-attachments/assets/af0ef5d5-6044-4ade-a352-572bb76cf505" />
</p>


Press the “enter” key to get pass the editing menu and use WASD keys to move. Press O or K to change the size of the walls.

# Installation

Download the "Final_simulation_3D" folder and play the "Final_simulation_3D.py" code. I personally use Thonny 4.1.7 with Python 3.10 to run the script. The following libraries are downloaded on my computer: Pygame (2.6.1), math, PIL (1.1.6) and ImageIO (2.37.0).

# License
Licensed under the MIT License - See the LICENSE document
