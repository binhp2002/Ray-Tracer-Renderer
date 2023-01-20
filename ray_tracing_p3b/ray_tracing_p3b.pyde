# Phong Duong

# This is the provided code for the ray tracing project.
#
# The most important part of this code is the command interpreter, which
# parses the scene description (.cli) files.

from __future__ import division
import traceback

from Helper import *
from Helper_Vector import *

debug_flag = False   # print debug information when this is True

shapes = []
backgroundColor = [0,0,0]
fov = 0
eyePos = (0,0,0)
u = (0, 0, 0)
v = (0, 0, 0)
w = (0, 0, 0)
light = []
surfaceMat = None

def setup():
    size(320, 320) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)
    frameRate(30)

# make sure proper error messages get reported when handling key presses
def keyPressed():
    try:
        handleKeyPressed()
    except Exception:
        traceback.print_exc()

# read and interpret a scene description .cli file based on which key has been pressed
def handleKeyPressed():
    if key == '1':
        interpreter("01_one_sphere.cli")
    elif key == '2':
        interpreter("02_three_spheres.cli")
    elif key == '3':
        interpreter("03_shiny_sphere.cli")
    elif key == '4':
        interpreter("04_many_spheres.cli")
    elif key == '5':
        interpreter("05_one_triangle.cli")
    elif key == '6':
        interpreter("06_icosahedron_and_sphere.cli")
    elif key == '7':
        interpreter("07_colorful_lights.cli")
    elif key == '8':
        interpreter("08_reflective_sphere.cli")
    elif key == '9':
        interpreter("09_mirror_spheres.cli")
    elif key == '0':
        interpreter("10_reflections_in_reflections.cli")
    elif key == '-':
        interpreter("11_star.cli")

# You should add code for each command that calls routines that you write.
# Some of the commands will not be used until Part B of this project.
def interpreter(fname):
    global Tri
    
    reset_scene()  # you should initialize any data structures that you will use here
    
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # parse the lines in the file in turn
    for line in lines:
        words = line.split()  # split up the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            global shapes
            global surfaceMat
            
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            radius = float(words[1])
            
            # call your sphere making routine here
            # for example: create_sphere(x,y,z,radius)
            circular = Sphere(x, y, z, radius, surfaceMat)
            shapes.append(circular)
            
            pass
        elif words[0] == 'fov':
            global fov
            fov = float(words[1])
            pass
        elif words[0] == 'eye':
            global eyePos
            ex = float(words[1])
            ey = float(words[2])
            ez = float(words[3])
            eyePos = PVector(ex, ey, ez)
            pass
        elif words[0] == 'uvw':
            #store u v w as vector class then do multp in render
            global u
            global v
            global w
            
            ux = float(words[1])
            uy = float(words[2])
            uz = float(words[3])
            vx = float(words[4])
            vy = float(words[5])
            vz = float(words[6])
            wx = float(words[7])
            wy = float(words[8])
            wz = float(words[9])
            
            
            u = PVector(ux, uy, uz)
            v = PVector(vx, vy, vz)
            w = PVector(wx, wy, wz) 
            pass
        elif words[0] == 'background':
            global backgroundColor
            r = float(words[1])
            g = float(words[2])
            b = float(words[3])
            backgroundColor = [r, g, b]
            pass
        elif words[0] == 'light':
            global light
            x, y, z = float(words[1]), float(words[2]), float(words[3])
            r, g, b = float(words[4]), float(words[5]), float(words[6])
            l = Light(x, y, z, r, g, b)
            light.append(l)
            pass
        elif words[0] == 'surface':
            global surfaceMat
            dr, dg, db = float(words[1]), float(words[2]), float(words[3])
            ar, ag, ab = float(words[4]), float(words[5]), float(words[6])
            sr, sg, sb = float(words[7]), float(words[8]), float(words[9])
            spec_power = float(words[10])
            k_refl = float(words[11])
            
            surfaceMat = Surface(dr, dg, db, ar, ag, ab, sr, sg, sb, spec_power, k_refl)            
            pass
        elif words[0] == 'begin':
            #global Tri
            Tri = Triangle(surfaceMat)
            
            pass
        elif words[0] == 'vertex':
            Tri.drawLine(float(words[1]), float(words[2]), float(words[3]))
            
            pass
        elif words[0] == 'end':
            shapes.append(Tri)
            
            pass
        elif words[0] == 'render':
            render_scene()    # render the scene (this is where most of the work happens)
        elif words[0] == '#':
            pass  # ignore lines that start with the comment symbol (pound-sign)
        else:
            print ("unknown command: " + word[0])

# render the ray tracing scene
def render_scene(): #help
    
    global debug_flag
    global eyePos

    d = 1/tan(radians(fov/2))
    for j in range(height):
        for i in range(width):
            U = (2.0 * i / width) - 1
            #V = (2 * j / height) - 1
            V = -1 * (2.0 * j / height - 1)
            
            if i % 20 == 0 and j == 0:
                print("Pixel %d, %d" % (i, j)) #to check progress
            
            #ray direction
            #rayDirec = (-d * w) + (V * v) + (U * u)
            rayDir = PVector.mult(w, -1 * d)
            V = PVector.mult(v, V)
            rayDir = PVector.add(V, rayDir)
            U = PVector.mult(u, U)
            rayDir = PVector.add(U, rayDir)
            rayDir.normalize()
                                       
            #ray origin aka eye
            #org = PVector(0, 0, 0)
            org = eyePos
            
            #creating ray
            ray = Ray(org, rayDir)
            
            ### put in new func
            #closest object hit along with its pixel coordination
            hitP = rayIntersectscene(ray, None)   
            
            pix_color = backgroundColor 
            #set background color to backgroundColor if no hit                       
            if hitP == None:
                #background(backgroundColor)
                pix_color = backgroundColor
                #print("no hit")
            else: 
                #for objP in hitP:
                #R, G, B = shading(hitP, 100)    
                #pix_color = color(R, G, B) 
                
                hitColor = shading(hitP, 10)
                pix_color = [hitColor.x, hitColor.y, hitColor.z]
                   
                #pix_color = color(1, 1, 1)
                #print("hit")  
                
            #extra level to count how many reflection to do to stop 
            #in shading func, call new ray     
            ###
            
            
            # Maybe set a debug flag to true for ONE pixel.
            # Have routines (like ray/sphere intersection)print extra information if this flag is set.
            debug_flag = False
            if i == 233 and j == 191:
                debug_flag = True
                


            # create an eye ray for pixel (i,j) and cast it into the scene
            #pix_color = color(0.8, 0.2, 0.3)  # you will calculate the correct pixel color here using ray tracing
            #set (i, height - j, pix_color)
            set (i, j, color(pix_color[0], pix_color[1], pix_color[2]))         # draw the pixel with the calculated color

#shading function
def shading(objP, mDepth): #shadow and reflection wrong
    res = PVector(0, 0, 0)
    totalR = PVector(0,0,0)
    
    shadowOrg = PVector.mult(objP.N, 0.0001)
    
    #ambient color 
    #temp10 = PVector.pairwise_mult(objP.surface.ambientColor, l.Color)
    #res = PVector.add(res, temp10)
    res = PVector.add(res, objP.surface.ambientColor)
    
    for l in light:
        
        #mDepth -= 1
               
        
        #making shadow
        intersection = PVector(objP.xR, objP.yR, objP.zR)
        #shadowOrg = PVector.mult(objP.N, 0.0001)
        shadowRay = Ray(PVector.add(intersection, shadowOrg), PVector.sub(l.position, intersection))
        shadowHit = rayIntersectscene(shadowRay, objP.object)
        
        # if debug_flag:
        #     if isinstance(shadowHit.object, Triangle):
        #         print("triangle")
        #     else:
        #         print("sphere")
        
        if shadowHit is not None and shadowHit.time < 1:
        #if shadowHit is not None and shadowHit.time < (PVector.sub(l.position, intersection)).mag():
            continue
        
        #Cl * Co
        temp = PVector(l.Color.x * objP.surface.diffuseColor.x,
                l.Color.y * objP.surface.diffuseColor.y,
                l.Color.z * objP.surface.diffuseColor.z)
        
        #can use .normalize() for |v|
        L = PVector(l.position.x - objP.xR, l.position.y - objP.yR, l.position.z - objP.zR)
        L.normalize()            
        

        cosTheta = PVector.dot(objP.N, L)
        
    
        diffuse = PVector.mult(temp, max(0, cosTheta))
        
        
        temp2 = PVector(diffuse.x, diffuse.y, diffuse.z)
        
        #diffuse color
        res = PVector.add(res, temp2)
        
        #ambient color 
        #temp10 = PVector.pairwise_mult(objP.surface.ambientColor, l.Color)
        #res = PVector.add(res, temp10) 
        #res = PVector.add(res, objP.surface.ambientColor)  
        
        #specular color
        #L1 = PVector(l.position.x - objP.xR, l.position.y - objP.yR, l.position.z - objP.zR).normalize()

        H = PVector.sub(L, objP.ray.rayDir.normalize()).normalize()

        specCont = max(0, (PVector.dot(objP.N, H))**(objP.surface.spec_power))
        temp11 = PVector.pairwise_mult(objP.surface.specularColor, l.Color)
        temp3 = PVector.mult(temp11, specCont)
        res = PVector.add(res, temp3)
                
        
    # reflection
    #E = (PVector.sub(eyePos, intersection)).normalize()
    #intersection = PVector(objP.xR, objP.yR, objP.zR)
    
    E = PVector.mult(objP.ray.rayDir, -1)
    
    #R = 2(E . N)N - E
    # x1 = PVector.dot(E, objP.N)
    # x2 = PVector.mult(objP.N, x1)
    # x3 = PVector.mult(x2, 2)
    # R_dir = PVector.sub(x3, E).normalize()

    # temp4 = PVector.mult(R_dir, 0.0001)
    # temp5 = PVector.add(intersection, temp4)
        
    # R = d + (2 (N dot (-d))) * N
    x1 = (PVector.dot(objP.ray.rayDir, objP.N) * -2)
    x2 = PVector.mult(objP.N, x1)
    R_dir = PVector.add(x2, objP.ray.rayDir).normalize()

    temp4 = PVector.mult(R_dir, 0.0001)
    temp5 = PVector.add(intersection, temp4)                
    
    #refRay = Ray(intersection + 0.0001 * R_dir, R_dir)
    refRay = Ray(temp5, R_dir)
    refHit = rayIntersectscene(refRay, None)
    
    backgroundVector = PVector(backgroundColor[0], backgroundColor[1], backgroundColor[2])
    
    totalR = PVector(0,0,0)
    
    if refHit is not None and refHit.time > 0:
        #if mDepth > 0 and objP.surface.k_refl > 0:
        if mDepth > 0:
            totalR = PVector.add(PVector.mult(shading(refHit, mDepth - 1), objP.surface.k_refl), totalR)
            #mDepth -= 1
    else:
        #print("bg color is", backgroundVector, "krefl is", objP.surface.k_refl)
        totalR = PVector.add(PVector.mult(backgroundVector, objP.surface.k_refl), totalR)
    
    res = PVector.add(res, totalR)

        #ambient color 
        #temp10 = PVector.pairwise_mult(objP.surface.ambientColor, l.Color)
        #res = PVector.add(res, temp10) 
        #res = PVector.add(res, objP.surface.ambientColor)                    
        
        #if debug_flag:
          #print("normal is: ", objP.N, "total color is: ", res, "diffuse color is: ", objP.surface.diffuseColor, "specular contribution is: ", specCont)
          #print ("color rgb is: ", res, "depth is: ", mDepth)
        
    #ambient color 
    #temp10 = PVector.pairwise_mult(objP.surface.ambientColor, l.Color)
    #res = PVector.add(res, temp10)
    #res = PVector.add(res, objP.surface.ambientColor)
    
    return PVector(res.x, res.y, res.z)

# here you should reset any data structures that you will use for your scene (e.g. list of spheres)
def reset_scene():
    global shapes
    global backgroundColor
    global fov
    global eyePos
    global u
    global v
    global w
    global light
    global surfaceMat
    global vertices
    
    shapes = [] 
    backgroundColor = [0,0,0]
    fov = 0
    eyePos = (0,0,0)
    u = (0, 0, 0)
    v = (0, 0, 0)
    w = (0, 0, 0)
    light = []
    surfaceMat = None    


#need pairwise product to have vector x vector
def pairwisePro(a, b):
    x = a.x * b.x
    y = a.y * b.y
    z = a.z * b.z
    pairwise = PVector(x, y, z)
    return pairwise

#closest sphere hit function
def rayIntersectscene(ray, exclude):
    
    #closest object hit along with its pixel coordination
    hitP = None
    
    #all objects hit along with its pixel coordination
    #hitObj = []
    
    minT = 9999999999999
    
    #loop thru shapes to find all objects hit
    for obj in shapes:
        
        if obj is exclude:
            continue
        
        #all the place intersect on an object
        currHit = obj.intersect(ray)

        #choose smaller time among places hit in an obj   
        if currHit is not None and currHit.time <= minT:
            minT = currHit.time
            hitP = currHit        
    
    return hitP     


# prints mouse location clicks, for help debugging
def mousePressed():
    print ("You pressed the mouse at " + str(mouseX) + " " + str(mouseY))

# this function should remain empty for this assignment
def draw():
    pass
