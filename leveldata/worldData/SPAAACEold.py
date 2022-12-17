"""HOW A LEVEL WORKS
-Class is defined
-Several values are defined within the class
    -time limit
    -intensity
    -formation
-All of these values begin as 'None' when an instance of the class is created.
-Then, what fileReader.py will do is run the "level methods" to redefine the values.
-Example:
    -levelReader.py loads "SPAAACE.py", which then creates all the values as None, just to begin
    -levelReader.py uses the "lvl1" function to define all the values and then run the program.
    -when lvl1 is over, it then runs "lvl2" to begin a new formation, then lvl2 to lvl3, so on and so forth.
"""
class data:
    """
    WORLD FILE INFORMATION
    Init declares the values, aka creating them.
    All the 'lvl' arguments will then modify said values for when the formation is created.
    So, if the level is 1, lvl1 is run to modify the values.
    """
    def __init__(self):
        """THESE ARE THE DEFAULTS--if they are not overwritten, this is what will be used!!"""
        self.time=None

        self.spawn_time=60 #how often a character spawn occurs - MEASURED IN FRAMES
        self.spawn_amount=1 #how many characters spawn in a spawn occurrence
        # self.variation=True #if the spawn time, spawn amount, and maxChar can be changed in slight ways to make it less uniform
        self.maxChar=None #maximum characters spawned

        self.formation=None
        self.imports=['nope']
        self.speed=1;self.minspeed=0.5;self.maxspeed=5
        self.speedINC={"time":True,"char":False}

    def lvl1(self):
        self.__init__() #resets values
        # print("lvl1 run")
        self.time=None
        self.maxChar=2
        self.formation={
            0:['nope','nope','nope','nope'],
        }
    def lvl2(self):
        self.__init__()  # resets values
        # print("lvl2 run")
        self.time=None
        self.maxChar = 2
        self.formation={
            0: ['nope', 'nope', 'nope','nope','nope'],
        }
    def lvl3(self):
        self.__init__()  # resets values
        # print("lvl3 run")
        self.time=None
        self.maxChar = 6
        self.formation={
            0: ['nope', 'nope', 'nope'],
            1: ['nope', 'nope', 'nope'],
            2: ['nope', 'nope', 'nope']
        }
    def lvl4(self):
        self.__init__()  # resets values
        # print("lvl4 run")
        self.speed=self.minspeed=self.maxspeed=0.5;self.speedINC={"time":False,"char":False}
        self.time=None
        self.maxChar = 10
        self.formation={
            0: ['nope', 'nope', 'nope', 'nope', 'nope','nope','nope'],
            1: ['nope', 'nope', 'nope', 'nope', 'nope','nope','nope'],
            2: ['    ', 'nope', 'nope', 'nope', 'nope','nope','    '],
            3: ['    ', 'nope', 'nope', 'nope', 'nope','nope','    '],
            4: ['    ', '    ', 'nope', 'nope', 'nope','    ','    ']
        }
    def BOSS(self):
        self.__init__()  # resets values
        self.time=None
        self.spawn_time=1
        pass
