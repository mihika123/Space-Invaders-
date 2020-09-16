"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special class
for it.  Unless you need something special for your extra gameplay features,
Ship and Alien could just be an instance of GImage that you move across the
screen. You only need a new class when you add extra features to an object. So
technically Bolt, which has a velocity, is really the only model that needs to
have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is
because there are a lot of constants in consts.py for initializing the objects,
and you might want to add a custom initializer.  With that said, feel free to
keep the pass underneath the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

Authors: Mihikaa Goenka (mg897), Oishani Ganguly (og58), 
Date: December 4th, 2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
#be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Creates and initializes a new Ship object.
        """
        super().__init__(x=GAME_WIDTH//2,y=SHIP_BOTTOM,width=SHIP_WIDTH,
        height=SHIP_HEIGHT,source='ship.png')


    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def _collidesship(self,bolt):
        """
        Returns: True if the bolt was fired by an alien and collides with the
        ship. Else returns False.

        Parameter bolt: The laser bolt to check.
        Precondition: bolt is an object of class Bolt.
        """
        k=False
        left_x=bolt.x-BOLT_WIDTH/2
        top_y=bolt.y+BOLT_HEIGHT/2
        right_x=bolt.x+BOLT_WIDTH/2
        bottom_y=bolt.y-BOLT_HEIGHT/2
        if self.contains((left_x,top_y)) or self.contains((right_x,top_y)):
            k=True
        elif self.contains((left_x,bottom_y))or self.contains((right_x,bottom_y)):
            k=True
        if bolt.getVelocity() < 0:
            return k
        return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GSprite):
    """
    A class to represent a single alien.
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x coordinate of the center of the alien.
        """
        return self.x


    def getY(self):
        """
        Returns the y coordinate of the center of the alien.
        """
        return self.y


    def setX(self,value):
        """
        Assigns value to the x coordinate of the center of the alien.

        Parameter value: the value of the x-coordinate
        Precondition: value is an int or float and 0.0<=x<=GAME_WIDTH
        """
        self.x=value


    def setY(self,value):
        """
        Assigns value to the y coordinate of the center of the alien.

        Parameter value: the value of the y-coordinate
        Precondition: value is an int or float and 0.0<=x<=GAME_HEIGHT
        """
        self.y=value


    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,src):
        """
        Creates and initializes a new Alien object.

        Parameter x: the value of the x-coordinate
        Precondition: x is an int or float and 0.0<=x<=GAME_WIDTH

        Parameter y: the value of the y-coordinate
        Precondition: y is an int or float and 0.0<=x<=GAME_HEIGHT

        Parameter src: the source of the image
        Precondition: src is a .png image file
        """

        super().__init__(x=x,y=y,width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
        source=src,format=(3,2))


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns: True if the bolt was fired by the player and collides with
        this alien.

        Parameter bolt: The laser bolt to check.
        Precondition: bolt is an object of class Bolt.
        """
        k=False
        left_x=bolt.x-BOLT_WIDTH/2
        top_y=bolt.y+BOLT_HEIGHT/2
        right_x=bolt.x+BOLT_WIDTH/2
        bottom_y=bolt.y-BOLT_HEIGHT/2
        if self.contains((left_x,top_y)) or self.contains((right_x,top_y)):
            k=True
        elif self.contains((left_x,bottom_y)) or self.contains((right_x,bottom_y)):
            k=True
        if bolt.getVelocity() > 0:
            return k
        return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _is_delete:     boolean value that checks to see if bolt should be deleted
    _isPlayerBolt:  boolean value that checks to see if bolt is fired by ship
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getPlayerBolt(self):
        """
        Returns the boolean value for when the bolt is fired by the ship and for
        when it is not.
        """
        return _isPlayerBolt


    def setPlayerBolt(self, value):
        """
        Sets the boolean value to value for when the bolt is fired by the ship
        and for when it is not.

        Parameter value: the value assigned to _isPlayerBolt
        Precondition: value is a boolean value
        """
        self._isPlayerBolt=value


    def getDelete(self):
        """
        Returns the boolean value for when the bolt exists and for when
        it does not.
        """
        return self._is_delete


    def setDelete(self, value):
        """
        Sets the boolean value to value for when the bolt exists and for when
        it does not.

        Parameter value: the value assigned to _is_delete
        Precondition: value is a boolean value
        """
        self._is_delete=value


    def getVelocity(self):
        """
        Returns the value of the velocity of the bolt.
        """
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,v,col):
        """
        Creates and initializes a new Bolt object.

        Parameter x: the value of the x-coordinate
        Precondition: x is an int or float and 0.0<=x<=GAME_WIDTH

        Parameter y: the value of the y-coordinate
        Precondition: y is an int or float and 0.0<=x<=GAME_HEIGHT

        Parameter v: the velocity of the bolt
        Precondition: v is an int or float

        Parameter col: the color of the bolt
        Precondition: col must be an RGB object
        """
        super().__init__(x=x,y=y,width=BOLT_WIDTH,height=BOLT_HEIGHT,
        linecolor=col,fillcolor=col)
        self._velocity=v
        self._is_delete=self.setDelete(False)
        self._isPlayerBolt=self.setPlayerBolt(False)

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
