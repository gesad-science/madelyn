from threading import Lock

class Singleton(type):

    _instances = {}

    _lock: Lock = Lock()
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            print(cls._instances)
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
