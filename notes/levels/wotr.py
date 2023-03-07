from levels import template
import random
class data(template.data):
    def __init__(self, level=1):

        template.data.__init__(self,level)

        #LEVEL INFORMATION
        self.worldInfo={
            "songname":'meowchill.mp3',
            "uitype":'default',
            "bg":'water'
            }

        #character
        self.imports = ['nope','fihs'] #PUT DUPLICATES IN THERE FOR DIFFERENT RATES OF CHARACTERS!!!
        self.bullets = ['strawberry']
        self.drop_health = 5 #how often it drops an extra life
        self.drop_bullet = 20 #chance out of 100 it drops a bullet per level
        self.speed=1

    def update_intensities(self,level):
        self.spawn_time=random.randint((60-level),60)
        self.spawn_amount = int((1+(0.1*level))//1)
        self.maxChar = random.randint(5,int(5+(0.1*level)//1))
        # print(str(level),":",str(self.spawn_time),",",str(self.spawn_amount),",",str(self.maxChar))
