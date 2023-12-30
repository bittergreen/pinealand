from pinealand.utils.sensory_buffer import VisualBuffer


class Organ(object):
    # abstract class
    def __init__(self):
        pass


class SensoryOrgan(Organ):

    def __init__(self):
        super(SensoryOrgan, self).__init__()
        self.sensory_buffer = VisualBuffer()
