from tracker import Tracker
from controller import Controller
from matlab_port import MatlabPort
from navigator import Navigator


class ControlledVehicle:
    def __init__(self, time_step, startX, startY, port):
        self.startX = startX
        self.startY = startY
        self.pivot_threshold = 30
        self.forward_speed = 120
        self.navigator = Navigator()
        self.controller = Controller(time_step, 120, 30, port)
        
    def step(self, my_pos, other_pos, current_heading):
        if (my_pos and other_pos):
            target_heading = self.navigator.get_target_heading(my_pos, other_pos)
            
            controller.update_motors(current_heading, target_heading)

        else:
            # no new data (fiducial is not in view)
            controller.coast()
    def step_rl(self, current_heading, target_heading):
        controller.update_motors(current_heading, target_heading)
            
    def reset(self):
        tracker = Tracker()
        tracker.update()
        my_pos = tracker.get_my_pos()
        target_pos = [startX, startY]
        while(not self.navigator.has_arrived())
