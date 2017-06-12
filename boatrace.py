"""
spaceshooter.py
Author: will laycock
Credit: me

Assignment:
Write and submit a program that implements the spacewar game:
https://github.com/HHS-IntroProgramming/Spacewar
"""
from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame
from math import sin, cos, pi, sqrt

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class BigExplosion(Sprite):
    
    asset = ImageAsset("images/explosion2.png", Frame(0,0,4800/25,195), 25)
    
    def __init__(self, position):
        super().__init__(BigExplosion.asset, position)
        self.image = 0
        self.center = (0.5, 0.5)
        
    def step(self):
        self.setImage(self.image//2) 
        self.image = self.image + 1
        if self.image == 50:
            self.destroy()

class Ocean(Sprite):

    asset = ImageAsset("images/toonvectors-83952-140.jpg")

    def __init__(self, position):
        super().__init__(Ocean.asset, position)

class Buoy(Sprite):
    
    asset = ImageAsset("images/float-clipart-life-buoy-md.png")
    
    ap = 0
    
    def __init__(self, position, rotation, next):
        super().__init__(Buoy.asset, position)
        self.prev=None
        self.visible=False
        self.next=next
        if self.next != None:
            self.next.prev=self
        self.rotation = rotation
        self.mass = 30*1000
        self.scale=0.075
        self.fxcenter = 0.5
        self.fycenter = 0.5
        self.circularCollisionModel()
        self.occurab=False
        self.occurbc=False
    
    def step(self):
        ab=self.collidingWithSprites(Ship)
        bc=self.collidingWithSprites(Ship2)
        if self.visible and ((not self.prev) or self.prev.occurab):
            if len(ab) > 0:
                self.occurab=True
            if self.next==None and len(ab) > 0 and myapp.ss.won==False:
                myapp.ss.won = True
                myapp.sv.explode()
        if self.visible and ((not self.prev) or self.prev.occurbc):
            if len(bc) > 0:
                self.occurbc=True
            if self.next==None and len(bc) > 0 and myapp.sv.won==False:
                myapp.sv.won = True
                myapp.ss.explode()
        if self.occurab and self.occurbc:
            self.visible=False
        if (self.prev==None or self.prev.occurab) and len(ab) and self.next != None:
            self.next.visible=True
        if (self.prev==None or self.prev.occurbc) and len(bc) and self.next != None:
            self.next.visible=True

                
            
class Buoy1(Buoy):
    def __init__(self, next):
        super().__init__((myapp.width-150,myapp.height/2), pi/2, next)
        self.visible=True
        
class Buoy2(Buoy):
    def __init__(self, next):
        super().__init__((myapp.width*(3/5),myapp.height/4), pi/2, next)
        
        
class Buoy3(Buoy):
    def __init__(self, next):
        super().__init__((myapp.width*(1/4),myapp.height*(4/7)), (2*pi)/3, next)
        
class Buoy4(Buoy):
    def __init__(self, next):
        super().__init__((myapp.width*(5/6),myapp.height*(6/7)), (pi)/8, next)
    
class Buoy5(Buoy):
    def __init__(self, next):
        super().__init__((myapp.width*(2/7),myapp.height*(6/7)), (5*pi)/6, next)
    
class Ship(Sprite):
    asset = ImageAsset("images/Rivamare-Birds-eye-view-drawing.png")

    def __init__(self, position):
        super().__init__(self.asset, position)
        self.scale=0.05
        self.vx = 1
        self.vy = 1
        self.vr = 0
        self.rotation=(7*pi)/4
        self.v = 0
        self.thrust = 0
        self.thrustframe = 1
        self.assignkeys()
        self.initposition = position
        self.fxcenter = self.fycenter = 0.5
        self.won = False
        """self.buoy1l=0
        self.buoy2l=0
        self.buoy3l=0
        self.buoy4l=0
        self.buoy5l=0
        self.buoy1s=0
        self.buoy2s=0
        self.buoy3s=0
        self.buoy4s=0
        self.buoy5s=0"""
    
    def assignkeys(self):
        BoatGame.listenKeyEvent("keydown", "up arrow", self.thrustOn)
        BoatGame.listenKeyEvent("keyup", "up arrow", self.thrustOff)
        BoatGame.listenKeyEvent("keydown", "left arrow", self.turnleft)
        BoatGame.listenKeyEvent("keyup", "left arrow", self.turnoff)
        BoatGame.listenKeyEvent("keydown", "right arrow", self.turnright)
        BoatGame.listenKeyEvent("keyup", "right arrow", self.turnoff)
    
    def step(self):
        vx = cos(self.rotation) * self.v
        vy = -sin(self.rotation) * self.v
        self.x += vx
        self.y += vy
        self.rotation += self.vr
        if self.x > myapp.width:
            self.x = 65
            self.y = 50
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.x < 0:
            self.x = 65
            self.y=50
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.y > myapp.height:
            self.x = 65
            self.y = 50
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.y < 0:
            self.x = 65
            self.y = 50
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.thrust == 0 and self.v >= 0.1:
            self.v -= 0.05
        if self.thrust == 1 and self.v == 0:
            self.v = 1
        if self.thrust == 1:
            self.setImage(self.thrustframe)
            self.thrustframe += 1
            if self.thrustframe == 4:
                self.thrustframe = 1
            if self.v < 5:
                self.v += 0.05

    def thrustOn(self, event):
        self.thrust = 1
        
    def explode(self):
        BigExplosion((self.x,self.y))
        self.destroy()
        
    def thrustOff(self, event):
        self.thrust = 0
    
    def turnleft(self, event):
        self.vr = 0.05
    
    def turnoff(self, event):
        self.vr = 0
        
    def turnright(self, event):
        self.vr = -0.05
        
class Ship2(Ship):
    asset = ImageAsset("images/boat10.png")
    
    def assignkeys(self):
        self.scale=0.075
        BoatGame.listenKeyEvent("keydown", "w", self.thrustOn)
        BoatGame.listenKeyEvent("keyup", "w", self.thrustOff)
        BoatGame.listenKeyEvent("keydown", "a", self.turnleft)
        BoatGame.listenKeyEvent("keyup", "a", self.turnoff)
        BoatGame.listenKeyEvent("keydown", "d", self.turnright)
        BoatGame.listenKeyEvent("keyup", "d", self.turnoff)
    
    def step(self):
        vx = cos(self.rotation) * self.v
        vy = -sin(self.rotation) * self.v
        self.x += vx
        self.y += vy
        self.rotation += self.vr
        if self.x > myapp.width:
            self.x = 65-sqrt(300)
            self.y = 50+sqrt(300)
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.x < 0:
            self.x = 65-sqrt(300)
            self.y = 50+sqrt(300)
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.y > myapp.height:
            self.x = 65-sqrt(300)
            self.y = 50+sqrt(300)
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.y < 0:
            self.x = 65-sqrt(300)
            self.y = 50+sqrt(300)
            self.v = 0
            self.thrust = 0
            self.rotation = (7*pi)/4
        if self.thrust == 0 and self.v >= 0.1:
            self.v -= 0.05
        if self.thrust == 1 and self.v == 0:
            self.v = 1
        if self.thrust == 1:
            self.setImage(self.thrustframe)
            self.thrustframe += 1
            if self.thrustframe == 4:
                self.thrustframe = 1
            if self.v < 5:
                self.v += 0.05
        else:
            self.setImage(0)
    """def ship1wins(self):
        self.visbile=False"""

class tally1(Sprite):
    asset = ImageAsset("images/Tally1.png")
    
    def __init__(self, position):
        super().__init__(self.asset, position)
        self.scale=0.075
        self.fxcenter = self.fycenter = 0.5
        
class tally2(Sprite):
    asset = ImageAsset("images/Tally2.png")
    
    def __init__(self, position):
        super().__init__(self.asset, position)
        self.scale=0.075
        self.fxcenter = self.fycenter = 0.5

class tally3(Sprite):
    asset = ImageAsset("images/Tally3.png")
    
    def __init__(self, position):
        super().__init__(self.asset, position)
        self.scale=0.075
        self.fxcenter = self.fycenter = 0.5

class tally4(Sprite):
    asset = ImageAsset("images/Tally4.png")
    
    def __init__(self, position):
        super().__init__(self.asset, position)
        self.scale=0.075
        self.fxcenter = self.fycenter = 0.5

class tally5(Sprite):
    asset = ImageAsset("images/Tally5.png")
    
    def __init__(self, position):
        super().__init__(self.asset, position)
        self.scale=0.075
        self.fxcenter = self.fycenter = 0.5


class BoatGame(App):
    def __init__(self, width, height):
        super().__init__()
        ocean = Ocean((0,0))
        tal = tally5((self.width-50, 30))
        ocean.scale = self.width/ocean.width
        self.ss = Ship((65,50))
        self.sv = Ship2((65-sqrt(300),50+sqrt(300)))

        
    def step(self):
        for ship in self.getSpritesbyClass(Ship):
            ship.step()
        for ship in self.getSpritesbyClass(Ship2):
            ship.step()
        for exp in self.getSpritesbyClass(BigExplosion):
            exp.step()
            
        b1.step()
        b2.step()
        b3.step()
        b4.step()
        b5.step()
        
            


myapp = BoatGame(SCREEN_WIDTH, SCREEN_HEIGHT)
b5 = Buoy5(None)
b4 = Buoy4(b5)
b3 = Buoy3(b4)
b2 = Buoy2(b3)
b1 = Buoy1(b2)
myapp.run()
