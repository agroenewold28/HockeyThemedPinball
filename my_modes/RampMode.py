import procgame.game
from procgame.game import AdvancedMode
import logging

class RampMode(procgame.game.AdvancedMode):
    """
    Example of T2 ramp criss-cross functionality
    gives 1M points for hitting a ramp within 2sec
    of hitting the opposite ramp.

    TODO: Sound effects, other visual feedback??

        Also, completing the ladder should reset the
            progress, and start Payback Mode for
            20 seconds
    """
    def __init__(self, game):
        """
        stuff in __init__ gets done EXACTLY once.
        happens when the "parent" Game creates this mode

        You _need_ to call the super class' init method:
        """
        super(RampMode, self).__init__(game=game, priority=20, mode_type=AdvancedMode.Game)

        # useful to set-up a custom logger so it's easier to track debugging messages for this mode
        self.logger = logging.getLogger('RampMode')

        self.left_ramp_ready = False
        self.right_ramp_ready = False
        pass

    def evt_player_added(self, player):
        player.setState('left_ramp_progress',0)
        player.setState('right_ramp_progress',0)

    def evt_ball_starting(self):
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()
        self.sync_lamps_to_progress()

    def disable_progress_lamps(self):
        # left side is: 65 .. 61
        self.game.lamps.checkpointL.disable()
        self.game.lamps.passcodeL.disable()
        self.game.lamps.silentAlarmL.disable()
        self.game.lamps.vaultKeyL.disable()
        self.game.lamps.cpuLitL.disable()

        # right side is: 75 .. 7
        self.game.lamps.checkpointR.disable()
        self.game.lamps.passcodeR.disable()
        self.game.lamps.silentAlarmR.disable()
        self.game.lamps.vaultKeyR.disable()
        self.game.lamps.cpuLitR.disable()

    def sync_lamps_to_progress(self):
        self.disable_progress_lamps()

        # left side is: 65 .. 61
        if(self.game.getPlayerState('left_ramp_progress')>0):
            self.game.lamps.checkpointL.enable()
            if(self.game.getPlayerState('left_ramp_progress')>1):
                self.game.lamps.passcodeL.enable()
                if(self.game.getPlayerState('left_ramp_progress')>2):
                    self.game.lamps.silentAlarmL.enable()
                    if(self.game.getPlayerState('left_ramp_progress')>3):
                        self.game.lamps.vaultKeyL.enable()
                        if(self.game.getPlayerState('left_ramp_progress')>4):
                            self.game.lamps.cpuLitL.enable()

        # right side is: 75 .. 71
        if(self.game.getPlayerState('right_ramp_progress')>0):
            self.game.lamps.checkpointR.enable()
            if(self.game.getPlayerState('right_ramp_progress')>1):
                self.game.lamps.passcodeR.enable()
                if(self.game.getPlayerState('right_ramp_progress')>2):
                    self.game.lamps.silentAlarmR.enable()
                    if(self.game.getPlayerState('right_ramp_progress')>3):
                        self.game.lamps.vaultKeyR.enable()
                        if(self.game.getPlayerState('right_ramp_progress')>4):
                            self.game.lamps.cpuLitR.enable()


    def evt_ball_ending(self, (shoot_again, last_ball)):
        self.cancel_delayed(name="disabler")
        self.disable_ramp_readiness()
        self.disable_progress_lamps()

    def sw_rampLeftMade_active(self, sw):
        if(self.left_ramp_ready):
            self.game.adjPlayerState('left_ramp_progress',1)
            self.sync_lamps_to_progress()
            self.game.score(1000000)
            self.left_ramp_ready = False
            self.cancel_delayed(name="disabler")
            self.delay(name="disabler", delay=2.0, handler=self.disable_ramp_readiness)

        self.game.lamps.rampRight.schedule(0x0f0f0f0f)
        self.game.lamps.rampL.disable()
        self.right_ramp_ready = True
        return procgame.game.SwitchStop

    def sw_rampRightMade_active(self, sw):
        if(self.right_ramp_ready):
            self.game.adjPlayerState('right_ramp_progress',1)
            self.sync_lamps_to_progress()
            self.game.score(1000000)
            self.right_ramp_ready = False
            self.cancel_delayed(name="disabler")
            self.delay(name="disabler", delay=2.0, handler=self.disable_ramp_readiness)

        self.game.lamps.rampL.schedule(0x0f0f0f0f)
        self.game.lamps.rampRight.disable()
        self.left_ramp_ready = True
        return procgame.game.SwitchStop

    def disable_ramp_readiness(self):
        self.left_ramp_ready = False
        self.right_ramp_ready = False
        self.game.lamps.rampL.disable()
        self.game.lamps.rampRight.disable()
