class data:
    def __init__(self):
        print("BLACKHOLE LOADED")
        self.time=None

        self.spawn_time=60 #how often a character spawn occurs - MEASURED IN FRAMES
        self.spawn_amount=1 #how many characters spawn in a spawn occurrence
        # self.variation=True #if the spawn time, spawn amount, and maxChar can be changed in slight ways to make it less uniform
        self.maxChar=None #maximum characters spawned

        self.formation=None
        self.imports=['nope']
        self.speed=1;self.minspeed=0.5;self.maxspeed=5
        self.speedINC={"time":False,"char":False}

    def lvl1(self):
        self.__init__() #resets values
        # print("lvl1 run")
        self.time=None
        self.maxChar=2
        self.formation={
            0: ['nope', '    ', '    ', 'nope'],
            1: ['    ', 'nope', 'nope', '    '],
            2: ['nope', '    ', '    ', 'nope'],
            3: ['    ', 'nope', 'nope', '    '],
            4: ['nope', '    ', '    ', 'nope'],
            5: ['    ', 'nope', 'nope', '    ']
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
