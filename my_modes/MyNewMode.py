import procgame.game
from procgame.game import AdvancedMode
import logging

class MyNewMode(procgame.game.AdvancedMode):

	def __init__(self, game):

		super(MyNewMode, self).__init__(game = game, priority = 1, mode_type = AdvancedMode.Game)
		self.logger = logging.getLogger("MyNewMode")
		pass

	def evt_player_added(self, new_player):
		new_player.setState("Player", False)

	def mode_started(self):
        self.logger.debug("My mode started")
    
    def mode_stopped(self): 
        self.logger.debug("My mode ended")

    def sw_tilt_active(self, sw):
    	self.game.lamps.lockLeft.enable()
    	self.game.displayText("Looks like a tilt!")
    	if(self.game.getPlayerState("Player") == False):
    		self.game.sound.play('Message-B_Decline')
    		self.game.score(100)
    	else:
    		self.game.sound.play('ALERT_Appear')

    def sw_target3_active(self, sw):
    	self.game.lamps.chaseLoopLow.enable()
    	self.game.sound.play('click')

    def sw_dropTarget_active(self, sw):
    	self.game.displayText("You gained 100 points!")
    	self.game.score(100)
    	if(self.game.getPlayerScore() > 200):
    		self.game.lamps.chaseLoopLow.disable()
    		self.game.lamps.ballPopper.schedule(0xff0000)
    		self.game.lamps.shooter.schedule(0x00fa00)
    		self.game.lamps.laneL.schedule(0x0005ff)

    def sw_lockTop_active(self, sw): 
    	self.game.sound.play('accomplish_tune')
    	self.game.score(500)
    	self.game.lamps.lockTop.pulse()
    	self.game.lamps.shooter.disable()

    def sw_startButton_active(self, sw):
    	mode_started(self)
    	self.game.lamps.slamTilt.enable()

   	def evt_ball_starting(self):
        if(self.game.getPlayerState("Player")==True):
            self.game.lamps.target1.enable()
        else:
            self.game.lamps.target1.disable()

    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.game.lamps.target1.disable()
 

