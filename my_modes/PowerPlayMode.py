import procgame.game
from procgame.game import AdvancedMode
import logging

class PowerPlayMode(procgame.game.AdvancedMode):
    """
    Example Mode
    """
    def __init__(self, game):
        """
        stuff in __init__ gets done EXACTLY once.
        happens when the "parent" Game creates this mode

        You _need_ to call the super class' init method:
        """
        super(PowerPlayMode, self).__init__(game=game, priority=10, mode_type=AdvancedMode.Manual) # 2 is lower than BGM
        # notice this mode has a mode_type of 'AdvancedMode.Game'
        # this means the mode is auto-added when a game starts and
        # removed when the last player finishes their game

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('PowerPlayMode')               
        pass

    def mode_started(self):
        self.logger.debug("Mode has started")
    
    def mode_stopped(self): 
        self.logger.debug("Mode has ended")

   	# def powerPlayGoal(self):

    def flippers(self):
   		self.game.sound.play('shot')
   		self.game.score(100)

    def jetAndSling(self):
    	self.game.sound.play('hockey_stick')
    	self.game.score(150)   	
    
    def sw_rampLeftMade_active(self, sw):
    	self.game.displayText("Power Play Goal!", 'kane')
        self.game.score(10000)
        self.game.sound.play('goal_horn')
        self.game.lamps.rampL.pulse()
        
    def sw_rampRightMade_active(self, sw):
        self.game.displayText("Power Play Goal!", 'kane')
        self.game.score(10000)
        self.game.sound.play('goal_horn')
        self.game.lamps.rampRight.schedule(0x000000ff)
        self.game.lamps.chaseValue.schedule(0x00f0f00)
        self.game.lamps.hurryUp.schedule(0xff000000)

    def sw_slingR_active(self, sw):
        self.jetAndSling()
        
    def sw_slingL_active(self, sw):
        self.jetAndSling()      
        
    def sw_jetL_active(self, sw):
        self.jetAndSling()
        
    def sw_jetR_active(self, sw):
        self.jetAndSling()
    
    def sw_jetB_active(self, sw):
        self.jetAndSling()

    def sw_flipperLwR_active(self, sw):
        self.flippers()

    def sw_flipperLwL_active(self, sw):
        self.flippers()







