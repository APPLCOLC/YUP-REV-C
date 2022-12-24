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
        """LEVEL INFORMATION"""
        self.worldInfo={"songname":'cabbage.mp3',"uitype":'default',"bg":'Space'}

        """THESE ARE THE DEFAULTS--if they are not overwritten, this is what will be used!!"""
        self.time=None
        self.char_distance_x=40
        self.char_distance_y=40
        self.formation_speed=0

        self.spawn_time=60 #how often a character spawn occurs - MEASURED IN FRAMES
        self.spawn_amount=1 #how many characters spawn in a spawn occurrence
        # self.variation=True #if the spawn time, spawn amount, and maxChar can be changed in slight ways to make it less uniform
        self.maxChar=None #maximum characters spawned

        self.formation=None
        self.imports=['nope','fihs','stickman','spike','zapp']
        self.speed=1
        self.speedINC={"time":True,"char":False}

    def lvl1(self):
        self.__init__() #resets values
        # print("lvl1 run")
        self.time=None
        self.maxChar=4
        self.formation={
            0:['stickman','zapp','zapp','stickman'],
        }
    def lvl2(self):
        self.__init__()  # resets values
        # print("lvl2 run")
        self.time=None
        self.maxChar = 2
        self.formation={
            0: ['spike', 'spike', 'spike','spike','spike'],
        }
    def lvl3(self):
        self.__init__()  # resets values
        # print("lvl3 run")
        self.time=None
        self.maxChar = 50
        self.spawn_time = 1
        self.formation={
            0:['stickman','stickman','stickman','stickman','stickman','stickman','stickman'],
            1:['stickman','stickman','stickman','stickman','stickman','stickman','stickman'],
            2:['stickman','stickman','stickman','stickman','stickman','stickman','stickman'],
            3: ['stickman', 'stickman', 'stickman', 'stickman', 'stickman', 'stickman', 'stickman'],
            4: ['stickman', 'stickman', 'stickman', 'stickman', 'stickman', 'stickman', 'stickman'],
            5: ['stickman', 'stickman', 'stickman', 'stickman', 'stickman', 'stickman', 'stickman']
        }
    def lvl4(self):
        self.__init__()  # resets values
        # print("lvl4 run")
        self.speed=0.5;self.speedINC={"time":False,"char":False}
        self.time=None
        self.maxChar = 10
        self.formation={
            0:['stickman','stickman','stickman','stickman','stickman','stickman','stickman'],
            1: ['nope', 'fihs', 'spike', 'fihs', 'spike','fihs','nope'],
            2: ['spike', 'fihs', 'nope', 'fihs', 'nope','fihs','spike'],
            3: ['    ', 'fihs', 'spike', 'fihs', 'spike','fihs','    '],
            4: ['    ', 'fihs', 'nope', 'fihs', 'nope','fihs','    '],

        }
    def BOSS(self):
        self.__init__()  # resets values
        self.time=None
        self.spawn_time=1
        pass
