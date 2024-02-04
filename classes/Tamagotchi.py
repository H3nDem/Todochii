from tkinter import StringVar

class Tamagotchi():
    MAX_HUNGER = 100
    HUNGER_THRESHOLD = 30
    
    def __init__(self):
        self.hunger = Tamagotchi.MAX_HUNGER
        self.hunger_display = StringVar()
        self.hunger_display.set("Hunger: {0}".format(self.hunger))

    def show_status(self):
        print("Hunger:", self.hunger, "/ 100")
        
    def get_hunger(self):
        return self.hunger
    
    def get_hunger_display(self):
        return self.hunger_display
    
    def update_hunger_display(self):
        self.hunger_display.set("Hunger: {0}".format(self.hunger))

    def isHungry(self):
        return self.hunger <= Tamagotchi.HUNGER_THRESHOLD


    # TODO : see how we will handle hunger and fun, if we just add (and not fill the whole bar)
            # We need a condition to make sur 100 is the max, thus we ensure to not go above this limit
    def feed(self):
        self.hunger = Tamagotchi.MAX_HUNGER
        self.update_hunger_display()

    def set_hunger(self, value):
        self.hunger = value
        self.update_hunger_display()

    # TODO : See if we rename it because it can be confusing
    # reduce the hunger bar
    def reduce_hunger(self):
        if (self.hunger > 0):
            self.hunger -= 1
            self.update_hunger_display()    
        









"""
class Tamagotchi():
    MAX_HUNGER = 99
    # MAX_FUN = 100
    HUNGER_THRESHOLD = 30
    # FUN_THRESHOLD = 30
    
    def __init__(self):
        self.hunger = Tamagotchi.MAX_HUNGER
        # self.Fun = Tamagotchi.MAX_FUN

    def show_status(self):
        print(
            "Hunger:", self.hunger, "/ 99"
            #, "\nFun:", self.Fun, "/ 100"
            )


    def get_hunger(self):
        return self.hunger






    def isHungry(self):
        return self.hunger <= Tamagotchi.HUNGER_THRESHOLD


    # TODO : see how we will handle hunger and fun, if we just add (and not fill the whole bar)
            # We need a condition to make sur 100 is the max, thus we ensure to not go above this limit
    def feed(self):
        self.hunger = Tamagotchi.MAX_HUNGER


    def set_hunger(self, value):
        self.hunger = value


    # TODO : See if we rename it because it can be confusing
    # reduce the hunger bar
    def reduce_hunger(self):
        if (self.hunger > 0):
            self.hunger -= 1
        
          
        
    def complain(self):
        if (self.isHungry()):
            print("I'm hungry")
        if (self.isBored()):
            print("I'm bored")








    # def isBored(self):
        # return self.Fun <= Tamagotchi.FUN_THRESHOLD
        
    # def play(self):
        # self.Fun = Tamagotchi.MAX_FUN        
        
    # def reduce_Fun(self):
        # self.Fun -= 1  
"""        