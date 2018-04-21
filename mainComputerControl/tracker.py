import tuio

class Tracker(object):

    def __init__(self):
        self.tracking = tuio.Tracking()
        self.tracker = None
        self.my_id = 0
        self.target_id = 2

    def update(self):
        self.tracking.update()

    def get_my_heading(self):
        for obj in self.tracking.objects():
            if (obj.id == self.my_id):
                return obj.angle

    def get_target_heading(self):
        for obj in self.tracking.objects():
            if (obj.id == self.target_id):
                return obj.angle

            
    def get_my_pos(self):
        for obj in self.tracking.objects():
            if (obj.id == self.my_id):
                return [obj.xpos, obj.ypos]

    def get_target_pos(self):
        for obj in self.tracking.objects():
            if (obj.id == self.target_id):
                return [obj.xpos, obj.ypos]
