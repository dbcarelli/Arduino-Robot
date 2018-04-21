from xbee import XBee

class Controller(object):
    def __init__(self, dt, forward_speed, pivot_threshold, port):
        self.current_heading = None
        self.target_heading = None
        self.error = None
        self.integrator = 0
        self.max = 50
        self.forward_throttle_avg = forward_speed
        self.kp = (253.0/360.0)*5
        self.ki = 0
        self.dt = dt
        self.xBee = XBee(port)
        self.motor_input_pivot = 0
        self.motor_input_right = 0
        self.motor_input_left  = 0
        self.pivot_threshold = pivot_threshold


    def update_motors(self, current_heading, target_heading):
        # update state
        self.current_heading = current_heading
        self.target_heading = target_heading

        # calculate error
        self.get_error()

        if (abs(self.error) > self.pivot_threshold):
            # calculate pivit motor inputs
            self.get_motor_input_pivot()

            # command the motors to pivot
            self.command_motors_pivot()

        else:
            # calculate pivit motor inputs
            self.get_motor_input_forward()

            # command the motors forward
            self.command_motors_forward()

    def get_error(self):

        self.error = (self.target_heading - self.current_heading)

        if ((self.error) > 180):
            self.error = -1.0*(360 + self.current_heading - self.target_heading )
        if( (self.error) < -180):
            self.error = (360 + self.target_heading - self.current_heading )

        print self.error

    def get_motor_input_pivot(self):
        # update integrator term
        self.update_integrator()

        #   result     proportional gain        integral gain        bias
        motor_input = (self.kp*self.error)+(self.ki*self.integrator)+3

        if (abs(motor_input) > self.max):
            self.motor_input_pivot = int(motor_input/abs(motor_input))*self.max
            return

        self.motor_input_pivot = motor_input

    def get_motor_input_forward(self):
        # veer left
        if (self.error > 0):
            self.motor_input_right = self.forward_throttle_avg + abs(self.error)*1.5
            self.motor_input_left = self.forward_throttle_avg - abs(self.error)*1.5

        # veer right
        elif (self.error < 0):
            self.motor_input_right = self.forward_throttle_avg - abs(self.error)*1.5
            self.motor_input_left = self.forward_throttle_avg + abs(self.error)*1.5

        # stay the course
        else:
            self.motor_input_right = self.forward_throttle_avg
            self.motor_input_left = self.forward_throttle_avg

        # make sure inputs are negative
        if (self.motor_input_right < 0):
            self.motor_input_right = 0
        if (self.motor_input_left < 0):
            self.motor_input_left = 0

    def update_integrator(self):
        self.integrator += self.error*self.dt

    def command_motors_pivot(self):
        # determine direction
        if (self.motor_input_pivot >= 0):
            self.xBee.send_command(1)
        else:
            self.xBee.send_command(2)

        # send motor speed
        self.xBee.send_command(abs(self.motor_input_pivot))

    def command_motors_forward(self):
        # notify that we are mooving forward
        self.xBee.send_command(3)

        # send pre-limitor
        self.xBee.send_command(4)

        # send motor inputs
        self.xBee.send_command(self.motor_input_left)
        self.xBee.send_command(self.motor_input_right)

        # send post-limitor
        self.xBee.send_command(5)

    def coast(self):
        if (self.error > self.pivot_threshold):
            self.motor_input_pivot -= 5
            if (self.motor_input_pivot < 6):
                self.motor_input_pivot = 0;
            self.command_motors_pivot()
        else:
            self.motor_input_right -= 10
            self.motor_input_left -= 10
            # make sure inputs are negative
            if (self.motor_input_right < 0):
                self.motor_input_right = 0
            if (self.motor_input_left < 0):
                self.motor_input_left = 0
            self.command_motors_forward()

    def stop(self):
        self.xBee.send_command(0)

    def close(self):
        self.xBee.close()

    def update_pivot_threshold(self, new_pivot_threshold):
        self.pivot_threshold = new_pivot_threshold

    def update_throttle(self, new_throttle):
        self.forward_throttle_avg = new_throttle
