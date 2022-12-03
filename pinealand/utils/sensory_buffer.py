import abc

from six import with_metaclass


class SensoryBuffer(with_metaclass(abc.ABCMeta), object):

    def __init__(self):
        self.buffer = []


class VisualBuffer(SensoryBuffer):
    pass
