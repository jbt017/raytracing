# Asignment 4:  Lighting and Shading models
# Justin Blake Till CWID 101-66-127
# Summary: Define octagonal prism object.  Implement three methods of lighting, Flat shading, Gouraud shading, and Phong
# shading.
# Date: 2/15/21

import math
import copy
from tkinter import *

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
# storage list for G shading vertex norms
vertexnorms = []


# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
apex = [0, 50, 100]
base1 = [50, -50, 50]
base2 = [50, -50, 150]
base3 = [-50, -50, 150]
base4 = [-50, -50, 50]

# Definition of the five Pyramid polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
frontpoly = [apex, base1, base4]
rightpoly = [apex, base2, base1]
backpoly = [apex, base3, base2]
leftpoly = [apex, base4, base3]
bottompoly = [base1, base2, base3, base4]

# Definition of the object
Pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
PyramidPointCloud = [apex, base1, base2, base3, base4]
PyramidReset = copy.deepcopy(PyramidPointCloud)

#Poly Colors
PyramidColor = ["black", "red", "green", "blue", "yellow"]

# ***************************** Initialize Cube Object ***************************
# Definition  of the five underlying points
ctcorner1 = [-150, 50, 50]
ctcorner2 = [-250, 50, 50]
cbcorner1 = [-150, -50, 50]
cbcorner2 = [-250, -50, 50]
ctcorner3 = [-150, 50, 150]
ctcorner4 = [-250, 50, 150]
cbcorner3 = [-150, -50, 150]
cbcorner4 = [-250, -50, 150]

# Definition of the six Cube polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
cfrontpoly = [ctcorner1, cbcorner1, cbcorner2, ctcorner2]
crightpoly = [ctcorner3, cbcorner3, cbcorner1, ctcorner1]
cbackpoly = [ctcorner4, cbcorner4, cbcorner3, ctcorner3]
cleftpoly = [ctcorner2, cbcorner2, cbcorner4, ctcorner4]
cbottompoly = [cbcorner1, cbcorner3, cbcorner4, cbcorner2]
ctoppoly = [ctcorner2, ctcorner4, ctcorner3, ctcorner1]

# Definition of the object
Cube = [ctoppoly, cbottompoly, cfrontpoly, crightpoly, cbackpoly, cleftpoly]

# Definition of the Cubes's underlying point cloud.  No structure, just the points.
CubePointCloud = [ctcorner1, ctcorner2, cbcorner1, cbcorner2, ctcorner3, ctcorner4, cbcorner3, cbcorner4]
CubeReset = copy.deepcopy(CubePointCloud)

# Poly Color
CubeColor = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]

# ***************************** Initialize Rectangular Pism Object ***************************
# Definition  of the five underlying points
rptcorner1 = [250, 100, 50]
rptcorner2 = [150, 100, 50]
rpbcorner1 = [250, -50, 50]
rpbcorner2 = [150, -50, 50]
rptcorner3 = [250, 100, 150]
rptcorner4 = [150, 100, 150]
rpbcorner3 = [250, -50, 150]
rpbcorner4 = [150, -50, 150]

# Definition of the six Cube polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
rpfrontpoly = [rptcorner1, rpbcorner1, rpbcorner2, rptcorner2]
rprightpoly = [rptcorner3, rpbcorner3, rpbcorner1, rptcorner1]
rpbackpoly = [rptcorner4, rpbcorner4, rpbcorner3, rptcorner3]
rpleftpoly = [rptcorner2, rpbcorner2, rpbcorner4, rptcorner4]
rpbottompoly = [rpbcorner1, rpbcorner3, rpbcorner4, rpbcorner2]
rptoppoly = [rptcorner2, rptcorner4, rptcorner3, rptcorner1]

# Definition of the object
RectPrism = [rptoppoly, rpbottompoly, rpfrontpoly, rprightpoly, rpbackpoly, rpleftpoly]

# Definition of the Rect Prism's underlying point cloud.  No structure, just the points.
RectPrismPointCloud = [rptcorner1, rptcorner2, rpbcorner1, rpbcorner2, rptcorner3, rptcorner4, rpbcorner3, rpbcorner4]
RectReset = copy.deepcopy(RectPrismPointCloud)

# Poly Colors
RectColor = ["white", "#cccccc", "#999999", "#666666","#333333", "black"]

# ***************************** Initialize Cylinder Object ***************************
# Definition of the 16 underlying points
front1 = [-50,120.7107,50]
front2 = [50,120.7107,50]
front3 = [120.7107,50,50]
front4 = [120.7107,-50,50]
front5 = [50,-120.7107,50]
front6 = [-50,-120.7107,50]
front7 = [-120.7107,-50,50]
front8 = [-120.7107,50,50]
back1 = [-50,120.7107,450]
back2 = [50,120.7107,450]
back3 = [120.7107,50,450]
back4 = [120.7107,-50,450]
back5 = [50,-120.7107,450]
back6 = [-50,-120.7107,450]
back7 = [-120.7107,-50,450]
back8 = [-120.7107,50,450]

# Definition of the ten polygon faces using the meaningful point names
# Polys are defined in clockwise order when viewed from the outside
northPoly = [front1, back1, back2, front2]
northEastPoly = [front2, back2, back3, front3]
eastPoly = [front3, back3, back4, front4]
southEastPoly = [front4, back4, back5, front5]
southPoly = [front5, back5, back6, front6]
southWestPoly = [front6, back6, back7, front7]
westPoly = [front7, back7, back8, front8]
northWestPoly = [front8, back8, back1, front1]
frontPoly = [front1, front2, front3, front4, front5, front6, front7, front8]
backPoly = [back1, back8, back7, back6, back5, back4, back3, back2]

# Definition of the cylinder object
cylinder = [northPoly, northEastPoly, eastPoly, southEastPoly, southPoly, southWestPoly, westPoly, northWestPoly, frontPoly, backPoly]

# Definition of the Rect Prism's underlying point cloud.  No structure, just the points.
CylinderPointCloud = [front1, front2, front3, front4, front5, front6, front7, front8, back1, back2, back3, back4, back5, back6, back7, back8]
CylinderReset = copy.deepcopy(CylinderPointCloud)

# Poly Colors
CylinderColor = ["white", "#cccccc", "#999999", "#666666", "#333333", "white", "#888888", "#777777", "#555555", "black"]

# ***************************** Clouds and Lists ***************************

# Define list of polys
Polylist = [cylinder]
PointCloudList = [CylinderPointCloud]
ResetCloudList = [CylinderReset]

# Color cloud
ColorList = [CylinderColor]


# ************************************************************************************

# This function resets the pyramid to its original size and location in 3D space
# Note that shortcuts like "apex = [0,50,100]" will not work as they build new
# structures rather than modifying the existing Pyramid / PyramidPointCloud
def resetPoly(cloud, default):
    for i in range(len(cloud)):
        for j in range(3):
            cloud[i][j] = default[i][j]



# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
    i = 0
    while i < len(object):
        j = 0
        while j < len(object[i]):
            object[i][j] = object[i][j] + displacement[j]
            j += 1
        i += 1


# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object, scalefactor):
    i = 0
    referencept = genreferencepoint(object)
    transreference = gentransvector(referencept)

    translate(object, transreference)
    while i < len(object):
        j = 0
        while j < len(object[i]):
            object[i][j] = object[i][j] * scalefactor
            j += 1
        i += 1

    translate(object, referencept)


# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotateZ(object, degrees):
    # convert degrees to radians for math function
    radianval = math.radians(degrees)
    referencept = genreferencepoint(object)

    i = 0
    while i < len(object):
        j = 0
        while j < len(object[i]):
            if j == 0:
                xpos = object[i][0] * math.cos(radianval) - object[i][1] * math.sin(radianval)
                # rotate X
            elif j == 1:
                ypos = object[i][0] * math.sin(radianval) + object[i][1] * math.cos(radianval)
                # rotate y
            elif j == 2:
                zpos = object[i][j]
                # rotate z
            j += 1
        object[i][0] = xpos
        object[i][1] = ypos
        object[i][2] = zpos
        i += 1



# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotateY(object, degrees):
    # convert degrees to radians for math function
    radianval = math.radians(degrees)

    i = 0
    while i < len(object):
        j = 0
        while j < len(object[i]):
            if j == 0:
                xpos = object[i][0] * math.cos(radianval) + object[i][2] * math.sin(radianval)
                # rotate X
            elif j == 2:
                zpos = -object[i][0] * math.sin(radianval) + object[i][2] * math.cos(radianval)
                # rotate y
            elif j == 1:
                ypos = object[i][j]
                # rotate z
            j += 1
        object[i][0] = xpos
        object[i][1] = ypos
        object[i][2] = zpos
        i += 1



# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotateX(object, degrees):
    # convert degrees to radians for math function
    radianval = math.radians(degrees)

    i = 0
    while i < len(object):
        j = 0
        while j < len(object[i]):
            if j == 1:
                ypos = object[i][1] * math.cos(radianval) - object[i][2] * math.sin(radianval)
                # rotate X
            elif j == 2:
                zpos = object[i][1] * math.sin(radianval) + object[i][2] * math.cos(radianval)
                # rotate y
            elif j == 0:
                xpos = object[i][j]
                # rotate z
            j += 1
        object[i][0] = xpos
        object[i][1] = ypos
        object[i][2] = zpos
        i += 1


# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def drawObject(object, color):
    global vertexnorms
    for i in range(0, len(object)):
        if filltype > 4:
            vertexnorms = []
            # calculate vertex normal for the foly
            if i > 7:
                for j in range(4):
                    currpoly = object[i]
                    currpolynv = normalvector(crossproduct(vectorsub(currpoly[0], nextpoly[1]), vectorsub(currpoly[0], currpoly[3])))
                    vertexnorms.append(currpolynv)
            elif i == 0:
                prevpoly = object[len(object)-3]
                nextpoly = object[i+1]
                currpoly = object[i]

                # print(f"@prevpoly {prevpoly}, @nextpoly {nextpoly}, @currpoly {currpoly}")
                prevpolynv = normalvector(crossproduct(vectorsub(prevpoly[0], prevpoly[1]), vectorsub(prevpoly[0], prevpoly[3])))
                nextpolynv = normalvector(crossproduct(vectorsub(nextpoly[0], nextpoly[1]), vectorsub(nextpoly[0], nextpoly[3])))
                currpolynv = normalvector(crossproduct(vectorsub(currpoly[0], nextpoly[1]), vectorsub(currpoly[0], currpoly[3])))
                
                vertexnorms.append(normalvector(vectoradd(currpolynv, prevpolynv)))
                vertexnorms.append(normalvector(vectoradd(currpolynv, prevpolynv)))
                vertexnorms.append(normalvector(vectoradd(currpolynv, nextpolynv)))
                vertexnorms.append(normalvector(vectoradd(currpolynv, nextpolynv)))
            else:
                prevpoly = object[i-1]
                nextpoly = object[i+1]
                currpoly = object[i]
                prevpolynv = normalvector(crossproduct(vectorsub(prevpoly[0], prevpoly[1]), vectorsub(prevpoly[0], prevpoly[3])))
                nextpolynv = normalvector(crossproduct(vectorsub(nextpoly[0], nextpoly[1]), vectorsub(nextpoly[0], nextpoly[3])))
                currpolynv = normalvector(crossproduct(vectorsub(currpoly[0], nextpoly[1]), vectorsub(currpoly[0], currpoly[3])))
                
                vertexnorms.append(normalvector(vectoradd(currpolynv, prevpolynv)))
                vertexnorms.append(normalvector(vectoradd(currpolynv, prevpolynv)))
                vertexnorms.append(normalvector(vectoradd(currpolynv, nextpolynv)))
                vertexnorms.append(normalvector(vectoradd(currpolynv, nextpolynv)))

        # print("***********************************************************************************")
        # print(f"Here are all of the vertex norms for your object {vertexnorms}")
        # print("***********************************************************************************")

        drawPoly(object[i], color[i])
    # print("drawObject stub executed.")

def vectoradd(P, Q):
    sum = []

    for i in range(3):
        sum.append(P[i] + Q[i])
    
    return sum

def vectorsub(P, Q):
    sum = []

    for i in range(3):
        sum.append(P[i] - Q[i])
    
    return sum

# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def drawPoly(poly, color):
    visible = backfacecull(poly)
    i = 0
    if visible and (filltype == 1 or filltype == 3):
        while i < len(poly):
            if i == (len(poly) - 1):
                drawLine(poly[i], poly[0])
            else:
                drawLine(poly[i], poly[i + 1])

            i += 1
    if visible and filltype !=1:
        polyfill(poly, color)
        

    # print("drawPoly stub executed.")


# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def drawLine(start, end):
    startdisplay = (convertToDisplayCoordinates(project(start)))
    enddisplay = (convertToDisplayCoordinates(project(end)))

    w.create_line(startdisplay[0], startdisplay[1], enddisplay[0], enddisplay[1])
    # print("drawLine stub executed.")


# draws with heavier line
def drawObjecthighlight(object, color):
    for i in range(0, len(object)):
        drawPolyhighlight(object[i], color[i])
    # print("drawObject stub executed.")


# draws with thicker line
def drawPolyhighlight(poly, color):
    visible = backfacecull(poly)
    if visible and filltype != 2:
        i = 0
        while i < len(poly):
            if i == (len(poly) - 1):
                drawLinehighlight(poly[i], poly[0])
            else:
                drawLinehighlight(poly[i], poly[i + 1])

            i += 1
    if visible and filltype !=1:
        polyfill(poly, color)

    # print("drawPoly stub executed.")


# draws with heavier line
def drawLinehighlight(start, end):
    startdisplay = (convertToDisplayCoordinates(project(start)))
    if debug:
        print(f"Line draw point {startdisplay}")
    enddisplay = (convertToDisplayCoordinates(project(end)))
    if debug:
        print(f"Line draw point {enddisplay}")

    w.create_line(startdisplay[0], startdisplay[1], enddisplay[0], enddisplay[1], width = 4)
    # print("drawLine stub executed.")

# This function determines the surface norm of a polygon and uses it to determine it's position relative to the viewpoint
# if a polygon is determined not visible, return False.
def backfacecull(poly):
    visible = False

    P = []
    Q = []
    for i in range(len(poly[0])):
        P.append(poly[1][i]-poly[0][i])
        Q.append(poly[2][i]-poly[0][i])

    N = crossproduct(P, Q)
    normN = normalvector(N)

    D = 0
    for i in range(len(poly[0])):
        D = D + (normN[i]*poly[0][i])

    vissum = 0
    for i in range(len(viewpoint)):
        vissum = vissum + (normN[i]*viewpoint[i])

    if vissum - D > 0:
        visible = True

    return visible

# Computer cross product of 2 3D vectors
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

# Color polygons
def polyfill(poly, color):
    displaypoly = []
    if debug:
        print(f"This is the initial array {poly}")

    # convert poly to display coordinates
    for i in range(len(poly)):
        tempproj = project(poly[i])
        if debug:
            print(f"This is the display projection {tempproj}")
        displaypoly.append(convertToDisplayCoordinates(tempproj))
        if debug:
            print(f"This is the display coordinate conversion {displaypoly}")

    for i in range(0,len(displaypoly)):
        for j in range(2):
            displaypoly[i][j] = round(displaypoly[i][j], 0)

    if debug:
        print(f"Rounded down {displaypoly}.")

    # generate edge table
    edgetable = []

    # fill list with all possible edge point sets
    edgelist = []
    # fill list with matching edge vertex pairs
    if filltype > 4:
        vertexnormslist = []

    for i in range(0,len(displaypoly)-1):
        edge = []
        if filltype > 4:
            vertnorm = []
        edge.append(displaypoly[i])
        edge.append(displaypoly[i+1])
        if filltype > 4 and i == 0:
            vertnorm.append(vertexnorms[0])
            vertnorm.append(vertexnorms[1])
        if filltype > 4 and i == 1:
            vertnorm.append(vertexnorms[1])
            vertnorm.append(vertexnorms[2])
        if filltype > 4 and i == 2:
            vertnorm.append(vertexnorms[2])
            vertnorm.append(vertexnorms[3])
        if filltype > 4 and i > 2:
            vertnorm.append(vertexnorms[3])
            vertnorm.append(vertexnorms[1])
        if debug:
            print(f"Edge candidate {edge}")
        edgelist.append(edge)
        if filltype > 4:
            vertexnormslist.append(vertnorm)

    edge = []
    if filltype > 4:
        vertnorm = []
    edge.append(displaypoly[len(displaypoly)-1])
    edge.append(displaypoly[0])
    if filltype > 4:
            vertnorm.append(vertexnorms[3])
            vertnorm.append(vertexnorms[1])
    if debug:
        print(f"Edge candidate {edge}")
    edgelist.append(edge)
    if filltype > 4:
        vertexnormslist.append(vertnorm) 
        # print(f"Here are the vertexnorms for a list of edges {vertexnormslist}")
    if debug:
        print(f"Fresh list of edges {edgelist}")

    # append edge table rows if available
    iterateedgelist = 0
    for i in edgelist:
        templist = []
        # check for error case of 0 height object
        if i[0][1] != i[1][1]:
            if i[0][1] <= i[1][1]:
                templist.append(i[0][0])
                if debug:
                    print(f"X val added to temp row {templist}")
                templist.append(i[0][1])
                templist.append(i[1][1])
                if debug:
                    print(f"Y vals added to temp row {templist}")
                # XEnd - XStart / YEnd - YStart = Delta X
                templist.append((i[1][0] - i[0][0]) / (i[1][1] - i[0][1]))
                if debug:
                    print(f"Delta X added to temp row {templist}")
                if filltype == 5: # G shading
                    startnorm = vertexnormslist[iterateedgelist][0]
                    endnorm = vertexnormslist[iterateedgelist][1]
                    # print("***********************************************************************************")
                    # print(f"here is the endnorm {endnorm}")
                    # print(f"here is the startnorm {startnorm}")
                    # print("***********************************************************************************")

                    # generate intensity and delta intensity for starting edge
                    L = normalvector(lightsource)
                    V = normalvector([0,0,-1])
                    ambient = Ia * Kd
                    N = startnorm
                    NdotL = dotproduct(N, L)
                    if NdotL < 0:
                        NdotL = 0
                    diffuse = Ip * Kd * NdotL
                    R = reflect(N, L) # return normal reflect vector
                    RdotV = dotproduct(R, V)
                    if RdotV < 0:
                        RdotV = 0
                    specular = Ip * Ks * RdotV**specIndex
                    startintensity = [ambient, diffuse, specular]

                    # generate intensity and delta intensity for ending edge
                    N = endnorm
                    NdotL = dotproduct(N, L)
                    if NdotL < 0:
                        NdotL = 0
                    diffuse = Ip * Kd * NdotL
                    R = reflect(N, L) # return normal reflect vector
                    RdotV = dotproduct(R, V)
                    if RdotV < 0:
                        RdotV = 0
                    specular = Ip * Ks * RdotV**specIndex
                    endintensity = [ambient, diffuse, specular]
                    # print("***********************************************************************************")
                    # print(f"here is the start intensity {startintensity}")
                    # print(f"here is the end intensity {endintensity}")
                    # print("***********************************************************************************")

                    # add to templist
                    templist.append(startintensity)
                    templist.append(endintensity)

                    # generate delta intensity
                    deltaintensity = []

                    for i in range(len(startintensity)):
                        change = (endintensity[i]-startintensity[i])/(templist[2]-templist[1])
                        # print(f"Here is the change delta for the edge {change}")
                        deltaintensity.append(change)

                    templist.append(deltaintensity)

                if filltype == 6: # Phong Shading
                    startnorm = vertexnormslist[iterateedgelist][0]
                    endnorm = vertexnormslist[iterateedgelist][1]

                    # add to templist
                    templist.append(startnorm)
                    templist.append(endnorm)

                    deltanorm = []
                    
                    for i in range(len(startnorm)):
                        change = (endnorm[i]-startnorm[i])/(templist[2]-templist[1])
                        deltanorm.append(change)

                    # print(f"This is delta norm {deltanorm}")

                    # add delta to templist
                    templist.append(deltanorm)

            else:
                templist.append(i[1][0])
                if debug:
                    print(f"X val added to temp row {templist}")
                templist.append(i[1][1])
                templist.append(i[0][1])
                if debug:
                    print(f"Y vals added to temp row {templist}")
                # XEnd - XStart / YEnd - YStart = Delta X
                templist.append((i[0][0] - i[1][0]) / (i[0][1] - i[1][1]))
                if debug:
                    print(f"Delta X added to temp row {templist}")
                if filltype == 5: # G Shading
                    # add intensity and delta intensity to temp edge table
                    endnorm = vertexnormslist[iterateedgelist][0]
                    startnorm = vertexnormslist[iterateedgelist][1]
                    # print("***********************************************************************************")
                    # print(f"here is the endnorm {endnorm}")
                    # print(f"here is the startnorm {startnorm}")
                    # print("***********************************************************************************")

                    # generate intensity and delta intensity for starting edge
                    L = normalvector(lightsource)
                    V = normalvector([0,0,-1])
                    ambient = Ia * Kd
                    N = startnorm
                    NdotL = dotproduct(N, L)
                    if NdotL < 0:
                        NdotL = 0
                    diffuse = Ip * Kd * NdotL
                    R = reflect(N, L) # return normal reflect vector
                    RdotV = dotproduct(R, V)
                    if RdotV < 0:
                        RdotV = 0
                    specular = Ip * Ks * RdotV**specIndex
                    startintensity = [ambient, diffuse, specular]
                    # print(f"This is calculated start intensity {startintensity}")

                    # generate intensity and delta intensity for ending edge
                    N = endnorm
                    NdotL = dotproduct(N, L)
                    if NdotL < 0:
                        NdotL = 0
                    diffuse = Ip * Kd * NdotL
                    R = reflect(N, L) # return normal reflect vector
                    RdotV = dotproduct(R, V)
                    if RdotV < 0:
                        RdotV = 0
                    specular = Ip * Ks * RdotV**specIndex
                    endintensity = [ambient, diffuse, specular]
                    # print(f"This is calculated end intensity {endintensity}")
                    # print("***********************************************************************************")
                    # print(f"here is the start intensity {startintensity}")
                    # print(f"here is the end intensity {endintensity}")
                    # print("***********************************************************************************")

                    # add to templist
                    templist.append(startintensity)
                    templist.append(endintensity)

                    # generate delta intensity
                    deltaintensity = []

                    for i in range(len(startintensity)):
                        change = (endintensity[i]-startintensity[i])/(templist[2]-templist[1])
                        # print(f"Here is the change delta for the edge {change}")
                        deltaintensity.append(change)

                    templist.append(deltaintensity)

                if filltype == 6: # Phong Shading
                    startnorm = vertexnormslist[iterateedgelist][0]
                    endnorm = vertexnormslist[iterateedgelist][1]

                    # add to templist
                    templist.append(startnorm)
                    templist.append(endnorm)

                    deltanorm = []
                    
                    for i in range(len(startnorm)):
                        change = (endnorm[i]-startnorm[i])/(templist[2]-templist[1])
                        deltanorm.append(change)

                    # print(f"This is delta norm {deltanorm}")


                    # add delta to templist
                    templist.append(deltanorm)

        # if edge was valid, add it's table data to the table list
        if templist:
            edgetable.append(templist)
            if debug:
                print(f"Added temp row to edge table {edgetable}")
        iterateedgelist += 1

    if not edgetable:
        return
    if debug:
        print(f"Printing your table {edgetable}")

    edgetable.sort(key=lambda x: x[1])
    if debug:
        print(f"print sorted table {edgetable}")
    # print("***********************************************************************************")
    # print(f"\nprint sorted table {edgetable}\n")
    # print("***********************************************************************************")


    # Assign Fill lines
    FirstFillLine = edgetable[0][1]
    LastFillLine = edgetable[len(edgetable)-1][2]
    if debug:
        print(f"First Y limit {FirstFillLine} Lower Y limit {LastFillLine}")

    # Indices for first (I), second (J) and next (next)
    I = 0
    J = 1
    next = 2

    #first two edges
    EdgeIX = edgetable[I][0]
    EdgeJX = edgetable[J][0]
    # print("***********************************************************************************")
    # print(f"\nFirst two edges \n {edgetable[I]}\n {edgetable[I]}\n")
    # print("***********************************************************************************")

    if debug:
        print(f"Initial edge values I {EdgeIX}  J {EdgeJX}")

    # if using Flat Shading mode, go ahead and calculate the poly color
    if filltype == 4:
        print("rendering poly color with Flat Shading method")
        L = normalvector(lightsource)
        V = normalvector([0,0,-1])
        N = normalvector(crossproduct(poly[0], poly[1]))
        ambient = Ia * Kd
        NdotL = dotproduct(N, L)
        if NdotL < 0:
            NdotL = 0
        diffuse = Ip * Kd * NdotL
        R = reflect(N, L) # return normal reflect vector
        RdotV = dotproduct(R, V)
        if RdotV < 0:
            RdotV = 0
        specular = Ip * Ks * RdotV**specIndex
        print(f"Here is the ambient {ambient} diffuse {diffuse} and specular {specular} for your Flat shaded poly.")
        color = triColorHexCode(ambient, diffuse, specular)

    for y in range(int(FirstFillLine), int(LastFillLine+1)):

        # determine line direction left to right
        if EdgeIX < EdgeJX:
            LeftX = EdgeIX
            RightX = EdgeJX
            LeftEdge = edgetable[I]
            RightEdge = edgetable[j]
        else:
            LeftX = EdgeJX
            RightX = EdgeIX
            LeftEdge = edgetable[J]
            RightEdge = edgetable[I]
            # print("\nLeft Edge")
            # print(LeftEdge)
            # print("Right Edge")
            # print(RightEdge)

        # determine delta intensity across the line
        if filltype == 5:
            deltalineintensity = []
            for i in range(len(LeftEdge[4])):
                if RightX - LeftX == 0:
                    deltaval = 0
                    deltalineintensity.append(deltaval)
                else:
                    deltaval = ((RightEdge[4][i] - LeftEdge[4][i])/(RightX - LeftX))
                    deltalineintensity.append(deltaval)

            # print(f"DeltaLineIntensity{deltalineintensity}")

        # determine delta norm across the line
        if filltype == 6:
            deltalineintensity = []
            if RightX - LeftX == 0:
                    deltaval = [0,0,0]
                    deltalineintensity = deltaval
            else:
                for i in range(len(LeftEdge[4])):
                    deltaval = ((RightEdge[4][i] - LeftEdge[4][i])/(RightX - LeftX))
                    deltalineintensity.append(deltaval)

        # paint across a fill line
        for x in range(int(LeftX), int(RightX)):
            # if using Gauroud calculate color intensity shifts
            if filltype == 5 and x == int(LeftX):
                intensity = LeftEdge[4]
                color = triColorHexCode(intensity[0], intensity[1], intensity[2])
                # print(f"here is the color code {color}")
                for i in range(len(intensity)):
                    intensity[i] = intensity[i] + deltalineintensity[i]
            elif filltype == 5:
                color = triColorHexCode(intensity[0], intensity[1], intensity[2])
                # print(f"here is the color code {color}")
                for i in range(len(intensity)):
                    intensity[i] = intensity[i] + deltalineintensity[i]
            
            # Phong shading methods
            if filltype == 6 and x == int(LeftX):
                intensity = LeftEdge[4]
                L = normalvector(lightsource)
                V = normalvector([0,0,-1])
                N = intensity
                ambient = Ia * Kd
                NdotL = dotproduct(N, L)
                if NdotL < 0:
                    NdotL = 0
                diffuse = Ip * Kd * NdotL
                R = reflect(N, L) # return normal reflect vector
                RdotV = dotproduct(R, V)
                if RdotV < 0:
                    RdotV = 0
                specular = Ip * Ks * RdotV**specIndex
                color = triColorHexCode(ambient, diffuse, specular)
                # print(f"here is the color code {color}")
                intensity = vectoradd(intensity, deltalineintensity)
            elif filltype == 6:
                intensity = LeftEdge[4]
                L = normalvector(lightsource)
                V = normalvector([0,0,-1])
                N = intensity
                ambient = Ia * Kd
                NdotL = dotproduct(N, L)
                if NdotL < 0:
                    NdotL = 0
                diffuse = Ip * Kd * NdotL
                R = reflect(N, L) # return normal reflect vector
                RdotV = dotproduct(R, V)
                if RdotV < 0:
                    RdotV = 0
                specular = Ip * Ks * RdotV**specIndex
                color = triColorHexCode(ambient, diffuse, specular)
                # print(f"here is the color code {color}")
                for i in range(len(intensity)):
                    intensity[i] = intensity[i] + deltalineintensity[i]
            
            # print(f"Here is the intensity {intensity}")
            # print(f"Here is the delta line intesnity {deltalineintensity}")

            w.create_line(x, y, x+1, y, fill=color)
            if debug:
                print(f"Printing pixel at X {x} and Y {y}")

        # update X values
        EdgeIX = EdgeIX + edgetable[I][3]
        EdgeJX = EdgeJX + edgetable[J][3]

        # update intensity valause
        if filltype == 5:
            # print("Before updates.")
            # print(edgetable[J][4])
            # print(edgetable[I][4])
            # print("Update vectors.")
            # print(edgetable[J][5])
            # print(edgetable[I][5])
            edgetable[J][4] = vectoradd(edgetable[J][6] , edgetable[J][4])
            edgetable[I][4] = vectoradd(edgetable[I][6] , edgetable[I][4])
            # print("After updates.")
            # print(edgetable[J][4])
            # print(edgetable[I][4])

        # update level norm
        if filltype == 6:
            # print("Test print edgetable for update check")
            # print(edgetable[J])
            edgetable[J][4] = vectoradd(edgetable[J][6] , edgetable[J][4])
            edgetable[I][4] = vectoradd(edgetable[I][6] , edgetable[I][4])



        # upon reaching the bottom of an edge, change to next edge
        if (y >= edgetable[I][2]) and (y < LastFillLine):
            I = next
            EdgeIX = edgetable[I][0]
            next+=1
        if (y >= edgetable[J][2]) and (y < LastFillLine):
            J = next
            EdgeJX = edgetable[J][0]
            next+=1




# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
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

# This function converts a list of 3D points to a single 3D reference point
# Returns reference points.
# For use with in-place transforms
def genreferencepoint(object):
    minX = object[0][0]
    maxX = object[0][0]
    minY = object[0][1]
    maxY = object[0][1]
    minZ = object[0][2]
    maxZ = object[0][2]

    i = 1

    while i < len(object):
        if object[i][0] < minX:
            minX = object[i][0]
        elif object[i][0] > maxX:
            maxX = object[i][0]
        if object[i][1] < minY:
            minY = object[i][1]
        elif object[i][1] > maxY:
            maxY = object[i][1]
        if object[i][2] < minZ:
            minZ = object[i][2]
        elif object[i][2] > maxZ:
            maxZ = object[i][2]
        i += 1

    refpoint = [((minX+maxX)/2), ((minY+maxY)/2), ((minZ+maxZ)/2)]
    return refpoint

# takes a reference point and generates a translation value required to center it on the origin
def gentransvector(point):
    transref = []

    for i in point:
        transref.append(-i)
    return transref

# Flat shading
def Flatshading():
    print("Flat Shading Algo")

# Gauroud shading
def Gauroud():
    print("Gauroud Algo")

# Phong shading
def Phong():
    print("Phong Shading Algo")


# generate a color hex code string from the illumination components
def triColorHexCode(ambient, diffuse, specular):
    combinedColorCode = colorHexCode(ambient + diffuse + specular)
    specularColorCode = colorHexCode(specular)
    colorString = "#" + specularColorCode + combinedColorCode + specularColorCode
    return colorString

def colorHexCode(intensity):
    if intensity > 1:
        intensity = 1
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

# **************************************************************************
# Everything below this point implements the interface
def reset():
    w.delete(ALL)
    resetPoly(PointCloudList[activeObjectIndex], ResetCloudList[activeObjectIndex])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def larger():
    w.delete(ALL)
    scale(PointCloudList[activeObjectIndex], 1.1)
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def smaller():
    w.delete(ALL)
    scale(PointCloudList[activeObjectIndex], .9)
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def forward():
    w.delete(ALL)
    translate(PointCloudList[activeObjectIndex], [0, 0, 5])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def backward():
    w.delete(ALL)
    translate(PointCloudList[activeObjectIndex], [0, 0, -5])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def left():
    w.delete(ALL)
    translate(PointCloudList[activeObjectIndex], [-5, 0, 0])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def right():
    w.delete(ALL)
    translate(PointCloudList[activeObjectIndex], [5, 0, 0])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def up():
    w.delete(ALL)
    translate(PointCloudList[activeObjectIndex], [0, 5, 0])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def down():
    w.delete(ALL)
    translate(PointCloudList[activeObjectIndex], [0, -5, 0])
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def xPlus():
    w.delete(ALL)
    referencept = genreferencepoint(PointCloudList[activeObjectIndex])
    transreference = gentransvector(referencept)
    translate(PointCloudList[activeObjectIndex], transreference)
    rotateX(PointCloudList[activeObjectIndex], 5)
    translate(PointCloudList[activeObjectIndex], referencept)

    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])




def xMinus():
    w.delete(ALL)
    referencept = genreferencepoint(PointCloudList[activeObjectIndex])
    transreference = gentransvector(referencept)
    translate(PointCloudList[activeObjectIndex], transreference)
    rotateX(PointCloudList[activeObjectIndex], -5)
    translate(PointCloudList[activeObjectIndex], referencept)

    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def yPlus():
    w.delete(ALL)
    referencept = genreferencepoint(PointCloudList[activeObjectIndex])
    transreference = gentransvector(referencept)
    translate(PointCloudList[activeObjectIndex], transreference)
    rotateY(PointCloudList[activeObjectIndex], 5)
    translate(PointCloudList[activeObjectIndex], referencept)

    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def yMinus():
    w.delete(ALL)
    referencept = genreferencepoint(PointCloudList[activeObjectIndex])
    transreference = gentransvector(referencept)
    translate(PointCloudList[activeObjectIndex], transreference)
    rotateY(PointCloudList[activeObjectIndex], -5)
    translate(PointCloudList[activeObjectIndex], referencept)

    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def zPlus():
    w.delete(ALL)
    referencept = genreferencepoint(PointCloudList[activeObjectIndex])
    transreference = gentransvector(referencept)
    translate(PointCloudList[activeObjectIndex], transreference)
    rotateZ(PointCloudList[activeObjectIndex], 5)
    translate(PointCloudList[activeObjectIndex], referencept)

    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


def zMinus():
    w.delete(ALL)
    referencept = genreferencepoint(PointCloudList[activeObjectIndex])
    transreference = gentransvector(referencept)
    translate(PointCloudList[activeObjectIndex], transreference)
    rotateZ(PointCloudList[activeObjectIndex], -5)
    translate(PointCloudList[activeObjectIndex], referencept)

    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

# def selPyramid():
#     global activeObjectIndex
#     w.delete(ALL)
#     for i in range(len(Polylist)):
#         drawObject(Polylist[i], ColorList[i])
#     activeObjectIndex = 0
#     drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])
#
#
# def selCube():
#     global activeObjectIndex
#     w.delete(ALL)
#     for i in range(len(Polylist)):
#         drawObject(Polylist[i], ColorList[i])
#     activeObjectIndex = 1
#     drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])
#
# def selRectPrism():
#     global activeObjectIndex
#     w.delete(ALL)
#     for i in range(len(Polylist)):
#         drawObject(Polylist[i], ColorList[i])
#     activeObjectIndex = 2
#     drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def selCylinder():
    global activeObjectIndex
    w.delete(ALL)
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    activeObjectIndex = 0
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def setline(event):
    global filltype
    filltype = 1
    print('Set 1')
    w.delete(ALL)
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def setfillline(event):
    global filltype
    filltype = 2
    w.delete(ALL)
    print("Set 2")
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def setfill(event):
    global filltype
    filltype = 3
    w.delete(ALL)
    print("Set 3")
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def setflatshading(event):
    global filltype
    filltype = 4
    w.delete(ALL)
    print("Set 4")
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def setgouraud(event):
    global filltype
    filltype = 5
    w.delete(ALL)
    print("Set 5")
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])

def setphong(event):
    global filltype
    filltype = 6
    w.delete(ALL)
    print("Set 6")
    for i in range(len(Polylist)):
        drawObject(Polylist[i], ColorList[i])
    #drawObjecthighlight(Polylist[activeObjectIndex], ColorList[activeObjectIndex])


root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=CanvasWidth, height=CanvasHeight)
# drawObject(Pyramid, ColorList[0])
# drawObject(Cube, ColorList[1])
# drawObject(RectPrism, ColorList[2])
w.pack()

#currsel and currcloud store the current selected poly and point cloud
currsel = Polylist[activeObjectIndex]
currcloud = PointCloudList[activeObjectIndex]
selCylinder()

controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="DN", command=down)
upButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=xPlus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=xMinus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=yPlus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=yMinus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=zPlus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=zMinus)
zMinusButton.pack(side=LEFT)

selectioncontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
selectioncontrols.pack(side=LEFT)

selectioncontrolslabel = Label(selectioncontrols, text="Select Poly")
selectioncontrolslabel.pack()

# selectPyramid = Button(selectioncontrols, text="Pyramid", command=selPyramid)
# selectPyramid.pack(side=LEFT)
#
# selectCube = Button(selectioncontrols, text="Cube", command=selCube)
# selectCube.pack(side=LEFT)
#
# selectRectPrism = Button(selectioncontrols, text="RectPrism", command=selRectPrism)
# selectRectPrism.pack(side=LEFT)

selectCylinder = Button(selectioncontrols, text="Cylinder", command=selCylinder)
selectCylinder.pack(side=LEFT)

#assign keybinds for drawing type selection
root.bind('1', setline)
root.bind('2', setfillline)
root.bind('3', setfill)
root.bind('4', setflatshading)
root.bind('5', setgouraud)
root.bind('6', setphong)

root.mainloop()
