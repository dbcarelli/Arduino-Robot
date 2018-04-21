import time
from tracker import Tracker
import numpy as np

class env:
    def __init__(self, time_step):
        self.time_step = time_step
        self.tracker = Tracker()
        self.tracker.update()
        self.chaser = ControlledVehicle(self.time_step, 0, 0, "COM9")
        self.runner = ControlledVehicle(self.time_step, 1, 1, "COM8") # IDK which is the actual serial port
        self.state = np.array([0, 0, 1, 1, self.tracker.get_target_heading(), self.tracker.get_my_heading()])
        self.state_length = self.state.shape[0]
        self.action_count = 360
        
    def reset(self):
        self.chaser.reset()
        self.runner.reset()
        self.tracker.update()
        while(self.tracker.get_my_pos() != [0, 0] and self.tracker.get_target_pos() != [1,1]):
            time.sleep(0.5)
            self.tracker.update()
        print("reset complete")

    def step(self, action):
        self.tracker.update()
        self.chaser.step(self.tracker.get_my_pos(), self.tracker.get_target_pos(), self.tracker.get_my_heading())
        self.runner.step_rl(self.tracker.get_target_heading(), action)
        time.sleep(self.time_step)
        self.tracker.update()
        chaser_pos = self.tracker.get_my_pos()
        runner_pos = self.tracker.get_target_pos()
        if(runner_pos and chaser_pos):
            next_state = np.array([chaser_pos[0], chaser_pos[1], runner_pos[0], runner_pos[1], self.tracker.get_my_pos(), self.tracker.get_target_heading()])
            reward = self.calculate_reward(self.state, next_state)
            if runner_pose[0] == chaser_pos[0] and runner_pose[1] == chaser_pos[1]:
                done = True
            else:
                done = False
        else:
            next_state = np.array([0, 0, 0, 0, 0, 0])
            reward = -100
            done = True
        return (next_state, reward, done)
        
