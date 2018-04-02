import procgame.game
from procgame.game import AdvancedMode
import logging

class HatTrickMode(procgame.game.AdvancedMode):
    """
    Example Mode
    """
    def __init__(self, game):
        """
        stuff in __init__ gets done EXACTLY once.
        happens when the "parent" Game creates this mode

        You _need_ to call the super class' init method:
        """
        super(HatTrickMode, self).__init__(game=game, priority=7, mode_type=AdvancedMode.Game) # 2 is lower than BGM
        # notice this mode has a mode_type of 'AdvancedMode.Game'
        # this means the mode is auto-added when a game starts and
        # removed when the last player finishes their game

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('HatTrickMode')        
        self.h1Count = 0
        self.h2Count = 0
        self.standupMidL = False
        self.standupMidC = False
        self.standupMidR = False
        self.standupRightT = False
        self.standupRightM = False
        self.standupRightB = False        
        pass

    def mode_started(self):
		self.logger.debug("Mode has started")

    def mode_stopped(self): 
        self.logger.debug("Mode has ended")

    def sw_standupMidL_active(self, sw):
        if(self.standupMidL == False):
            self.game.lamps.standupMidL.enable()
            self.game.score(50)
            self.standupMidL = True          
            self.standupSwitches()
        else:
            self.game.score(10)

    def sw_standupMidC_active(self, sw):
    	if(self.standupMidC == False):
    		self.game.lamps.standupMidC.enable()
    		self.game.score(50)
    		self.standupMidC = True
    		self.standupSwitches()
    	else:
    		self.game.score(10) 

    def sw_standupMidR_active(self, sw):
        if(self.standupMidR == False):
            self.game.lamps.standupMidR.enable()
            self.game.score(50)
            self.standupMidR = True            
            self.standupSwitches()
        else:
            self.game.score(10)

    def sw_standupRightT_active(self, sw):
        if(self.standupRightT == False):
            self.game.lamps.standupRightT.enable()
            self.game.score(50)
            self.standupRightT = True
            self.standupRightSwitches()
        else:
            self.game.score(10)

    def sw_standupRightM_active(self, sw):
        if(self.standupRightM == False):
            self.game.lamps.standupRightM.enable()
            self.game.score(50)
            self.standupRightM = True            
            self.standupRightSwitches()
        else:
            self.game.score(10)

    def sw_standupRightB_active(self, sw):
        if(self.standupRightB == False):
            self.game.lamps.standupRightB.enable()
            self.game.score(50)
            self.standupRightB = True            
            self.standupRightSwitches()
        else:
            self.game.score(10)

    def standupSwitches(self):
        self.h1Count = self.h1Count + 1
        if(self.h1Count == 3):
            self.hatTrick(True)
            self.h1Count = 0
        else:
            self.game.score(50)

    def standupRightSwitches(self):
        self.h2Count = self.h2Count + 1
        if(self.h2Count == 3):
            self.hatTrick(False)
            self.h2Count = 0
        else:
            self.game.score(50)

    def hatTrick(self, topSwitches):
        self.game.score(800)
        self.game.sound.play('goal_horn')
        self.game.displayText("Hat Trick!", 'hat')
        self.midLampShow()
        if(topSwitches == True):        
            self.standupMidL = False
            self.standupMidC = False
            self.standupMidR = False 
            self.game.lamps.standupMidL.disable()
            self.game.lamps.standupMidC.disable()
            self.game.lamps.standupMidR.disable()
        else:
            self.standupRightT = False
            self.standupRightM = False
            self.standupRightB = False
            self.game.lamps.standupRightB.disable()
            self.game.lamps.standupRightM.disable()
            self.game.lamps.standupRightT.disable() 

    def midLampShow(self):
    	self.game.lamps.lockTop.schedule(0x0000000f)
        self.game.lamps.database2.schedule(0x000000f0)
        self.game.lamps.million10.schedule(0x00000f00)
        self.game.lamps.extraBall44.schedule(0x0000f000)
        self.game.lamps.multiball.schedule(0x000f0000)
        self.game.lamps.lightHurryUp.schedule(0x00f00000)
        self.game.lamps.holdBonus47.schedule(0x0f000000)
        self.game.lamps.securityPass.schedule(0xf0000000)
        self.game.lamps.twofiftyK.schedule(0x0000000f)
        self.game.lamps.fivehunK.schedule(0x000000f0)
        self.game.lamps.sevenfiftyK.schedule(0x00000f00)
        self.game.lamps.oneMil.schedule(0x0000f000)
        self.game.lamps.threeMil.schedule(0x000f0000)
        self.game.lamps.fiveMil.schedule(0x00f00000)
        self.game.lamps.hurryUp.schedule(0x0f000000)
        self.game.lamps.chaseValue.schedule(0xf0000000)
        