import procgame.game
from procgame.game import AdvancedMode
import logging
import random

class HockeyMode(procgame.game.AdvancedMode):
    """
    Example Mode
    """
    def __init__(self, game):
        """
        stuff in __init__ gets done EXACTLY once.
        happens when the "parent" Game creates this mode

        You _need_ to call the super class' init method:
        """
        super(HockeyMode, self).__init__(game=game, priority=6, mode_type=AdvancedMode.Game) # 2 is lower than BGM
        # notice this mode has a mode_type of 'AdvancedMode.Game'
        # this means the mode is auto-added when a game starts and
        # removed when the last player finishes their game

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        
        self.logger = logging.getLogger('HockeyMode')
        self.jetCount = 0
        self.power_play_count = 0
        pass

    def mode_started(self):
        self.logger.debug("Mode has started")
    
    def mode_stopped(self): 
        self.logger.debug("Mode has ended")

    def evt_game_starting(self):
        self.game.sound.play('hockey_song')
        self.game.displayText("Your off!", 'puck_drop')
        
    def evt_player_added(self, new_player):
        new_player.setState("laneR", False)
        new_player.setState("laneC", False)
        new_player.setState("laneL", False)

    def evt_ball_starting(self):
        self.jetCount = 0

    def sw_laneL_active(self, sw):
        if(self.game.getPlayerState("laneL") == False):
            self.game.lamps.laneL.enable()
            self.game.sound.play('hockey_stick')
            self.game.score(80)
            self.game.setPlayerState("laneL", True)
            self.lanes()
        else:
            self.game.score(20)

    def sw_laneC_active(self, sw):
        if(self.game.getPlayerState("laneC") == False):
            self.game.lamps.laneC.enable()
            self.game.sound.play('hockey_stick')
            self.game.score(80)
            self.game.setPlayerState("laneC", True)
            self.lanes()
        else:
            self.game.score(20)

    def sw_laneR_active(self, sw):
        if(self.game.getPlayerState("laneR") == False):
            self.game.lamps.laneR.enable()
            self.game.sound.play('hockey_stick')
            self.game.score(80)
            self.game.setPlayerState("laneR", True)
            self.lanes()
        else:
            self.game.score(20)

    def sw_ballPopper_active(self, sw):
        self.game.displayText("Your on a breakaway!", 'rink_background')
        self.game.score(100);
        self.game.sound.play('crowd_noise')
        self.game.lamps.database3.schedule(0x0000008f)
        self.game.lamps.loadGun.schedule(0x0000f80)
        self.game.lamps.extraBall.schedule(0x0008f000)
        self.game.lamps.dropTarget.schedule(0xff000000)
        self.game.lamps.loadForJackpot.schedule(0x00f80000)
    
    def sw_rampLeftMade_active(self, sw):
        self.rampMade()
        self.game.lamps.rampL.pulse()
        
    def sw_rampRightMade_active(self, sw):
        self.rampMade()
        self.game.lamps.rampRight.schedule(0x000000ff)
        self.game.lamps.chaseValue.schedule(0x00f0f00)
        self.game.lamps.hurryUp.schedule(0xff000000)
        
    def sw_jetL_active(self, sw):
        self.jet()
        
    def sw_jetR_active(self, sw):
        self.jet()
    
    def sw_jetB_active(self, sw):
        self.jet()
        
    def sw_dropTarget_active(self, sw):
        self.rampDropTarget()
        
    def sw_rampLeftEnter_active(self, sw):
        self.rampDropTarget()  
    
    def sw_rampRightEnter_active(self, sw):
        self.rampDropTarget() 
        
    def sw_outlaneL_active(self, sw):
        self.outlane()               
        
    def sw_outlaneR_active(self, sw):
        self.outlane()    
        
    def sw_slingR_active(self, sw):
        self.sling()
        
    def sw_slingL_active(self, sw):
        self.sling()  
        
    def sw_escapeH_active(self, sw):
        self.escape()
        
    def sw_escapeL_active(self, sw):
        self.escape()
        
    def sw_inlaneR_active(self, sw):
        self.inlane() 
        self.frontLampShow()
        self.game.lamps.database3.disable()
        self.game.lamps.loadGun.disable()
        self.game.lamps.extraBall.disable()
        self.game.lamps.dropTarget.disable() 
        self.game.lamps.rampRight.disable()
        self.game.lamps.chaseValue.disable()
        self.game.lamps.hurryUp.disable()
        self.game.lamps.loadForJackpot.disable()
        
    def sw_inlaneL_active(self, sw):
        self.inlane()
        self.frontLampShow()
        self.game.lamps.database3.disable()
        self.game.lamps.loadGun.disable()
        self.game.lamps.extraBall.disable()
        self.game.lamps.dropTarget.disable() 
        self.game.lamps.rampRight.disable()
        self.game.lamps.chaseValue.disable()
        self.game.lamps.hurryUp.disable()
        self.game.lamps.loadForJackpot.disable()
        
    def sw_chaseLoopLow_active(self, sw):
        self.chaseLoop()      
              
    def sw_chaseLoopHigh_active(self, sw):
        self.chaseLoop()   
        
    def sw_lockLeft_active(self, sw):
        self.locks()
        
    def sw_lockTop_active(self, sw):
        self.locks()

    def sw_flipperLwR_active(self, sw):
        self.flippers()

    def sw_flipperLwL_active(self, sw):
        self.flippers()

    def sw_gripTrigger_active(self, sw):
        self.frontLampShow()
        if self.game.switches.shooter.is_active():
            self.game.coils.plunger.pulse()
        return procgame.game.SwitchStop

    def sw_lockLeft_active_for_200ms(self, sw):
        self.game.coils.lockLeft.pulse()
        return procgame.game.SwitchStop

    def sw_lockTop_active_for_200ms(self, sw):
        self.game.coils.lockTop.pulse()
        return procgame.game.SwitchStop

    def lanes(self):
        self.power_play_count = self.power_play_count + 1
        if(self.power_play_count == 3):
            self.powerPlay()
            self.game.score(1500)
            self.power_play_count = 0
            self.game.setPlayerState("laneR", False)
            self.game.setPlayerState("laneC", False)
            self.game.setPlayerState("laneL", False)

    def powerPlay(self):
        self.game.displayText("Power Play!", 'kane')
        self.game.lamps.laneR.disable()
        self.game.lamps.laneC.disable()
        self.game.lamps.laneL.disable()
        self.highLampShow()
        self.game.modes.add(self.game.power_play_mode)
        self.delay(name="powerPlayModeDuration", delay=20.0, handler=self.removePowerPlayMode)

    def removePowerPlayMode(self):
        self.game.modes.remove(self.game.power_play_mode)

    def rampMade(self):
        self.game.displayText("Nice Assist!", 'hockeyAction')
        self.game.score(130)
        self.game.sound.play('hockey_stick')
        self.disableMidLampShow()
        
    def jet(self):
        self.game.sound.play('punch')
        self.game.score(70)        
        self.game.lamps.mouth.schedule(0xf0f0f0f0)
        self.game.lamps.eyesLower.schedule(0x0f0f0f0f)
        self.jetCount = self.jetCount + 1
        if(self.jetCount == 5):
            self.knockout()
            self.jetCount = 0
        
    def rampDropTarget(self):
        self.game.score(25)    
        
    def chaseLoop(self): 
        self.game.displayText("Turnover!", 'hockeyAction')
        self.game.score(25)
    
    def outlane(self):
        self.game.score(-25)
        self.game.sound.play('hit_post') 
        
    def sling(self):
        self.game.score(25)
        self.game.sound.play('hit')
        self.game.lamps.mouth.disable()
        self.game.lamps.eyesLower.disable()
        self.disableFrontLampShow()
        
    def escape(self):
        self.game.score(25)
        self.game.sound.play('hockey_stick') 
    
    def inlane(self):
        self.game.score(10)
        self.game.displayText("Here comes a shot!", 'hockey_shot') 
        self.game.sound.play('shot') 
        self.game.lamps.mouth.disable()
        self.game.lamps.eyesLower.disable()        
        self.disableMidLampShow()
        
    def locks(self):
        self.game.score(-50)
        self.game.sound.play('penalty_whistle')
        self.game.displayText("You got a penalty!", 'ref')

    def flippers(self):
        self.game.displayText('Save!', 'save')
        self.game.lamps.rampRight.disable()
        self.game.lamps.chaseValue.disable()
        self.game.lamps.hurryUp.disable()
        self.disableHighLampShow()         
            
    def knockout(self):
        self.game.score(500)
        self.game.displayText("Knockout!", 'hockey_fight')
        self.game.sound.play('fighting_bell')
        self.midLampShow()

    def frontLampShow(self):
        self.game.lamps.mult2x.schedule(0xf0f0f0f0)
        self.game.lamps.holdBonus.schedule(0xf0f0f0f0)
        self.game.lamps.mult8x.schedule(0xf0f0f0f0)
        self.game.lamps.mult4x.schedule(0x0f0f0f0f)
        self.game.lamps.mult6x.schedule(0x0f0f0f0f)

    def disableFrontLampShow(self):
        self.game.lamps.mult2x.disable()
        self.game.lamps.holdBonus.disable()
        self.game.lamps.mult8x.disable()
        self.game.lamps.mult4x.disable()
        self.game.lamps.mult6x.disable()

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

    def disableMidLampShow(self):
        self.game.lamps.lockTop.disable()
        self.game.lamps.database2.disable()
        self.game.lamps.million10.disable()
        self.game.lamps.extraBall44.disable()
        self.game.lamps.multiball.disable()
        self.game.lamps.lightHurryUp.disable()
        self.game.lamps.holdBonus47.disable()
        self.game.lamps.securityPass.disable()
        self.game.lamps.twofiftyK.disable()
        self.game.lamps.fivehunK.disable()
        self.game.lamps.sevenfiftyK.disable()
        self.game.lamps.oneMil.disable()
        self.game.lamps.threeMil.disable()
        self.game.lamps.fiveMil.disable()
        self.game.lamps.hurryUp.disable()
        self.game.lamps.chaseValue.disable()

    def highLampShow(self):
        self.game.lamps.rampL.schedule(0x0000000f)
        self.game.lamps.extraBall.schedule(0x000000f0)
        self.game.lamps.dropTarget.schedule(0x00000f00)
        self.game.lamps.database2.schedule(0x0000f000)
        self.game.lamps.lockTop.schedule(0x000f0000)
        self.game.lamps.laneL.schedule(0x00f00000)
        self.game.lamps.laneC.schedule(0x0f000000)
        self.game.lamps.laneR.schedule(0xf0000000)

    def disableHighLampShow(self):
        self.game.lamps.rampL.disable()
        self.game.lamps.extraBall.disable()
        self.game.lamps.dropTarget.disable()
        self.game.lamps.database2.disable()
        self.game.lamps.lockTop.disable()
        self.game.lamps.laneL.disable()
        self.game.lamps.laneC.disable()
        self.game.lamps.laneR.disable()


