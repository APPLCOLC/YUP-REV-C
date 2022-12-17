"""HOW A LEVEL WORKS
-Class is defined
-Several values are defined within the class
    -time limit
    -intensity
    -formation
-All of these values begin as 'None' when an instance of the class is created.
-Then, what fileReader.py will do is run the "level methods" to redefine the values.
-Example:
    -levelReader.py loads "SPAAACE.py", which then creates all of the values as None, just to begin
    -levelReader.py uses the "lvl1" function to define all of the values and then run the program.
    -when lvl1 is over, it then runs "lvl2" to begin a new formation, then lvl2 to lvl3, so on and so forth.
"""
class data:
    def __init__(self):
        self.time=None
        self.intensity=None
        self.formation=None

    def lvl1(self):
        time=None
        intensity=1
        formation={
            1:['nope','nope','nope']
        }
    def lvl2(self):
        time=None
        intensity=1
        formation={}
    def lvl3(self):
        time=None
        intensity=1
        formation={}
    def lvl4(self):
        time=None
        intensity=1
        formation={}
    def BOSS(self):
        time=None
        intensity=1
        pass
