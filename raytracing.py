# Asignment 5:  Ray Tracing
# Justin Blake Till CWID 101-66-127
# Summary: Define three spheres and checkerboard plane.  Light the objects with ray tracing implementation.
# shading.
# Date: 2/26/21

import math
import copy
from tkinter import *


# Constants and globals
CanvasWidth = 800
CanvasHeight = 400
d = 500
viewpoint = [0, 0, -500]
filltype = 1
activeObjectIndex = 0
debug = False
lightsource = [1, 1, -1]
# 45 degrees behind the viewer
# ambient light intensity
Ia = 0.3
# point light intensity
Ip = 0.7
# constants of reflectivity
Kd = 0.5
Ks = 0.5
# specular index constant
specIndex = 1

# ************************************************************************************
# function definitions

# vector addition
def vectoradd(P, Q):
    sum = []

    for i in range(3):
        sum.append(P[i] + Q[i])
    
    return sum

# vector subtraction
def vectorsub(P, Q):
    sum = []

    for i in range(3):
        sum.append(P[i] - Q[i])
    
    return sum

# Compute cross product of 2 3D vectors
def crossproduct(vector1, vector2):
    product = []
    product.append(vector1[1]*vector2[2]-vector1[2]*vector2[1])
    product.append(vector1[2] * vector2[0] - vector1[0] * vector2[2])
    product.append(vector1[0] * vector2[1] - vector1[1] * vector2[0])
    return product

# Compute dot product of 2 3D vectors
def dotproduct(vector1, vector2):
    product = (vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2])   
    return product

# Normalize 3D vector
def normalvector(vector):
    norm = 0

    for i in vector:
        norm = norm + i**2

    norm = math.sqrt(norm)
    normalv = []

    for i in range((len(vector))):
        normalv.append(vector[i]/norm)

    return normalv

# ************************************************************************************
# project/conversion/hex  suppporting methods

# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
    ps = []

    # Projection of start points
    xpos = d * (point[0] / (d + point[2]))
    ypos = d * (point[1] / (d + point[2]))
    zpos = point[2] / (d + point[2])  # suspect we will need later

    ps.append(xpos)
    ps.append(ypos)
    ps.append(zpos)

    return ps


# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as
# they are only used in rendering.
def convertToDisplayCoordinates(point):
    displayXY = []

    # Display point conversion of starting points
    displayXY.append(CanvasWidth / 2 + point[0])
    displayXY.append(CanvasHeight / 2 - point[1])

    return displayXY



# ************************************************************************************
# GUI setup