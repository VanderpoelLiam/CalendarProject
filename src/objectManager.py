class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ObjectManager(metaclass=Singleton):
    __objects = []

    def __contains__(self, obj):
        return ObjectManager.__objects.__contains__(obj)

    def addObj(self, obj):
        ObjectManager.__objects.append(obj)

    def removeObj(self, obj):
        ObjectManager.__objects.remove(obj)

    def getObjects(self):
        return ObjectManager.__objects

    def clearObjects(self):
        ObjectManager.__objects.clear()

    def getNumObjects(self):
        return len(ObjectManager.__objects)
