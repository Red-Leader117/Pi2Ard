import types, weakref

class Dummy():
    def __init__(self, name):
        self.name = name
    def __del__(self):
        print("delete",self.name)

d2 = Dummy("d2")
def func(self):
    print("func called")
d2.func = types.MethodType(func, weakref.ref(d2)) #This works
#d2.func = func.__get__(weakref.ref(d2), Dummy) #This works too
d2.func()
del d2
d2 = None
print("after d2")