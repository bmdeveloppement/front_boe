# -*- coding: utf-8 -*-

def _dummy_init(self, *args, **kwargs):
    """Empty function for overriding __init__ method on created singleton"""
    pass


class Singleton(object):
    """
    Singleton utilitary class.
    Effective singleton must inherit from this class
    """

    #Instance of the sigleton class.
    #Beware, it is not a Singleton instance,
    #it is an object inherited from Singleton instance
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        Override the instanciation of an object,creating a single instance.
        Initialization of the object is overrided from the second call"""
        if not isinstance(cls.__instance, cls):
            cls.__instance = object.__new__(cls, *args, **kwargs)
            cls.__instance.__init__(*args, **kwargs)
        cls.__init__ = _dummy_init
        return cls.__instance