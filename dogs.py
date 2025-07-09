import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import json


class SerraDaEstrela:
    def __init__(self):
        self.sound = "Ao ao"
        self.color = "brown"

    def look_cute(self):
        print("{} is looking amazing!".format(self.name))


class Samoyed:
    def __init__(self):
        self.color = "white"
        self.position = np.zeros(4)

    def work(self):
        print("Pulling a sledge")
        self.position += np.random.randint(0,5,4) + np.array([0,0,0,1])  

    def look_cute(self):
        img = Image.open("gandalf1.jpg")
        img = np.asarray(img)
        plt.imshow(img)
        plt.show()





class Dog(SerraDaEstrela, Samoyed):

    def __init__(self, name, age):
        self.name =  name
        self.age = age
        self.sound = "Waf waf"
        self.color = "black"
        self.position = np.zeros(4)
        super().__init__()
        Samoyed.__init__(self)

    def walk(self):
        print("Walking on four legs")
        self.position += np.random.randint(0,2,4) + np.array([0,0,0,1])

    def bark(self):
        print(self.sound)



my_dog = Dog("Gandalf", 3)
print(my_dog.color)
my_dog.bark()
my_dog.look_cute()
print(my_dog.__dict__)
my_dog.work()