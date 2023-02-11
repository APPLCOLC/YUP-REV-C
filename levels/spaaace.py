from levels import template
import random
class data(template.data):
    def __init__(self, level=1):

        template.data.__init__(self,level)

        #LEVEL INFORMATION
        self.worldInfo={
            "songname":'cabbage.mp3',
            "uitype":'default',
            "bg":'Space'
            }

        #character
        self.imports = ['nope','fihs','stickman','spike','zapp'] #PUT DUPLICATES IN THERE FOR DIFFERENT RATES OF CHARACTERS!!!
        self.bullets = ['bananas','strawberry']
        self.drop_health = 5 #how often it drops an extra life
        self.drop_bullet = 20 #chance out of 100 it drops a bullet per level
        self.speed=1
        

        #manually-generated formations to replace randomly-generated formations 
        self.manual_formations=[]

        form={
            0:['nope'],
        };self.manual_formations.append(form)

        form={
            0:['    ','nope','nope','nope','nope','    '],
        };self.manual_formations.append(form) 

        form={
            0:['nope','nope','nope','nope','nope','nope'],
            1:['    ','nope','nope','nope','nope','    '],
            2:['    ','    ','nope','nope','    ','    '],
        };self.manual_formations.append(form)

        
        self.manual_type=0 # [0 : no influence , 1 : random order , 2 : ordered] ; 0 and 2 will overwrite manual_influence.
        self.manual_loop=True #this only counts of the type is 2.
        self.manual_influence=0  #<0 is no influence, >100 is all influence ; only applies to type 1


    def update_intensities(self,level):
        self.spawn_time=random.randint((60-level),60)
        self.spawn_amount = int((1+(0.1*level))//1)
        self.maxChar = random.randint(5,int(5+(0.1*level)//1))
        # print(str(level),":",str(self.spawn_time),",",str(self.spawn_amount),",",str(self.maxChar))
