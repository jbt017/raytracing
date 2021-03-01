# Asignment 5:  Ray Tracing
# Justin Blake Till CWID 101-66-127
# Summary: Define three spheres and checkerboard plane.  Light the objects with ray tracing implementation.
# shading.
# Date: 2/26/21

import math
import copy
from tkinter import *


# ************************************************************************************
# vector math

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

# scalar multiplication
def scalarMult(vector, scalar):
    product = []

    for i in vector:
        product.append(i * scalar)
    
    return product


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

# Constants and globals
CanvasWidth = 800
CanvasHeight = 400
d = 500
viewpoint = [0, 0, -d] # center of projection
debug = False
lightsource = [1, 1, -1]
lightsource = normalvector(lightsource)
# 45 degrees behind the viewer
# ambient light intensity
Ia = 0.3
# point light intensity
Ip = 0.7
Ipl = normalvector([150, 150, 150])
# constants of reflectivity
Kd = 0.5
Ks = 0.5
# specular index constant
specIndex = 10
blackbackground = "#000000"
skyboxcolor = "#94f3ff"
depth = 4



# ************************************************************************************
# object defitions

class sphere:
    def __init__(self, radius, center, color):
        self.radius = radius
        self.color = color
        self.center = center
        self.localweight = 20
        self.reflectweight = 80
        self.N = []

    def getcolor(self, X, Z):
        return self.color

    def getsurfNorm(self, point):
        self.N = normalvector(point)
        return self.N

spherelist = []

class checkerboard:
    def __init__(self):
        self.y = -200
        self.color = ""
        self.point = [0, -200, 0]
        self.localweight = 80
        self.reflectweight = 20
        P = vectorsub([100, -200, 100], self.point)
        Q = vectorsub([-100, -200, 100], self.point)
        self.N = normalvector(crossproduct(P,Q))

    def getcolor(self, X, Z):
        if X >= 0: 
            ColorFlag = 1
        else:
            ColorFlag = 0

        if abs(X) % 200 > 100:
            if ColorFlag == 0:
                ColorFlag = 1

        if abs(Z) % 200 > 100:
            if ColorFlag == 0:
                ColorFlag = 1

        if ColorFlag == 1:
            self.color = normalvector([255, 0, 0])
        else:
            self.color = "white"
            self.color = normalvector([255, 255, 255])

        return self.color

    def getsurfNorm(self, point):
        return self.N


    

# ************************************************************************************
# function definitions
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

# generate a 3-D reflection vector, given a surface normal, N, and lighting vector, L
def reflect(N, L):
    R = []
    N = normalvector(N)
    L = normalvector(L)

    twoCosPhi = 2 * (N[0]*L[0] + N[1]*L[1] + N[2]*L[2])

    if twoCosPhi > 0:
        for i in range(3):
            R.append( - L[i])
    else:
        for i in range(3):
            R.append( -N[i] + (L[i] / twoCosPhi))

    return normalvector(R)

# generate a color hex code string from the illumination components
def triColorHexCode(ambient, diffuse, specular, color):
    combinedColorCode = colorHexCode(ambient + diffuse + specular)
    specularColorCode = colorHexCode(specular)
    colorString = "#" + specularColorCode + combinedColorCode + specularColorCode
    return colorString

def colorHexCode(intensity):
    hexString = str(hex(round(255 * intensity)))
    if hexString[0] == "-":
        print("negative intensity error")
    else:
        # get rid of "0x" at the beginning of hex strings
        trimmedHexString = hexString[2:]
        # convert single digit hex strings to two digit hex strings
        if len(trimmedHexString) == 1: trimmedHexString = "0" + trimmedHexString
        # we will use the green color component to display our monochrome illumination results
    return trimmedHexString

# compute local color from Phong Illumination Model
def computeLocalColor(object, startPoint):

    # calculate red
    L = normalvector(vectorsub(lightsource, startPoint))
    V = normalvector([0,0,-1])
    N = object.getsurfNorm(startPoint)
    ambient = object.getcolor(startPoint[0], startPoint[2])[0] * Kd
    NdotL = dotproduct(N, L)

    if NdotL < 0:
        NdotL = 0
    diffuse = Ipl[0] * Kd * NdotL
    R = reflect(N, L) # return normal reflect vector
    RdotV = dotproduct(R, V)

    if RdotV < 0:
        RdotV = 0
    specular = Ipl[0] * Ks * RdotV**specIndex

    redcolor = triColorHexCode(ambient, diffuse, specular, object.getcolor(startPoint[0], startPoint[1]))


    # calculate green

    L = normalvector(lightsource)
    V = normalvector([0,0,-1])
    N = object.getsurfNorm(startPoint)
    ambient = object.getcolor(startPoint[0], startPoint[2])[1] * Kd
    NdotL = dotproduct(N, L)

    if NdotL < 0:
        NdotL = 0
    diffuse = Ipl[1] * Kd * NdotL
    R = reflect(N, L) # return normal reflect vector
    RdotV = dotproduct(R, V)

    if RdotV < 0:
        RdotV = 0
    specular = Ipl[1] * Ks * RdotV**specIndex

    greencolor = triColorHexCode(ambient, diffuse, specular, object.getcolor(startPoint[0], startPoint[1]))

    # calculate blue

    L = normalvector(vectorsub(lightsource, startPoint))
    V = normalvector([0,0,-1])
    N = object.getsurfNorm(startPoint)
    ambient = object.getcolor(startPoint[0], startPoint[2])[2] * Kd
    NdotL = dotproduct(N, L)

    if NdotL < 0:
        NdotL = 0
    diffuse = Ipl[2] * Kd * NdotL
    R = reflect(N, L) # return normal reflect vector
    RdotV = dotproduct(R, V)

    if RdotV < 0:
        RdotV = 0
    specular = Ipl[2] * Ks * RdotV**specIndex

    bluecolor = triColorHexCode(ambient, diffuse, specular, object.getcolor(startPoint[0], startPoint[1]))

    # print(f"bluecolor is {bluecolor}") 

    color = redcolor[0:3] + greencolor[3:5] + bluecolor[5:7]
    # print(f"combined color code is {color}")


    return color

# combine color sources to output pixel color
def combineColors(localColor, localWeight, reflectedColor, reflectedWeight):
    color = localColor
    return color


# ************************************************************************************
# drawing/implementation methods

# trace ray from pixel 
def traceray(startPoint, ray, depth):
    # return black if you reach the bottom of the recursive call
    if depth == 0:
        return blackbackground

    # interset ray with all objects and find intersection point
    # (if any) that is closest to startPoint of ray
    if depth == 4:
        ray = vectorsub(startPoint, ray)
    intersection = findClosestIntersect(startPoint, ray)

    # if no intersection return skyboxcolor

    if intersection[0] == []:
        return skyboxcolor

    # Compute local color
    localColor = computeLocalColor(intersection[1], startPoint)

    # Compute reflected direction
    N = intersection[1].getsurfNorm(startPoint)
    L = normalvector(lightsource)
    # sub T for L to account for trace vector rather than lighting vector, i.e. it moves in the opposite direction
    T = scalarMult(L, -1)
    reflectedVector = reflect(N,T)

    # Compute color of reflection
    reflectedColor = traceray(intersection[0], reflectedVector, depth-1)

    # Combine local and reflected colors
    color = combineColors(localColor, intersection[1].localweight, reflectedColor, intersection[1].reflectweight)

    return localColor


# find possible intersects (if any) and return the closest, return false if no intersect
def findClosestIntersect(startPoint, ray):
    intersect = []
    # print(f"This is the startpoint {startPoint} and this is the ray {ray}")

    # check spheres for possible intersections
    for i in spherelist:
        # calculate pieces of your quadratic
        a = ray[0]**2 + ray[1]**2 + ray[2]**2
        b = 2 * ray[0] * (startPoint[0] - i.center[0]) + 2 * ray[1] * (startPoint[1] - i.center[1]) + 2 * ray[2] * (startPoint[2] - i.center[2])
        c = i.center[0]**2 + i.center[1]**2 + i.center[2]**2 + startPoint[0] + startPoint[1] + startPoint[2] + 2 * (-i.center[0] + startPoint[0] - i.center[1] + startPoint[1] - i.center[2] + startPoint[2]) - i.radius**2

        # calculate the discriminant
        discriminant = b**2 - (4 * a * c)

        if discriminant < 0:
            pass
        elif discriminant == 0:
            t = (-b + discriminant)/(2 * a)

            intersect.append(vectoradd(startPoint, scalarMult(ray, t)))
            intersect.append(i)
            
            return intersect
        elif discriminant > 0:
            t = (-b + discriminant)/(2 * a)
            t2 = (-b - discriminant)/(2 * a)

            # verify which root gives you the closer intersect
            if t2 < t:
                t = t2

            intersect.append(vectoradd(startPoint, scalarMult(ray, t)))
            intersect.append(i)
            return intersect

    # check checker plane for possible intersections
    if intersect == []:
        # calculate pieces of t formula
        A = board.getsurfNorm(startPoint)[0]
        B = board.getsurfNorm(startPoint)[1]
        C = board.getsurfNorm(startPoint)[2]

        a = board.point[0]
        b = board.point[1]
        c = board.point[2]

        D = A * a + B * b + C * c

        denominator = A * ray[0] + B * ray[1] + C * ray[2]
        
        # check to see if intercept exists
        if denominator == 0:
            return intersect
        else:
            numerator = -((A * startPoint[0] + B * startPoint[1] + C * startPoint[2]) - D)
            t = numerator / denominator

            intersect.append(vectoradd(startPoint, scalarMult(ray, t)))
            intersect.append(board)


    return intersect



# ************************************************************************************
# GUI setup

root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
w.pack()

# ************************************************************************************
# Setup Objects

# instance green, red, and blue spheres
spherelist.append(sphere(50, [250, 200, 50], normalvector([255, 0, 0])))
spherelist.append(sphere(50, [500, 200, -50], normalvector([0, 0, 255])))
spherelist.append(sphere(50, [700, 200, -0], normalvector([0, 255, 0])))

board = checkerboard()

# start the draw
for y in range(CanvasHeight):
        for x in range(CanvasWidth):
            ijk = vectorsub([x, y, 0], viewpoint)
            color = traceray(viewpoint, ijk, depth)
            # print(f"printing color {color} at {x} and {y}")
            w.create_line(x, y, x+1, y, fill=color)


root.mainloop()