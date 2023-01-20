import math
from Helper_Vector import *

class Light:
    def __init__ (self, x, y, z, r, g, b):
        self.position = PVector(x, y, z)
        self.Color = PVector(r, g, b)
        
class Surface:
    def __init__ (self, dr, dg, db, ar, ag, ab, sr, sg, sb, spec_power, k_refl):
        self.diffuseColor = PVector(dr, dg, db)
        self.ambientColor = PVector(ar, ag, ab)
        self.specularColor = PVector(sr, sg, sb)
        self.spec_power = spec_power
        self.k_refl = k_refl        
        
        
class Sphere:
    def __init__ (self, x, y, z, r, surface):
        self.xc = x
        self.yc = y
        self.zc = z
        self.r = r 
        self.surface = surface
        
    def intersect(self, ray):
        hit = None
        
        Ar = ((ray.rayDir.x)**2) + ((ray.rayDir.y)**2) + ((ray.rayDir.z)**2)
        Br = 2 * ((ray.rayDir.x * (ray.org.x - self.xc)) + (ray.rayDir.y * (ray.org.y - self.yc)) + (ray.rayDir.z * (ray.org.z - self.zc)))
        Cr = ((ray.org.x - self.xc)**2) + ((ray.org.y - self.yc)**2) + ((ray.org.z - self.zc)**2) - ((self.r)**2)        
        
        
        #intersection testing = if discriminant negative = doesnt hit sphere => discriminant var
        discrim = (Br)**2 - (4 * Ar * Cr)
        
        if discrim >= 0: 
            if Ar != 0:
            #if True:   
                #time
                t1 = (-Br + sqrt(discrim)) / (2 * Ar)
                t2 = (-Br - sqrt(discrim)) / (2 * Ar)
                
                # if debug_flag:
                #     print(t1)
                #     print(t2)
            
                #store all the place hit on an object
                if t1 >= 0:
                    posHit = PVector(ray.rayDir.x * t1 + ray.org.x, ray.rayDir.y * t1 + ray.org.y, ray.rayDir.z * t1 + ray.org.z) 
                    objC = PVector(self.xc, self.yc, self.zc)
                    N = PVector.sub(posHit, objC)
                    N.normalize()
                    
                    hit = Hit(t1, self, ray.rayDir.x * t1 + ray.org.x, ray.rayDir.y * t1 + ray.org.y, ray.rayDir.z * t1 + ray.org.z, N, ray)
                    #hitObj.append(hit)
                if t2 >= 0:
                    #where ray hit on obj
                    posHit = PVector(ray.rayDir.x * t2 + ray.org.x, ray.rayDir.y * t2 + ray.org.y, ray.rayDir.z * t2 + ray.org.z) 
                    #obj center position
                    objC = PVector(self.xc, self.yc, self.zc)
                    N = PVector.sub(posHit, objC)
                    N.normalize()    
                                            
                    hit = Hit(t2, self, ray.rayDir.x * t2 + ray.org.x, ray.rayDir.y * t2 + ray.org.y, ray.rayDir.z * t2 + ray.org.z, N, ray)
                    #hitObj.append(hit)
                    
        return hit
                
        

class Ray:
    def __init__ (self, org, rayDir):
        self.org = org
        self.rayDir = rayDir
        
        
class Hit:
    def __init__(self, time, object, xR, yR, zR, N, ray):
        self.time = time
        self.object = object
        self.surface = object.surface
        self.xR = xR
        self.yR = yR
        self.zR = zR
        #normal
        self.N = N
        #ray
        self.ray = ray

class Triangle:
    def __init__(self, surface):
        self.A = None
        self.B = None
        self.C = None
        self.surface = surface
        
    def drawLine(self, x, y, z):
        if self.A is None:
            self.A = PVector(x, y, z)
        elif self.B is None:
            self.B = PVector(x, y, z)
        elif self.C is None:
            self.C = PVector(x, y, z)
                        
    def intersect(self, ray):
        hit = None
        
        q = PVector.sub(self.A, ray.org)
        
        AB = PVector.sub(self.B, self.A) 
        CA = PVector.sub(self.A, self.C) 
        BC = PVector.sub(self.C, self.B) 
        
        AC = PVector.sub(self.C, self.A) #to find N
        
        #normal
        #N = PVector.cross(AC, AB) #old
        N = PVector.cross(AB, AC)
        N.normalize()
        
        # if PVector.dot(N, ray.rayDir) > 0:
        #     N = PVector.mult(N, -1)
        
        if PVector.dot(N, ray.rayDir) != 0:
            #time ray hit the object
            t = PVector.dot(N, q) / PVector.dot(N, ray.rayDir)
            
            if t < 0:
                return None
            
            #where ray hit on obj aka point p
            posHit = PVector(ray.rayDir.x * t + ray.org.x, ray.rayDir.y * t + ray.org.y, ray.rayDir.z * t + ray.org.z) 
            
            # BP = PVector.sub(posHit, self.B) #E1
            # AP = PVector.sub(posHit, self.A) #E2
            # CP = PVector.sub(posHit, self.C) #E3
            
            PB = PVector.sub(self.B, posHit) #E1
            PA = PVector.sub(self.A, posHit) #E2
            PC = PVector.sub(self.C, posHit) #E3
            
            # #area of smaller triangles
            A1 = PVector.dot(N, PVector.cross(PA, PB))
            A2 = PVector.dot(N, PVector.cross(PB, PC))
            A3 = PVector.dot(N, PVector.cross(PC, PA))
            
            #A1 = PVector.dot(N, PVector.cross(AP, AB))
            #A2 = PVector.dot(N, PVector.cross(BP, BC))
            #A3 = PVector.dot(N, PVector.cross(CP, CA))

            # A1 = PVector.dot(N, PVector.cross(PA, AB))
            # A2 = PVector.dot(N, PVector.cross(PB, BC))
            # A3 = PVector.dot(N, PVector.cross(PC, CA))            
                    
            if PVector.dot(N, ray.rayDir) > 0:
                N = PVector.mult(N, -1)
            
            if A1 >= 0 and A2 >= 0 and A3 >= 0:
            #if A1 < 0 and A2 < 0 and A3 < 0:
                hit = Hit(t, self, ray.rayDir.x * t + ray.org.x, ray.rayDir.y * t + ray.org.y, ray.rayDir.z * t + ray.org.z, N, ray)
        
        return hit
            
