"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders
application. There is no need for any additional classes in this module.
If you need more classes, 99% of the time they belong in either the wave module
or the models module. If you are unsure about where a new class should go,
post a question on Piazza.

Authors: Mihikaa Goenka (mg897), Oishani Ganguly (og58), 
Date: December 4th, 2018
"""
from consts import *
from game2d import *
from wave import *
from random import randint
import os.path
import sys


# PRIMARY RULE: Invaders can only access attributes in wave.py via
# getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when
    the game started, paused, completed, etc. It keeps track of that in an
    attribute called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from
                consts.py [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
                STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and
                aliens [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for
    the method update.

    You may have more attributes if you wish (you might want an attribute to
    store any score across multiple waves). If you add new attributes, they need
    to be documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _lastkeys:  the number of keys pressed last frame [int >= 0]
    _last:      the number of clicks in the last frame [Point2 or None if mouse
                was not down last frame]
    _background:the background of the game window [GRectangle]
    _space:     the animating stars on the background [GRectangle]
    _scoretext: the text indicating the score [GLabel]
    _pause:     the text displaying the message when the game is manually paused
    _oops:      the text displaying the message when the game is paused when the
                ship has died once [GLabel]
    _win:       the text displaying the message when the game has been won
                [GLabel]
    _end:       the text displaying the message at the end of a game [GLabel]
                [GLabel]
    _mute:      the icon displaying the mute button
                [GImage]
    _livestext: the text indicating the lives [GLabel]
    _muted:     int value to check whether the sound is muted [1 or 0]
    _over:      sound played when the game is over and player has lost [Sound]
    _clap:      sound played when the game is over and the player has won [Sound]
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the game
        is running. You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state=STATE_INACTIVE
        self._lastkeys=self._muted=0
        self._last=self._wave=self._space=None
        self._background=GRectangle(x=GAME_WIDTH/2,y=GAME_HEIGHT/2,
        width=GAME_WIDTH,height=GAME_HEIGHT,fillcolor='black')
        self._scoretext=GLabel(text="SCORE: ", font_size=40,
        font_name='Arcade.ttf',x=GAME_WIDTH/10,y=GAME_HEIGHT-GAME_HEIGHT/16,
        fillcolor='black',linecolor='yellow')
        self._pause=GLabel(text="Game is Paused\n Press 'r' to Resume\n Press"+
        " 'q' to Quit Game", font_size=60,font_name='Arcade.ttf',x=GAME_WIDTH/2,
        y=GAME_HEIGHT/2,linecolor='white')
        self._oops=GLabel(text="OOPS!\n Press 'c' to continue\n Press 'q' to"+
        " Quit Game", font_size=60,font_name='Arcade.ttf',x=GAME_WIDTH/2,
        y=GAME_HEIGHT/2,linecolor='white')
        self._win=GLabel(text="YOU WIN!\n Press 'n' to Play Again\n Press 'q'"+
        " to Quit Game", font_size=60,font_name='Arcade.ttf',x=GAME_WIDTH/2,
        y=GAME_HEIGHT/2,linecolor='white')
        self._end=GLabel(text="GAME OVER\n You Lose :(\n Press 'n' to Play"+
        "Again\n Press 'q' to Quit Game", font_size=60,font_name='Arcade.ttf',
        x=GAME_WIDTH/2,y=GAME_HEIGHT/2,linecolor='white')
        self._mute=GImage(x=GAME_WIDTH-GAME_WIDTH/10+15,
        y=GAME_HEIGHT-GAME_HEIGHT/16-20,width=GAME_WIDTH/30,
        height=GAME_HEIGHT/30,source='mute.png')
        self._livestext= GLabel(text="LIVES: ", font_size=40,
        font_name='Arcade.ttf',x=GAME_WIDTH-GAME_WIDTH/8,y=GAME_HEIGHT-GAME_HEIGHT/16,
        fillcolor='black',linecolor='green')
        self._text=GLabel(text="Press 's' to Play\n Press 'p' to Pause\n Press"+
        " 'q' to Quit Game", font_size=60,font_name='Arcade.ttf',x=GAME_WIDTH/2,
        y=GAME_HEIGHT/2,linecolor='blue')
        self._gameOverSounds()


    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game. It also mutes the game completely till the end if a single click
        on the mute icon is detected

        STATE_INACTIVE: This is the state when the application first opens.  It
        is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in this
        state so long as the player never presses a key.  In addition, this is
        the state the application returns to when the game is over (all lives
        are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state that creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key. This
        state only lasts one animation frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move
        the ship and fire laser bolts.  All of this should be handled inside of
        class Wave (NOT in this class).  Hence the Wave class should have an
        update() method, just like the subcontroller example in lecture.

        STATE_MANUAL_PAUSED: This is a manually paused state. However, the
        game is still visible on the screen.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the
        game is still visible on the screen.

        STATE_COMPLETE: The wave is not over, and the game is lost.

        STATE_WIN: The wave is over, and the game is won.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state==STATE_INACTIVE:
            self._determineStateStart()
        if self._state==STATE_NEWWAVE:
            self._wave=Wave()
            self._state=STATE_ACTIVE
        if self._state==STATE_ACTIVE:
            self._wave.update(self.input,dt)
            self._determineStateManualPause()
            self._determineStatePause()
            self._determineMute()
            self._determineStateComplete()
        if self._state==STATE_MANUAL_PAUSED:
            self._determineMute()
            self._determineStateResume()
        if self._state==STATE_PAUSED:
            self._determineMute()
            self._nextLife()
        if self._state==STATE_COMPLETE or self._state==STATE_WIN:
            self._newWave()
        if self._muted==1:
            self._wave.getMusic().stop()
            self._wave.getPew1().stop()
            self._wave.getPew2().stop()
            self._wave.getBlast1().stop()
            self._wave.getBlast2().stop()


    def subdraw(self):
        """
        Draws the background, the animating stars in space, the score sign, the
        lives sign, the mute button, and the wave.
        """
        self._background.draw(self.view)
        a=['white', 'blue', 'green', 'red', 'yellow', 'magenta', 'cyan']
        for i in range(80):
            self._space=GRectangle(x=random.randint(0, GAME_WIDTH),
            y=random.randint(0, GAME_HEIGHT),width=1.5, height=1.5,
            fillcolor=a[random.randint(0,6)])
            self._space.draw(self.view)
        self._scoretext.draw(self.view)
        self._livestext.draw(self.view)
        self._mute.draw(self.view)
        self._wave.draw(self.view)


    def draw(self):
        """
        Draws the game objects, the images, the texts, and the labels to the
        view.
        """
        if self._state==STATE_INACTIVE:
            self._background.draw(self.view)
            self._text.draw(self.view)
        if self._state==STATE_ACTIVE:
            self.subdraw()
        if self._state==STATE_COMPLETE:
            self.subdraw()
            self._end.draw(self.view)
            self._highscore=GLabel(text="YOUR SCORE IS: "
            +str(self._wave.getScore())+"   HIGHSCORE IS: "+str(self.HighScore()),
            x=GAME_WIDTH/2, y=GAME_WIDTH/2-200,font_size=30,linecolor='magenta',
            font_name='Arcade.ttf')
            self._highscore.draw(self.view)
        if self._state==STATE_WIN:
            self.subdraw()
            self._win.draw(self.view)
            self._highscore=GLabel(text="YOUR SCORE IS: "
            +str(self._wave.getScore())+"   HIGHSCORE IS: "+str(self.HighScore()),
            x=GAME_WIDTH/2, y=GAME_WIDTH/2-200, font_size=30, linecolor='magenta',
             font_name='Arcade.ttf')
            self._highscore.draw(self.view)
        if self._state==STATE_MANUAL_PAUSED:
            self.subdraw()
            self._pause.draw(self.view)
        if self._state==STATE_PAUSED:
            self.subdraw()
            self._oops.draw(self.view)
        if self._state==STATE_CONTINUE:
            self._state=STATE_ACTIVE


    # HELPER METHODS FOR THE STATES GO HERE
    def _determineStateStart(self):
        """
        Determines the current state and assigns it to self._state.

        This method checks for a key press for 's' or 'q', and if there is one,
        changes the state to the next value. A key press is when a key is pressed
        for the FIRST TIME. The state does not change as we hold down the key.

        The game quits itself when 'q' is pressed and starts when 's' is pressed.
        """
        curr_keys = self.input.key_count
        change=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('s')
        change1=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('q')
        if change:
            self._state = STATE_NEWWAVE
        elif change1:
            sys.exit()
        self._lastkeys=curr_keys


    def _determineStateManualPause(self):
        """
        Determines the current state and assigns it to self._state

        This method checks for a key press for 'p' or 'q', and if there is one,
        changes the state to the next value. A key press is when a key is pressed for the
        FIRST TIME. The user must release the key and press a different one to
        change the state.

        The game quits itself when 'q' is pressed and pauses when 'p' is pressed.
        """
        curr_keys = self.input.key_count
        change=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('p')
        change1=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('q')
        if change:
            self._state = STATE_MANUAL_PAUSED
        elif change1:
            sys.exit()
        self._lastkeys=curr_keys


    def _determineStatePause(self):
        """
        Determines whether the ship has been killed or not. If it has, it moves
        into the next state and assigns new state to self._state.
        """
        if self._wave._shipExist():
            self._state = STATE_PAUSED


    def _determineStateResume(self):
        """
        Determines the current state and assigns it to self._state

        This method checks for a key press for 'r' or 'q', and if there is one,
        changes the state to the next value. A key press is when a key is pressed
        for the FIRST TIME. The user must release the key and press a different
        one to change the state.

        The game quits itself when 'q' is pressed and resumes from a manual pause
        when 'r' is pressed.
        """
        curr_keys = self.input.key_count
        change=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('r')
        change1=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('q')
        if change:
            self._state = STATE_ACTIVE
        elif change1:
            sys.exit()
        self._lastkeys=curr_keys


    def HighScore(self):
        """
        Updates and returns the highscore in a .txt file if the previous high
        score was beaten by the player.
        """
        hisc=open(os.path.join('invaders','high.txt'),"r")
        highscore=hisc.read()
        highnum=int(highscore)
        hisc.close()
        hisc=open(os.path.join('invaders','high.txt'),"w+")
        currentscore=int(self._wave.getScore())
        if currentscore>highnum:
            highnum=currentscore
        hisc.write(str(highnum))
        hisc.close()
        return highnum


    def _determineStateComplete(self):
        """
        Determines whether the player has won or lost the game and updates
        self._state accordingly.

        Plays music accordingly.
        """
        if self._wave.getNoAliens()==0:
            self._wave.getMusic().stop()
            self._clap.play(loop=False)
            self._state=STATE_WIN
        elif self._wave.getLives()==0 or self._wave._trackDown()<DEFENSE_LINE:
            self._wave.getMusic().stop()
            self._over.play(loop=False)
            self._state=STATE_COMPLETE


    def _nextLife(self):
        """
        Determines the current state and assigns it to self._state

        This method checks for a key press for 'c' or 'q' after the ship has
        died, and if there is one, changes the state to the next value after
        decresing the lives by 1. A key press is when a key is pressed for the
        FIRST TIME. The user must release the key and press a different one to
        change the state.

        The game quits itself when 'q' is pressed and continues from the paused
        state when 'c' is pressed.
        """
        curr_keys = self.input.key_count
        change=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('c')
        change1=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('q')
        if change:
            self._state = STATE_CONTINUE
            self._wave.setShip()
        elif change1:
            sys.exit()
        self._lastkeys=curr_keys


    def _newWave(self):
        """
        Determines the current state and assigns it to self._state

        This method checks for a key press for 'n' or 'q', and if there is one,
        changes the state to the next value. A key press is when a key is pressed
        for the FIRST TIME. The user must release the key and press a different
        one to change the state.

        The game quits itself when 'q' is pressed and a new game starts when
        'n' is pressed.
        """
        curr_keys = self.input.key_count
        change=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('n')
        change1=curr_keys>0 and self._lastkeys==0 and self.input.is_key_down('q')
        if change:
            self._state = STATE_NEWWAVE
        elif change1:
            sys.exit()
        self._lastkeys=curr_keys


    def _determineMute(self):
        """
        Checks whether there was a click on the mute button. If there was, mutes
        the game sound till the end of the current gameself.
        """
        touch = self.input.touch
        if self._last is None and touch is not None and self._mute.contains((touch.x,touch.y)):
            self._muted=1
        self._last = touch

    def _gameOverSounds(self):
        """
        Initializes the sounds when the player loses or wins
        """
        self._over=Sound('over.wav')
        self._clap=Sound('clap.wav')
