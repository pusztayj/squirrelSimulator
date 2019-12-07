# squirrelSimulator
A game made by Justin Pusztay and Trevor Stalnaker

## Overview
In the fast paced world of Squirrel Simulator, the player guides a squirrel through a forested wood in the hopes of stashing enough nuts to survive. The player must be on guard against competitors. Will you befriend your fellow creatures to protect your hard won acorns, or will you strive to be the top of the food chain.  

### How to Play

### Prerequisites
The entire game and processing is completed on Python3. 
You can download python at the following link:
https://www.python.org/

To use this framework the following packages are needed:
```
pygame
random (Built into Python)
math (Built into Python)
```
To install these packages on Terminal for  Mac OSX/ Linux, or Command Prompt on Windows, pip must be installed on your computer (link: https://pip.pypa.io/en/stable/installing/). Once installed, copy and paste the following lines:

```
pip install pygame
```
### Installing

Git must be installed on your computer (link: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

To download the Repository, open Terminal/ Command Prompt to the desired location, and run the following line:

```
git clone https://github.com/pusztayj/squirrelSimulator.git
```
If you are having trouble navigating around Terminal, you can use the following as a resource. https://www.tbi.univie.ac.at/~ronny/Leere/270038/tutorial/node8.html

### Known Issues
Squirrel Simulator displays no issues on Windows machines but crashes randomly on UNIX machines. In our experience these crashes happen randomly but are all loading issues. It can't load the font, the images, and the sound. This is a very strange issue since it loads all these items but crashes at different points in the code. For example, it loads texts with the only font that we use- Times New Roman- but then claims that it can't be loaded. A similar issue occurs for our images. We did not fix this issue because it was discovered on December 6, 2019 around 10pm.
