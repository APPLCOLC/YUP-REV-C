import time,random
from modules import characters


#LET THIS BE A TEMPLATE FOR THE LEVELS
#NAME THE CLASS "LEVEL"
class Level():

    #INITIALIZE THE LEVEL
    #CREATE A TIMER CALLED "self.start" USING TIME
    #SET "self.currentevent" TO 0
    #MAKE A LIST CALLED "self.events"
    #THE INITIALIZATION IS WHAT IS READ AT THE START OF "playstate.py"
    def __init__(self):
        self.start = time.time()
        self.currentevent = 0
        self.events = [True,True,True,True,True,True,True,True,True]


    #SPAWN FUNCTION CODE
    #spawn(char, allspriteclass, hurtclass, bulletclass, playerclass, specialcode=None)

    #"levelUpdate" IS WHAT IS CALLED EVERY SINGLE FRAME.
    #DUE TO THIS, YOU NEED TO CREATE A SECOND TIMER EVERY FRAME CALLED "self.end"
    #"timepassed" IS A VARIABLE THAT IS ABLE TO TELL HOW MUCH TIME HAS PASSED BETWEEN "self.start" and "self.end"
    #AFTER THESE VARIABLES ARE CREATED, YOU ARE ABLE TO CHECK THE NUMBER OF "timepassed" AND CAUSE EVENTS ACCORDINGLY.
        #This is where "self.events" comes into play.
        #If "self.events[self.currentevent]" is equal to "True", that means the event has not occured yet and the event will occur.
        #Once the event occurs:
        #   "self.events[self.currentevent]" gets marked as "False", telling the code not to occur again
        #   "self.currentevent" gets changed by 1, in order to know which event to mark False the next time around
        #At the end, there is also a "return" command so, when the event gets changed by 1, it doesn't roll to the next event, then the next, over and over.
        #   This is caused due to an error with the fact that "self.events" cannot be marked with an index of "self.currentevent" because it needs to know the order.
    #ALSO BE SURE TO IMPORT THE THREE THINGS: "HurtSprites"(class) "allsprites"(class) "bulletsprites"(class) "player"(variable)
    #THESE ARE WHAT IS USED IN ORDER TO SPAWN ITEMS
    def levelUpdate(self, allspriteclass, hurtclass, bulletclass, playerclass):
        try:
            self.end = time.time()
            timepassed = self.end - self.start

            if timepassed > 2 and self.events[0] == True:
                self.events[self.currentevent] = False
                self.currentevent += 1
                characters.spawn("nope",allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num":random.randint(0,600),"directionnum":1})
                return

            elif timepassed >= 4 and self.events[1] == True:
                self.events[self.currentevent] = False
                self.currentevent += 1
                for i in range(10):
                    characters.spawn("nope",allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num":random.randint(0,600),"directionnum":1})
                return

            elif timepassed >= 10 and self.events[2] == True:
                self.events[self.currentevent] = False
                for i in range(50):
                    characters.spawn("nope",allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num":random.randint(0,600),"directionnum":1})

                return
        except:
            return "finish"

        #Called at the end of every level file
        #Will finish the level
        if self.events[len(self.events) - 1] == False:
            return "finish"

        # print(self.currentevent, end = '')
        # print(self.events[self.currentevent])
        # print(self.events)






