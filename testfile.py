import raytracing

sphere = raytracing.sphere(2, [5, 4 , 10], raytracing.normalvector([255, 0, 0]))

spherelist = []
spherelist.append(sphere)

startpoint = [0,0,0]

ray = [5, 4, 12]

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

            intersect.append(raytracing.vectoradd(startPoint, raytracing.scalarMult(ray, t)))
            intersect.append(i)
            
            return intersect
        elif discriminant > 0:
            t = (-b + discriminant)/(2 * a)
            t2 = (-b - discriminant)/(2 * a)

            # verify which root gives you the closer intersect
            if t2 < t:
                t = t2

            intersect.append(raytracing.vectoradd(startPoint, raytracing.scalarMult(ray, t)))
            intersect.append(i)
            return intersect

print(f"This is the intersect {findClosestIntersect(startpoint, ray)}")