import time,random
from modules import characters



class Level():
    def __init__(self):
        self.start = time.time()
        self.currentevent = 0
        self.events = [True,True,True,True,True,True,True,True,True]


    def levelUpdate(self, allspriteclass, hurtclass, bulletclass, playerclass):
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

        elif timepassed >= 7.5 and self.events[2] == True:
            self.events[self.currentevent] = False
            self.currentevent += 1
            for i in range(50):
                temp_start = time.time()
                characters.spawn("nope",allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num":random.randint(0,600),"directionnum":1})

        elif timepassed >= 10 and self.events[3] == True:
            self.events[self.currentevent] = False
            self.currentevent += 1
            characters.spawn("nope", allspriteclass, hurtclass, bulletclass, playerclass, specialcode={"num": random.randint(0, 600), "directionnum": 0})
        elif timepassed >= 10.25 and self.events[4] == True:
            self.events[self.currentevent] = False
            self.currentevent += 1
            characters.spawn("nope", allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num": random.randint(0, 600), "directionnum": 1})
        elif timepassed >= 10.5 and self.events[5] == True:
            self.events[self.currentevent] = False
            self.currentevent += 1
            characters.spawn("nope", allspriteclass, hurtclass, bulletclass, playerclass, specialcode={"num": random.randint(0, 600), "directionnum": 2})
        elif timepassed >= 10.75 and self.events[6] == True:
            self.events[self.currentevent] = False
            self.currentevent += 1
            characters.spawn("nope", allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num": random.randint(0, 600), "directionnum": 3})
        elif timepassed >= 11 and self.events[7] == True:
            self.events[self.currentevent] = False
            self.currentevent += 1
            for i in range(40):
                characters.spawn("nope", allspriteclass, hurtclass, bulletclass, playerclass,specialcode={"num": i * 10 , "directionnum": i%4 })

            return





