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
        self.char_distance_x=40
        self.char_distance_y=40

        self.spawn_time=1 #how often a character spawn occurs - MEASURED IN FRAMES
        self.spawn_amount=1 #how many characters spawn in a spawn occurrence
        self.maxChar=None #maximum characters spawned

        self.formation=None
        self.imports=['nope','fihs','stickman','spike','zapp']
        self.speed=1
        self.speedINC={"time":True,"char":True}
