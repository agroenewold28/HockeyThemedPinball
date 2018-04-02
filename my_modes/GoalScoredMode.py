import procgame.game
from procgame.game import AdvancedMode
import logging
import random

class GoalScoredMode(procgame.game.AdvancedMode):
    """
    Example Mode
    """
    def __init__(self, game):
        """
        stuff in __init__ gets done EXACTLY once.
        happens when the "parent" Game creates this mode

        You _need_ to call the super class' init method:
        """
        super(GoalScoredMode, self).__init__(game=game, priority=8, mode_type=AdvancedMode.Game) # 2 is lower than BGM
        # notice this mode has a mode_type of 'AdvancedMode.Game'
        # this means the mode is auto-added when a game starts and
        # removed when the last player finishes their game

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('HockeyMode')       
        self.target_tracker = 0
        self.targets_hit = 0        
        pass


    def mode_started(self):
        self.logger.debug("Mode has started")
    
    def mode_stopped(self): 
        self.logger.debug("Mode has ended")

    def evt_player_added(self, new_player):
    	new_player.setState("gunPresent", False)
        new_player.setState("t1", False)
        new_player.setState("t2", False)
        new_player.setState("t3", False)
        new_player.setState("t4", False)
        new_player.setState("t5", False)

    def sw_gunLoaded_active(self, sw):
        freeTarget = False
        self.game.setPlayerState("gunPresent", True)
        while(freeTarget == False):
            r = random.randint(1, 6)
            self.target_tracker = r
            if(r == 1):
                if(self.game.getPlayerState("t1") == False):
                    self.game.lamps.target1.schedule(0xf0f0f0f0)
                    freeTarget = True
                    self.game.setPlayerState("t1", True)
            elif(r == 2):
                if(self.game.getPlayerState("t2") == False):
                    self.game.lamps.target2.schedule(0xf0f0f0f0)
                    freeTarget = True
                    self.game.setPlayerState("t2", True)
            elif(r == 3):
                if(self.game.getPlayerState("t3") == False):
                    self.game.lamps.target3.schedule(0xf0f0f0f0)
                    freeTarget = True                   
                    self.game.setPlayerState("t3", True)
            elif(r == 4):
                if(self.game.getPlayerState("t4") == False):
                    self.game.lamps.target4.schedule(0xf0f0f0f0)
                    freeTarget = True
                    self.game.setPlayerState("t4", True)
            else:
                 if(self.game.getPlayerState("t5") == False):
                    self.game.lamps.target5.schedule(0xf0f0f0f0)
                    freeTarget = True
                    self.game.setPlayerState("t5", True)               

    def sw_target1_active(self, sw):
        if(self.target_tracker == 1 and self.game.getPlayerState("gunPresent") == True):
            self.targets_hit = self.targets_hit + 1
            if(self.targets_hit == 5):
                self.targetReset()
                self.targets_hit = 0
            self.game.lamps.target1.enable()
            self.goal()
        elif(self.game.getPlayerState("gunPresent") == True):
            self.disableBlinker()
        else:
            self.game.score(30)
            self.game.sound.play('hit_post')
        self.game.setPlayerState("gunPresent", False)

    def sw_target2_active(self, sw):
        if(self.target_tracker == 2 and self.game.getPlayerState("gunPresent") == True):
            self.targets_hit = self.targets_hit + 1            
            if(self.targets_hit == 5):
                self.targetReset()
                self.targets_hit = 0
            self.game.lamps.target2.enable()
            self.goal()
        elif(self.game.getPlayerState("gunPresent") == True):
            self.disableBlinker()
        else:
            self.game.score(30)
            self.game.sound.play('hit_post')
        self.game.setPlayerState("gunPresent", False)

    def sw_target3_active(self, sw):
        if(self.target_tracker == 3 and self.game.getPlayerState("gunPresent") == True):
            self.targets_hit = self.targets_hit + 1            
            if(self.targets_hit == 5):
                self.targetReset()
                self.targets_hit = 0
            self.game.lamps.target3.enable()
            self.goal()
        elif(self.game.getPlayerState("gunPresent") == True):
            self.disableBlinker()            
        else:
            self.game.score(30)
            self.game.sound.play('hit_post')
        self.game.setPlayerState("gunPresent", False)

    def sw_target4_active(self, sw):
        if(self.target_tracker == 4 and self.game.getPlayerState("gunPresent") == True):
            self.targets_hit = self.targets_hit + 1            
            if(self.targets_hit == 5):
                self.targetReset()
                self.targets_hit = 0
            self.game.lamps.target4.enable()
            self.goal()
        elif(self.game.getPlayerState("gunPresent") == True):
            self.disableBlinker()            
        else:
            self.game.score(30)
            self.game.sound.play('hit_post')
        self.game.setPlayerState("gunPresent", False)

    def sw_target5_active(self, sw):
        if(self.target_tracker == 5 and self.game.getPlayerState("gunPresent") == True):
            self.targets_hit = self.targets_hit + 1            
            if(self.targets_hit == 5):
                self.targetReset()
                self.targets_hit = 0
            self.game.lamps.target5.enable()
            self.goal()
        elif(self.game.getPlayerState("gunPresent") == True):
            self.disableBlinker()            
        else:
            self.game.score(30)
            self.game.sound.play('hit_post')      
        self.game.setPlayerState("gunPresent", False)

    def disableBlinker(self):
        if(self.target_tracker == 1):
            self.game.lamps.target1.disable()
        elif(self.target_tracker == 2):
            self.game.lamps.target2.disable()
        elif(self.target_tracker == 3):
            self.game.lamps.target3.disable()
        elif(self.target_tracker == 4):
            self.game.lamps.target4.disable()
        else:
            self.game.lamps.target5.disable()

    def goal(self):
        self.game.displayText("Score!", 'kane')
        self.game.score(1000)
        self.game.sound.play('goal_horn')

    def targetReset(self):
        self.game.lamps.target1.disable()
        self.game.lamps.target2.disable()
        self.game.lamps.target3.disable()
        self.game.lamps.target4.disable()
        self.game.lamps.target5.disable()       
        self.frontLampShow()
        self.midLampShow()
        self.highLampShow()
        self.game.setPlayerState("t1", False)
        self.game.setPlayerState("t2", False)
        self.game.setPlayerState("t3", False)
        self.game.setPlayerState("t4", False)
        self.game.setPlayerState("t5", False)
        self.game.displayText("That's a bonus!")
        self.game.score(10000)

   	def frontLampShow(self):
   		self.game.lamps.mult2x.schedule(0xf0f0f0f0)
        self.game.lamps.holdBonus.schedule(0xf0f0f0f0)
        self.game.lamps.mult8x.schedule(0xf0f0f0f0)
        self.game.lamps.mult4x.schedule(0x0f0f0f0f)
        self.game.lamps.mult6x.schedule(0x0f0f0f0f)

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

    def highLampShow(self):
        self.game.lamps.rampL.schedule(0x0000000f)
        self.game.lamps.extraBall.schedule(0x000000f0)
        self.game.lamps.dropTarget.schedule(0x00000f00)
        self.game.lamps.database2.schedule(0x0000f000)
        self.game.lamps.lockTop.schedule(0x000f0000)
        self.game.lamps.laneL.schedule(0x00f00000)
        self.game.lamps.laneC.schedule(0x0f000000)
        self.game.lamps.laneR.schedule(0xf0000000)


