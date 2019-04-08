import sys
import math

class Punto:
    coor_x=0
    coor_y=0
    
    def __init__(self,_x=0.0,_y=0.0):
        self.coor_x = _x
        self.coor_y = _y
    
    def getX(self):
        return self.coor_x
    
    def getY(self):
        return self.coor_y
    
    def setX(self,val_x):
        self.coor_x=val_x
    
    def setY(self,val_y):
        self.coor_y=val_y
    
    def tradurcirAPolares(self,x,y):
        c1=math.sqrt(x*x+y*y)
        c2=0
        if x == 0:
            if y > 0:
                c2=90
            elif y < 0:
                c2=270
        elif x > 0:
            if y > 0:
                c2= math.atan(y/x)
            elif y < 0:
                c2=360-math.atan(y/x)
        else:
            if y > 0:
                c2= 180- math.atan(y/x)
            elif y < 0:
                c2=180+math.atan(y/x)
            else:
                c2=270
        return [c1,c2]