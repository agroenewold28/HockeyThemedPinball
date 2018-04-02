import procgame.game
from procgame.game import AdvancedMode

class GunMode(procgame.game.AdvancedMode):
	""" 
	this class handles the `Cannon` in T2; monitors the 
	switches and enables the trigger to fire when safe
	"""
	def __init__(self, game):
		super(GunMode, self).__init__(game=game, priority=20, 
			mode_type=AdvancedMode.System)
		self.gunMoving = False
		self.clearToFire = False
		self.acceptTrigger = False
		self.wasHome = False

	def mode_started(self):
		self.clearToFire = False
		if(not self.game.switches.gunHome.is_active()):
			# gun is not Home at start
			self.start_gun_move()
		else:
			# at home
			self.wasHome = True
			pass
		if(self.game.switches.gunLoaded.is_active()):
			# gun is loaded at start
			self.start_gun_move()

	def sw_gunLoaded_active_for_200ms(self, sw):
		self.clearToFire = False
		self.acceptTrigger = True
		self.start_gun_move()
		return procgame.game.SwitchContinue

	def start_gun_move(self):
		self.game.coils.gunMotor.pulsed_patter(8,4,0)
		self.gunMoving = True

	def stop_gun_move(self):
		self.game.coils.gunMotor.disable() # turn off the motor
		self.gunMoving = False # indicate that the motor is off

	def sw_gunMark_active(self, sw):
		if(self.wasHome):
			self.clearToFire = True
		else:
			self.clearToFire = False
		self.wasHome = False

		if(self.game.switches.gunLoaded.is_active()):
			if(self.clearToFire == False):
				# last chance to auto-ditch ball!!
				self.fire_gun()
		return procgame.game.SwitchContinue

	def sw_gunHome_active_for_200ms(self, sw):
		self.wasHome = True
		if not self.game.switches.gunLoaded.is_active() :  # the ball is NOT in the gun
			self.stop_gun_move()
			if(self.game.switches.ballPopper.is_active()): # if there's a ball waiting, send it down
				self.game.coils.ballPopper.pulse()
		else: # the ball IS in the gun
			self.start_gun_move()

		return procgame.game.SwitchContinue

	def is_clear_to_feed(self):
		return (self.game.switches.gunLoaded.is_active() == False) and (self.game.switches.gunHome.is_active())

	def sw_ballPopper_active_for_200ms(self,sw):
		if(self.is_clear_to_feed()):
			self.game.coils.ballPopper.pulse()
		#else:
			# something else
		return procgame.game.SwitchContinue
		
	def mode_stopped(self): 
		pass
		
	def sw_gripTrigger_active(self, sw):
		#self.game.displayAward("gun sees trigger ctf=[" + str(self.gunClearToFire) + "]")
		if self.game.switches.gunLoaded.is_active():
			if self.acceptTrigger==True and self.clearToFire == True:
				self.fire_gun()
		return procgame.game.SwitchContinue

	def fire_gun(self):
		self.game.coils.gunKicker.pulse()
		self.gunClearToFire = False
	
