import abc

from pinealand.utils.sensory_buffer import VisualBuffer
from six import with_metaclass


class Organ(with_metaclass(abc.ABCMeta, object)):
    # abstract class
    def __init__(self):
        pass


class SensoryOrgan(Organ):

    def __init__(self):
        super(SensoryOrgan, self).__init__()
        self.sensory_buffer = VisualBuffer()
