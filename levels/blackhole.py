import random
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
    def __init__(self, level=None):
        #LEVEL INFORMATION
        self.worldInfo={
            "songname":'cave.mp3',
            "uitype":'default',
            "bg":'nightofnights'
            }
        self.level_length=50 #TEMPORARY, NORMALLY 10

        #SIZE values
        self.char_distance_x=40
        self.char_distance_y=40

        self.char_min_width=5
        self.char_min_height=1
        self.char_max_width=10
        self.char_max_height=5


        #THROWDOWN values
        self.spawn_time=0
        self.spawn_amount=0
        self.maxChar=0
        self.update_intensities(level)#dynamic value assignment based on character


        #character
        self.imports=['nope','fihs','stickman','spike','zapp']
        self.bullets = ['bananas']
        self.drop_health = 5  # how often it drops an extra life
        self.drop_bullet = 50 #chance out of 100 it drops a bullet per level
        self.speed=1
        

        #manually-generated formations to replace randomly-generated formations 
        self.manual_formations=[]

        form={
            0:['    ','    ','nope','    ','    ','    '],
        };self.manual_formations.append(form)

        form={
            0:['    ','nope','nope','nope','nope','    '],
        };self.manual_formations.append(form) 

        form={
            0:['nope','nope','nope','nope','nope','nope'],
            1:['    ','nope','nope','nope','nope','    '],
            2:['    ','    ','nope','nope','    ','    '],
        };self.manual_formations.append(form)

        
        self.manual_type=2 # [0 : no influence , 1 : random order , 2 : ordered] ; 0 and 2 will overwrite manual_influence.
        self.manual_loop=False #this only counts of the type is 2.
        self.manual_influence=0  #<0 is no influence, >100 is all influence ; only applies to type 1


    def update_intensities(self,level):
        self.spawn_time=random.randint((60-level),60)
        self.spawn_amount = int((1+(0.1*level))//1)
        self.maxChar = random.randint(5,int(5+(0.1*level)//1))
        # print(str(level),":",str(self.spawn_time),",",str(self.spawn_amount),",",str(self.maxChar))
