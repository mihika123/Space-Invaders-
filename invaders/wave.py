"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave.  Whenever you
move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer.

Authors: Mihikaa Goenka (mg897), Oishani Ganguly(og58)
Date: December 4th, 2018
"""
from game2d import *
from consts import *
from models import *
import random
import sys

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
#permitted to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary. It
    also marches the aliens back and forth across the screen until they are all
    destroyed or they reach the defense line (at which point the player loses).
    When the wave is complete, you should create a NEW instance of Wave
    (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    This class will be similar to that one in how it interacts with the main
    class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of
                 Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt,
                 possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but you
    MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter
    for any attribute that you need to access in Invaders.  Only add the getters
    and setters that you need for Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may
    want to keep track of the score.  You also might want some label objects to
    display the score and number of lives. If you make changes, please list the
    changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _music:     the sound played with every step the aliens take and the
                background music when game is paused [Sound]
    _pew1:      the sound played when ship fires bolt [Sound]
    _pew2:      the sound played when aliens fire bolts [Sound]
    _blast1:    the sound played when aliens are destroyed [Sound]
    _blast2:    the sound played when the ship is destroyed [Sound]
    _pop2:      the sound played when the ship intercepts a power-up bolt [Sound]
    _alienscopy:2d list of Alien objects that stores a deep copy of _aliens
    _alienbolts:the random number of steps the aliens take before firing a bolt
                [1<=_alienbolts<=BOLT_RATE]
    _noaliens:  the value of the number of aliens when all have been killed
    _speed:     stores the speed of the aliens [_speed=ALIEN_SPEED]
    _movingR:   boolean value that keeps track of whether the aliens are moving
                right or left at any point
    _numMarch:  the number of steps taken by the aliens yet
    _score:     the score of the player [GLabel]
    _livestext2:stores the number of lives remaining for the player [GLabel]
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getScore(self):
        """
        Returns the text attribute of the player's score.

        This method returns the GLabel object _score's text attribute directly.
        """
        return self._score.text


    def UpdateScore(self, val):
        """
        Adds the score 'val' to the player's previous score text as an integer
        and converts it to a string.

        Parameter val: The value to add to self._score.text
        Precondition:  val is an int >=0
        """
        newscore=int(self._score.text)+val
        self._score.text=str(newscore)


    def getNoAliens(self):
        """
        Returns the attribute _noaliens directly.
        """
        return self._noaliens


    def setNoAliens(self, value):
        """
        Sets the attribute _noaliens to value.

        Parameter value: The value to assign to self._noaliens
        Precondition:  value is an int >=0
        """
        self._noaliens=value


    def getLives(self):
        """
        Returns the number of lives of the player directly.
        """
        return self._lives


    def UpdateLives(self):
        """
        Deducts 1 from the player's current number of  lives and converts it to
        a string.
        """
        self._lives-=1
        self._livestext2.text=str(self._lives)


    '''def UpdateNewLife(self):
        self._lives+=1
        self._livestext2.text=str(self._lives)
    '''

    def getMusic(self):
        """
        Returns the marching-cum-background music of the game.
        """
        return self._music


    def getPew1(self):
        """
        Returns the the sound of the ship firing a bolt.
        """
        return self._pew1


    def getPew2(self):
        """
        Returns the the sound of the aliens firing a bolt.
        """
        return self._pew2


    def getBlast1(self):
        """
        Returns the the sound of the ship being destroyed.
        """
        return self._blast1


    def getBlast2(self):
        """
        Returns the the sound of an alien being destroyed.
        """
        return self._blast2


    def getPop2(self):
        """
        Returns the the sound of the ship intercepting a power-up bolt.
        """
        return self._pop2


    def getShip(self):
        """
        Returns the ship objects.
        """
        return self._ship


    def setShip(self):
        """
        Creates a Ship object and assigns it the attribute _ship.
        """
        self._ship=Ship()


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def initaliens(self):
        """
        Creates and returns a 2d list of alien objects.

        The 2d list is created in a bottom up manner with adjacent pairs of rows
        being the same kind of aliens.
        """
        aliens=[]
        k=ALIEN_ROWS-1
        for row in range(ALIEN_ROWS):
            alienrow=[]
            for alien in range(ALIENS_IN_ROW):
                if row%6==0 or row%6==1:
                        c=0
                elif row%6==2 or row%6==3:
                        c=1
                else:
                        c=2
                x=ALIEN_H_SEP*(alien+1)+0.5*ALIEN_WIDTH+ALIEN_WIDTH*alien
                y=(GAME_HEIGHT-ALIEN_CEILING)-(ALIEN_V_SEP*k)-(ALIEN_HEIGHT*k)-\
                (0.5*ALIEN_HEIGHT)
                alienrow.append(Alien(x,y,ALIEN_IMAGES[c]))
            k-=1
            aliens.append(alienrow)
        return aliens


    def __init__(self):
        """
        Initialises all the instance attributes.
        """
        self._ship=Ship()
        self._aliens=self.initaliens()
        self._bolts=[]
        self._dline=GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
        linewidth=2,linecolor='red')
        self._lives=SHIP_LIVES
        self._time=0
        self._music=Sound('126347_latin_alienican.wav')
        self._pew1=Sound('pew1.wav')
        self._pew2=Sound('pew2.wav')
        self._blast1=Sound('blast1.wav')
        self._blast2=Sound('blast2.wav')
        self._pop2=Sound('pop2.wav')
        self.movingR=True
        self._alienscopy=[]
        for i in range(len(self._aliens)):
            self._alienscopy.append(self._aliens[i][:])
        self._alienbolts=random.randint(1,BOLT_RATE)
        self._score=GLabel(text=str(0), font_size=40,
        font_name='Arcade.ttf',x=GAME_WIDTH/10 + 100,y=GAME_HEIGHT-\
        GAME_HEIGHT/16,
        fillcolor='black',linecolor='yellow')
        self._noaliens=ALIENS_IN_ROW*ALIEN_ROWS
        self._livestext2=GLabel(text=str(self.getLives()), font_size=40,
        font_name='Arcade.ttf',x=GAME_WIDTH-GAME_WIDTH/20,\
        y=GAME_HEIGHT-GAME_HEIGHT/16,
        fillcolor='black',linecolor='green')
        self._speed=ALIEN_SPEED
        self._numMarch=0


    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input,dt):
        """
        Method to move the ship, aliens, regular bolts, and power-up bolts.

        This method fires both alien bolts and ship bolts and deletes them on
        collision or when the reach the end of the game window.

        Parameter input: the user input used to control the ship and change state
        Precondition: input is an instance of GInput; it is inherited from
        GameApp

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._moveShip(input)
        self._moveAlien(dt)
        for bolt in self._bolts:
            if bolt._isPlayerBolt==False:
                self._collisionship(bolt)
        self._determineFire(input, self._aliens)
        self._DeleteBolt()


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the player score, player lives, the ship, the defense line,
        the aliens, and the bolts on the game window.

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView; it is inherited from GameApp
        """
        self._score.draw(view)
        self._livestext2.draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        for b in self._bolts:
            b.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    def _determineFire(self,input, aliens):
        """
        Determines the current arrow key pressed, creates a Bolt object and
        fires a laser bolt from the ship accordingly.

        This method checks for an up arrow key press, and if there is
        one, creates a Bolt object and fires a laser bolt in the upward
        direction.  A key press is when a key is pressed EVERY TIME. We want a
        bolt to fire when the previous bolt has killed an alien OR when the
        previous bolt has reached the end of the game window.

        Parameter input: the user input used to control the ship and change state
        Precondition: input is an instance of GInput; it is inherited from
        GameApp

        Parameter aliens: the list of aliens
        Precondition: aliens is a 2d list of Alien objects
        """
        if input.is_key_down('up'):
            y=SHIP_HEIGHT+BOLT_HEIGHT/2
            c=0
            for bolt in self._bolts:
                if bolt._velocity>0:
                    bolt.setPlayerBolt(True)
                    c+=1
            if c==0 and self._ship is not None:
                bolt=Bolt(self._ship.x,y,BOLT_SPEED,'blue')
                self._pew1.play(loop=False)
                self._bolts.append(bolt)
        for bolt in self._bolts:
            bolt.y+=bolt.getVelocity()
            self._collision(bolt)
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].y-BOLT_HEIGHT/2 > GAME_HEIGHT:
                del self._bolts[i]
            else:
                i += 1


    def _collision(self, bolt):
        """"
        Checks whether a bolt from the ship has collided with an alien.

        If a collision has been detected, it destroys the alien by making it a
        None object and increases the score by a value.

        Parameter bolt: the bolt with which the collision is being checked
        Precondition: bolt is a Bolt object
        """
        for row in range(ALIEN_ROWS) :
            if row>=0 and row<ALIEN_ROWS/3:
                val=10
            elif row>=ALIEN_ROWS/3 and row<2*ALIEN_ROWS/3:
                val=30
            else:
                val=50
            for alien in range(ALIENS_IN_ROW):
                if self._aliens[row][alien]is not None and \
                bolt._isPlayerBolt:
                    if (self._aliens[row][alien].collides(bolt)):
                        self._aliens[row][alien]=None
                        self.UpdateScore(val)
                        self._blast1.play(loop=False)
                        bolt.setDelete(True)
                        self._AliensOver()


    def _AliensOver(self):
        """
        If all the aliens have been killed successfully, sets the attribute
        _noaliens to 0.
        """
        k=0
        for row in self._aliens:
            for alien in row:
                if alien is None:
                    k+=1
        if (k==(ALIEN_ROWS*ALIENS_IN_ROW)):
            self.setNoAliens(0)


    def _DeleteBolt(self):
        """
        Deletes a bolt.
        """
        i=0
        while i < len(self._bolts):
            if self._bolts[i].getDelete():
                del self._bolts[i]
            else:
                i += 1


    def _shipExist(self):
        """
        Returns True if the ship has been killed. False otherwise.
        """
        if self.getShip() is None:
            return True
        return False


    def _alienFire(self):
        """
        Creates regular and power-up bolts and appends it to the list of bolts
        for the aliens to fire. The chances of a power-up bolt being created
        and fired is 1 in 8.

        Also determines whether a bolt has reached the end of the game window
        without collision. If it has, deletes the bolt.
        """
        value=False
        c=0
        while (value is not True):
            colum=random.randint(0,ALIENS_IN_ROW-1)
            for row in range(ALIEN_ROWS):
                if self._aliens[row][colum]!=None and c==0:
                    x=self._aliens[row][colum].getX()
                    y=self._aliens[row][colum].getY()
                    rand=random.randint(1,10)
                    if rand==10:
                        a='purple'
                    else:
                        a='yellow'
                    bolt=Bolt(x,y-ALIEN_HEIGHT/2,-1*BOLT_SPEED,a)
                    bolt.setPlayerBolt(False)
                    self._pew2.play(loop=False)
                    self._bolts.append(bolt)
                    c+=1
                    value=True
                    break
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].y+BOLT_HEIGHT/2 < 0:
                del self._bolts[i]
            else:
                i += 1


    def _collisionship(self, bolt):
        """
        Detects for a bolt collision with the ship.

        If a power-up bolt collides with the ship, the score increases by __.
        If a regular bolt collides with the ship, lives decrese by 1, the ship
        is destroyed and set to None.

        Parameter bolt: the bolt with which the collision is being checked
        Precondition: bolt is a Bolt object
        """
        color=[0.6274509803921569,0.12549019607843137,0.9411764705882353,1.0]
        if self._ship is not None:
            if self._ship._collidesship(bolt) and bolt._isPlayerBolt==False:
                if bolt.linecolor==color:
                    val=50
                    self._pop2.play(loop=False)
                    self.UpdateScore(val)

                else:
                    self._ship=None
                    self._blast2.play(loop=False)
                    self.UpdateLives()
                bolt.setDelete(True)


    def _moveShip(self,input):
        """
        Determines the current arrow key pressed and moves the ship accordingly.

        This method checks for a left or right arrow key press, and if there is
        one, moves the ship by SHIP_MOVEMENT pixels in the direction of the
        arrow pressed.  A key press is when a key is pressed EVERY TIME. We want
        the ship to continue to move as we hold down the keys.

        If the ship reaches the left or right edge of the game window, the ship
        is unable to move further in the respective direction.

        Parameter input: the user input used to control the ship and change state
        Precondition: input is an instance of GInput; it is inherited from
        GameApp
        """
        max=GAME_WIDTH-SHIP_WIDTH/2
        min=0+SHIP_WIDTH/2
        if self._ship is not None:
            if input.is_key_down('left'):
                if self._ship.x-SHIP_WIDTH/2>=min:
                    self._ship.x-= SHIP_MOVEMENT
                else:
                    self._ship.x=min
            if input.is_key_down('right'):
                if self._ship.x+SHIP_WIDTH/2<=max:
                    self._ship.x+= SHIP_MOVEMENT
                else:
                    self._ship.x=max


    def _moveAlienRight(self):
        """
        Moves each alien to the right by ALIEN_H_WALK.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    newx=alien.getX()+ALIEN_H_WALK
                    alien.frame = (alien.frame+1) % 2
                    alien.setX(newx)


    def _moveAlienLeft(self):
        """
        Moves each alien to the left by ALIEN_H_WALK.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    newx=alien.getX()-ALIEN_H_WALK
                    alien.frame = (alien.frame+1) % 2
                    alien.setX(newx)


    def _moveAlienDown(self):
        """
        Moves each alien dynamically down by ALIEN_V_WALK.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    newy=alien.getY()-ALIEN_V_WALK
                    if newy==DEFENSE_LINE+ALIEN_HEIGHT/2:
                        return STATE_COMPLETE
                    else:
                        alien.frame = (alien.frame+1) % 2
                        alien.setY(newy)
                        self._speed-=self._speed/300
        self._time=0


    def _trackRight(self):
        """
        Tracks whether the aliens have reached the right end of the game window.
        """
        for alien in range(ALIENS_IN_ROW-1,-1,-1):
            for row in range(ALIEN_ROWS):
                if self._aliens[row][alien] is not None:
                    return self._aliens[row][alien].getX()+ALIEN_WIDTH/2


    def _trackLeft(self):
        """
        Tracks whether the aliens have reached the left end of the game window.
        """
        for alien in range(ALIENS_IN_ROW):
            for row in range(ALIEN_ROWS):
                if self._aliens[row][alien] is not None:
                    return self._aliens[row][alien].getX()-ALIEN_WIDTH/2


    def _trackDown(self):
        """
        Tracks whether the aliens have reached the defense line.
        """
        for alien in range(ALIEN_ROWS):
            for colum in range(ALIENS_IN_ROW):
                if self._aliens[alien][colum] is not None:
                    return self._aliens[alien][colum].getY()-ALIEN_WIDTH/2


    def _movingRight(self):
        """
        Moves the aliens to the right as long as they have not reached the right
        edge of the game window.
        """
        self._music.play(loop=False)
        self._moveAlienRight()
        self._numMarch+=1
        if self._numMarch==self._alienbolts:
            self._alienFire()
            self._numMarch=0
            self._alienbolts=random.randint(1,BOLT_RATE)
        self._time=0


    def _movingLeft(self):
        """
        Moves the aliens to the left as long as they have not reached the left
        edge of the game window.
        """
        self._music.play(loop=False)
        self._moveAlienLeft()
        self._numMarch+=1
        if self._numMarch==self._alienbolts:
            self._alienFire()
            self._numMarch=0
            self._alienbolts=random.randint(1,BOLT_RATE)
        self._time=0


    def _reachedRight(self):
        """
        If the aliens have reached the right edge of the game window, moves the
        aliens down by ALIEN_V_WALK and left by ALIEN_H_WALK.
        """
        self._music.play(loop=False)
        self._moveAlienDown()
        self._numMarch+=1
        if self._numMarch==self._alienbolts:
            self._alienFire()
            self._numMarch=0
            self._alienbolts=random.randint(1,BOLT_RATE)
        self._music.play(loop=False)
        self._moveAlienLeft()
        self._numMarch+=1
        if self._numMarch==self._alienbolts:
            self._alienFire()
            self._numMarch=0
            self._alienbolts=random.randint(1,BOLT_RATE)
        self._time=0
        self.movingR=False


    def _reachedLeft(self):
        """
        If the aliens have reached the left edge of the game window, moves the
        aliens down by ALIEN_V_WALK and right by ALIEN_H_WALK.
        """
        self._music.play(loop=False)
        self._moveAlienDown()
        self._numMarch+=1
        if self._numMarch==self._alienbolts:
            self._alienFire()
            self._numMarch=0
            self._alienbolts=random.randint(1,BOLT_RATE)
        self._music.play(loop=False)
        self._moveAlienRight()
        self._numMarch+=1
        if self._numMarch==self._alienbolts:
            self._alienFire()
            self._numMarch=0
            self._alienbolts=random.randint(1,BOLT_RATE)
        self._time=0
        self.movingR=True


    def _moveAlien(self,dt):
        """
        Keeps moving the aliens across the game window.

        The aliens keep moving from right to left as long as they are above the
        defense line. The aliens speed up dynamically as they get closer to the
        defense line.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time+=dt
        if self._aliens is not None:
            if self._time>self._speed and \
            (self._trackRight()<GAME_WIDTH-ALIEN_H_SEP) and self.movingR:
                self._movingRight()
            elif self._time>self._speed and \
            (self._trackRight()>=GAME_WIDTH-ALIEN_H_SEP):
                self._reachedRight()
            elif self._time>self._speed and \
            (self._trackLeft()>ALIEN_H_SEP) and self.movingR==False:
                self._movingLeft()
            elif self._time>self._speed and (self._trackLeft()<=ALIEN_H_SEP):
                self._reachedLeft()
