# removed player spawn
# removed player addition to allsprites and playersprites
# removed player from debugspawn
# removed player controls from events
# removed player UI health



"START###############################################################"
"""IMPORTS--------------------"""
import pygame,math,time,random
"""DISPLAY INITIALIZATION--------------------"""
pygame.display.set_caption("YUP")
icon = pygame.Surface((50,50))
try:
    icon =  pygame.image.load("assets/images/UI/icon.ico")
    pygame.display.set_icon(icon)
except: pass
try:WIN = pygame.display.set_mode((600,800),pygame.SCALED)
except:WIN = pygame.display.set_mode((600,800))

"""INITIALIZATION--------------------"""
pygame.font.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
allsprites = pygame.sprite.Group()
playersprite = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
from modules import player as playerguy
from modules.bullets import display_bullet


"""IMAGES##############################################################"""
class UI_images():
    #BEGIN AND END
    beginImage = pygame.image.load("./assets/images/UI/BEGIN AND END/GET READY.png")
    endImage = pygame.image.load("./assets/images/UI/BEGIN AND END/LEVEL COMPLETE.png")

    #ERRORS
    errortitle = pygame.image.load("./assets/images/UI/errors/errorOccured.png")

    #LOGO FOR TITLE
    logo1 = pygame.image.load("./assets/images/UI/TITLEMENU/logo1.png")
    logo2 = pygame.image.load("./assets/images/UI/TITLEMENU/logo2.png")
    logo3 = pygame.image.load("./assets/images/UI/TITLEMENU/logo3.png")
    titlebglogo = [logo1, logo2, logo3]
    del logo1, logo2, logo3

    #PAUSE GRAPHIC
    pause1=pygame.image.load('./assets/images/UI/pause/paus\'d (1).png')
    pause2=pygame.image.load('./assets/images/UI/pause/paus\'d (2).png')
    pause3=pygame.image.load('./assets/images/UI/pause/paus\'d (3).png')
    pause=[pause1,pause2,pause3]
    for i in range(len(pause)): pause[i]=pygame.transform.scale(pause[i],(600,200))
    del pause1,pause2,pause3

    #PRESS SPACE
    press_space = pygame.image.load("./assets/images/UI/space.png")

    #BUTTONS
    quitbutton = pygame.image.load("./assets/images/UI/quitbutton.png")
    quitbuttonpressed = pygame.image.load("./assets/images/UI/quitbuttonpressed.png")
    QUIT = [quitbutton, quitbuttonpressed]
    del quitbutton, quitbuttonpressed
    startbutton = pygame.image.load("./assets/images/UI/startbutton.png")
    startbuttonpressed = pygame.image.load("./assets/images/UI/startbuttonpressed.png")
    START = [startbutton, startbuttonpressed]
    del startbutton, startbuttonpressed
    optionsbutton = pygame.image.load("./assets/images/UI/optionsbutton.png")
    optionsbuttonpressed = pygame.image.load("./assets/images/UI/optionsbuttonpressed.png")
    OPTIONS = [optionsbutton, optionsbuttonpressed]
    del optionsbutton, optionsbuttonpressed
    continuebutton = pygame.image.load("./assets/images/UI/continuebutton.png")
    continuebuttonpressed = pygame.image.load("./assets/images/UI/continuebuttonpressed.png")
    CONTINUE = [continuebutton,continuebuttonpressed]
    del continuebutton,continuebuttonpressed

    #LOADING
    loading = pygame.image.load("./assets/images/UI/loading/loadgif (1).png")

    #GENERAL
    yes = pygame.image.load("./assets/images/UI/YES.png")
    yes = pygame.transform.scale(yes, (50, 25))
    no = pygame.image.load("./assets/images/UI/NO.png")
    no = pygame.transform.scale(no, (50, 25))
    on = pygame.image.load("./assets/images/UI/ON.png")
    off = pygame.image.load("./assets/images/UI/OFF.png")
    checkmark = pygame.image.load("./assets/images/UI/CHECKMARK.png")
    xmark = pygame.image.load("./assets/images/UI/X.png")
    slider = pygame.image.load("./assets/images/UI/slider.png")
    knob = pygame.image.load("./assets/images/UI/knob.png")

    #SETTINGS IMAGES
    optionbg = pygame.image.load("./assets/images/UI/options/bg.png")
    option_placeholder = pygame.image.load("./assets/images/UI/options/placeholder.png")
    option_funnymode = pygame.image.load("./assets/images/UI/options/funnymode.png")
    option_ostvolume = pygame.image.load("./assets/images/UI/options/ostVolume.png")
    option_sfxvolume = pygame.image.load("./assets/images/UI/options/sfxVolume.png")
    option_mute = pygame.image.load("./assets/images/UI/options/MUTE.png")
    option_fullscreen = pygame.image.load("./assets/images/UI/options/fullscreen.png")
    option_lowquality = pygame.image.load("./assets/images/UI/options/LowQuality.png")
    option_fps = pygame.image.load("./assets/images/UI/options/FPS.png")
    option_30 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS30.png"),(50,30))
    option_60 = pygame.transform.scale(pygame.image.load("./assets/images/UI/options/FPS60.png"),(50,30))
    option_spriteFlick = pygame.image.load("./assets/images/UI/options/spriteFlicker.png")
    option_extraVisuals = pygame.image.load("./assets/images/UI/options/extraVisuals.png")
    option_simpleBG = pygame.image.load("./assets/images/UI/options/SimpleBG.png")

    #GAME OVER IMAGES
    continueGraphic1 = pygame.image.load("./assets/images/UI/game over/continue 1.png")
    continueGraphic2 = pygame.image.load("./assets/images/UI/game over/continue 2.png")
    continueGraphic3 = pygame.image.load("./assets/images/UI/game over/continue 3.png")
    continueGraphic4 = pygame.image.load("./assets/images/UI/game over/continue 4.png")
    continueGraphic = [continueGraphic2,continueGraphic3,continueGraphic4,continueGraphic1]
    del continueGraphic2, continueGraphic3, continueGraphic4, continueGraphic1
    gameOverGraphic = pygame.image.load("./assets/images/UI/game over/GAME OVER.png")
    scoreGraphic = pygame.image.load("./assets/images/UI/game over/SCORE.png")

    #BAGKGROUNDS
    levelselectBG = pygame.image.load("./assets/images/UI/level select/levelSelectBG.png")
    titlebg1 = pygame.image.load("./assets/images/UI/TITLEMENU/background.png")
    erorrbg = pygame.image.load("./assets/images/UI/errors/bg.png")
    loadbg = pygame.image.load("./assets/images/UI/splash.png")

    #CURSOR
    cursor = pygame.image.load("./assets/images/UI/LIVES/000.png")
ui=UI_images




"""SOUNDS##############################################################"""
class Sounds():
        
    def __init__(self):
        ###################SOUNDS####################
        self.ostList=[];self.soundList=[]

        #UI NOISES
        self.denied=pygame.mixer.Sound('./assets/sounds/sfx_denied.wav');self.soundList.append(self.denied)
        self.back=pygame.mixer.Sound('./assets/sounds/sfx_back.wav');self.soundList.append(self.back)
        self.scroll=pygame.mixer.Sound('./assets/sounds/sfx_scroll.wav');self.soundList.append(self.scroll)
        self.select=pygame.mixer.Sound('./assets/sounds/sfx_select.wav');self.soundList.append(self.select)
        self.select2=pygame.mixer.Sound('./assets/sounds/sfx_select2.wav');self.soundList.append(self.select2)
        self.error=pygame.mixer.Sound('./assets/sounds/QUACK.wav');self.soundList.append(self.error)
        #ENEMY SOUNDS
        self.hit = pygame.mixer.Sound('./assets/sounds/sfx_boomsmall.wav');self.soundList.append(self.hit)
        self.bighit = pygame.mixer.Sound('./assets/sounds/sfx_boombig.wav');self.soundList.append(self.bighit)
        self.bosshit = pygame.mixer.Sound('./assets/sounds/sfx_bosshit.wav');self.soundList.append(self.bosshit)
        self.nyoom = pygame.mixer.Sound('./assets/sounds/sfx_nyoom.wav');self.soundList.append(self.nyoom)
        self.death = pygame.mixer.Sound('./assets/sounds/sfx_death.wav');self.soundList.append(self.death)
        self.ouch = pygame.mixer.Sound('./assets/sounds/sfx_ouch.wav');self.soundList.append(self.ouch)
        self.yeah = pygame.mixer.Sound('./assets/sounds/sfx_yeah.wav');self.soundList.append(self.yeah)

        #BULLET NOISES
        self.shoot_bap1 = pygame.mixer.Sound('./assets/sounds/shoot_bap.wav');self.soundList.append(self.shoot_bap1)
        self.shoot_bap2 = pygame.mixer.Sound('./assets/sounds/shoot_bap2.wav');self.soundList.append(self.shoot_bap2)
        self.shoot_bap3 = pygame.mixer.Sound('./assets/sounds/shoot_bap3.wav');self.soundList.append(self.shoot_bap3)
        self.shoot_bap4 = pygame.mixer.Sound('./assets/sounds/shoot_bap4.wav');self.soundList.append(self.shoot_bap4)
        self.shoot_realistic = pygame.mixer.Sound('./assets/sounds/shoot_realistic.wav');self.soundList.append(self.shoot_realistic)
        self.shoot_laser = pygame.mixer.Sound('./assets/sounds/shoot_laser.wav');self.soundList.append(self.shoot_laser)
        self.shoot_bee = pygame.mixer.Sound('./assets/sounds/shoot_bee.wav');self.soundList.append(self.shoot_bee)
        self.shoot_missile = pygame.mixer.Sound('./assets/sounds/shoot_missile.wav');self.soundList.append(self.shoot_missile)

        self.continueEnd = pygame.mixer.Sound('./assets/ost/continueEnd.wav');self.soundList.append(self.continueEnd)
        ##############################################
        
        self.offsetSounds = {self.shoot_laser:0.5,self.shoot_realistic:0.25}

    ###############FUNCTIONS###############-
    def play_song(self,dir):
        try:curSong=pygame.mixer.music.load("./assets/ost/"+dir)
        except:print("IMPORT FAIL")
        try:
            with open('./assets/settings.txt','r') as data:vol=eval(data.read())['OST VOL'][0]
            pygame.mixer.music.set_volume(vol)
        except BaseException as e:
            print("song volume error")
        pygame.mixer.music.play(loops=10)
        return curSong
    def stop_song(curSong=None):
        pygame.mixer.music.stop()

    def play_nonmain_song(self,dir):
        #This is specifically because if you replace the music file being played, in a menu for instance, it will not remember any song played before.
        #If you pause the game, it replaces the gameplay music with the pause music, and forges all about the gameplay music.
        try:curSong=pygame.mixer.Sound("./assets/ost/"+dir)
        except:print("IMPORT FAIL")
        try:
            with open('./assets/settings.txt','r') as data:vol=eval(data.read())['OST VOL'][0]
            curSong.set_volume(vol)
        except:
            print("nonmain song volume error")
        curSong.play()
        return curSong
    #songs are easily stopped on their own and do not need a stop function
        
    def adjust_sounds(self, volume):
        for item in self.soundList:
            item.set_volume(volume)
        self.apply_offsets()
        # death.set_volume(death.get_volume() / 2)
    def adjust_ost(self, volume=None):
        if volume!=None: 
            # try:
            # print("volume is present | volume set to",str(volume))
            pygame.mixer.music.set_volume(volume)
            # except:print("adjust_ost error")
        else:
            # try:
            # print("volume is missing | volume set to",str(volume))
            with open('./assets/settings.txt','r') as data:volume=eval(data.read())['OST VOL'][0]
            pygame.mixer.music.set_volume(volume)
            # except:print("adjust_ost error")
      
    def apply_offsets(self):
        for k,v in self.offsetSounds.items():
            soundvol=self.soundList[self.soundList.index(k)].get_volume()*v
            # print(str(self.soundList[self.soundList.index(k)].get_volume()),"|",str(v),"|",str(soundvol))
            self.soundList[self.soundList.index(k)].set_volume(soundvol)
                # except: print("failed")

sounds=Sounds();sounds.apply_offsets()
# print(sounds)




"""SHARED ASSETS##############################################################"""

"""APPLYING SETTINGS--------------------"""
def readapply(settings=None, nonmain_song=None):
    if settings == None:
        with open("assets/settings.txt", "r") as data:
            # print("settings not present | settings file read")
            settings = eval(data.read())

    fullscreen = settings["FULLSCREEN"][0]
    # mobile= True

    # audio adjust
    sounds.adjust_sounds(settings['SOUND VOL'][0])
    sounds.adjust_ost(settings['OST VOL'][0])
    if nonmain_song != None: nonmain_song.set_volume(settings['OST VOL'][0])

    # screen adjust
    if fullscreen:
        pygame.display.set_mode((600, 800), pygame.FULLSCREEN | pygame.SCALED)
    else:
        pygame.display.set_mode((600, 800), pygame.SCALED)

    return settings

"""DEBUG TEXT--------------------"""
def debug_displays(allsprites,sprite_class_dict,variables,time,FPS,WIN=None): #-PLAYREMOVE
    baseText=["-DEBUG-"]
    baseText.append("FPS:"+str(round(FPS,1)))
    baseText.append("TIME:"+str(round(time,1)))
    for key, value in variables.items():
        baseText.append(str(key) + "-var:" + str(len(value)))
    baseText.append("ALLSPRITES:"+str(len(allsprites)))
    for key,value in sprite_class_dict.items():
        baseText.append(""+str(key)+":"+str(len(value)))
    font=pygame.font.Font("./assets/font/Setfont-Regular.ttf",20)
    if WIN==None:print(baseText)
    else:
        for i in range(len(baseText)):
            surface = font.render(str(baseText[i]), True, "white")
            WIN.blit(surface,(0,((i*20)+30)))
            del surface
    del font,baseText
 
"""RESETTING TEMPSAVE--------------------"""
def reset_progress():
    with open("./assets/tempsave.txt","w") as data:
        tempsave = {"NewGame?":True,"LevelSelect?":False,"CurrentLevel":1,"PlayerInstance":None}
        data.write(str(tempsave))

"""LOADING--------------------"""
def LongLoad(WIN=WIN,ui=ui):
    WIN.blit(ui.loadbg,(0,0))
    pygame.display.update()
def shortLoad(WIN=WIN,ui=ui):
    WIN.blit(ui.loading,(0,0) )
    pygame.display.update()

"""SCORE DISPLAY--------------------"""
def display_score(scoreValue,coord,WIN,snap=True,shadow=True,color=(0,0,0),shadowColor=(255,255,255),size=20):
    scoreFont = pygame.font.Font("./assets/font/Setfont-Regular.ttf",size)
    if shadow: scoreSurface = scoreFont.render(str(scoreValue),True,color,shadowColor)
    else: scoreSurface = scoreFont.render(str(scoreValue),True,color)
    scoreRect = scoreSurface.get_rect()
    if snap:scoreRect.right = coord[0]
    else: scoreRect.center = coord
    WIN.blit(scoreSurface,scoreRect)
    del scoreFont,scoreRect,scoreSurface

"""APPLYING SOME TEMPORARY VALUES--------------------"""
reset_progress()
LongLoad()







"""IMPORTANT MODULES##############################################################"""
"""BACKGROUNDS--------------------"""
class BG():
    """CONCEPT PSEUDOCODE
    BG CLASS
        INIT
            values are created
                photo name (string) (defaults at "null")
                current frame (int) (starts at 1)
                WIN (the window)
                prefix (string)
                    save several frame arguments as values:
                        x
                        (x)
                        frame (x)
                        framex
                        frame x
                        Frame (x)
                        Framex
                        Frame x
                there are several try/except statements that cycle through these frame arguments until one works, in which it saves that one as the preferred prefix
            all values are taken in as arguments, except prefix
            it will then blit the first frame as a test
        UPDATE  
            try to blit the prefix and the frame to the screen
            if there is an error, like the frames going out-of-range, the current frame cycles back to 1.
"""
    def __init__(self, WIN, photoName='null',curFrame=1):
        #beginning values
        self.WIN,self.photoName,self.curFrame=WIN,photoName,curFrame #converting arguments to variables
        self.prefix=None #the prefix used for loading the directory
        self.dir=[] #all of the images loaded into one list
        self.bgY,self.bgX=0,0 #scroll stuff

        #iterating through every value in the prefixlist to see if it works
        prefixList=[('',''),('(',')'),('frame (',')'),('frame',''),('frame ',''),('Frame (',')'),('Frame',''),('Frame ','')]
        x=0
        for item in prefixList:
            try:
                photo=pygame.image.load(('./assets/images/bg/' + self.photoName + '/' + prefixList[x][0] + '1' + prefixList[x][1] + '.png'))
                self.prefix=prefixList[x];del x;break
            except Exception as E:x+=1
            if x > len(prefixList): x=0;self.photoName='null'

        #opening config.txt  
        try:
            with open(('./assets/images/bg/' + self.photoName + '/config.txt'),"r") as data:
                self.config=eval(data.read())
                self.spd_c=0 #this is a counter variable for if the speed is halved. it will only advance every 2 frames.
        except Exception as E:
            self.config=None; print("no config"); print(E)

        #assembling a list made from the images
        while True:
            try:
                if self.config != None:
                    item=pygame.image.load(('./assets/images/bg/' + self.photoName + '/' + self.prefix[0] + str(self.curFrame) + self.prefix[1] + '.png'))
                    item=pygame.transform.scale(item,(600,800))
                    item=pygame.transform.flip(item,self.config['flip_horiz'],self.config['flip_vert'])
                    item.convert_alpha();item.set_alpha(self.config['opacity'])
                    self.dir.append(item)
                else:
                    item=pygame.image.load(('./assets/images/bg/' + self.photoName + '/' + self.prefix[0] + str(self.curFrame) + self.prefix[1] + '.png'))
                    item=pygame.transform.scale(item,(600,800)).convert_alpha()
                    self.dir.append(item)
                self.curFrame+=1
            except Exception as E:
                self.curFrame=1
                break
    def decoys(self):
        if self.bgY!=0:
            self.WIN.blit(self.dir[self.curFrame],(self.bgX,self.bgY-800))
            self.WIN.blit(self.dir[self.curFrame],(self.bgX,self.bgY+800))
        if self.bgX!=0:
            self.WIN.blit(self.dir[self.curFrame],(self.bgX+600,self.bgY))
            self.WIN.blit(self.dir[self.curFrame],(self.bgX-600,self.bgY))
        if self.bgY!=0 and self.bgX!=0:
            self.WIN.blit(self.dir[self.curFrame],(self.bgX+600,self.bgY-800))
            self.WIN.blit(self.dir[self.curFrame],(self.bgX-600,self.bgY+800))
            self.WIN.blit(self.dir[self.curFrame],(self.bgX+600,self.bgY+800))
            self.WIN.blit(self.dir[self.curFrame],(self.bgX-600,self.bgY-800))
        return
    def update(self):
        self.WIN.fill("black")#initial screen fill in case of transparancy 
        #SPEED CODE IF CONFIG IS PRESENT
        if self.config != None:
            if self.config['speed'] == 0.5:
                #this was that "slowdown code" i mentioned earlier.
                #a value, spc_c is risen and only when it is high enough will it advance a frame.
                if self.spd_c >= 2: self.spd_c=0; self.curFrame+=1
                else: self.spd_c+=1
            elif self.config['speed']==2:
                self.curFrame+=2
            else:self.curFrame+=1
            # SCROLL CODE & DECOY SCROLL CODE
            self.bgY += self.config['scrollVert']
            self.bgX += self.config['scrollHoriz']
            if self.bgY >= 800 or self.bgY <= -800: self.bgY=0
            if self.bgX >= 600 or self.bgX <= -600: self.bgX=0

            #RESETTING THE FRAME
            if self.curFrame>=len(self.dir):self.curFrame=0
            
            #WHAT IS DECOY CODE?
            #Basically, if an image is scrolling, there will always be a part of the screen with no background occupying it.
            #So, to solve this issue, there is a "decoy bg" placed above and below the background to prevent the issue. 

        # ALTERNATIVE
        else:
            self.curFrame+=1


    #Displaying the bg is treated differently due to fps changes in playstate
    def display_bg(self):
        self.WIN.blit(self.dir[self.curFrame],(self.bgX,self.bgY))
        if self.config != None: self.decoys() 

"""FORMATION FOR GAMEPLAY--------------------"""
class Formation():
    def __init__(self, allsprites, enemies, bullets, player, file=None,level=1):

        #note to self, the player class is used, not the sprite group.
        """
        FILE is the piece of code used that holds all the python data.
            the world file is a text file that holds all the setting data
            and the world data file is a python file that holds things such as intensity and formation
        FILE also holds all the imports needed to spawn characters needed for a file
        """
        # print("formation created")
        self.pos=[0,0]
        self.finished=False
        self.dirH=['l','r'];self.dirH=self.dirH[random.randint(0,1)] #potential [l/r]: randomized
        self.totalchar=0 #this is the highest amount of characters onscreen. it will create a ratio based off of how many characters are still alive to create a speed
        self.timePassed=False #this is for the exit animation if too much time has passed
        self.exitSpeed=10 #this is the speed in which the formation exits
        self.bullets=bullets #bullet classes
        self.file=file #the piece of code used that holds all the python data
        self.imports={}  # self.imports is the actual imported character files
        self.activeformation = {}  # the actual character objects; NOT file.formation, which is just a class list
        self.curFrame=0 #count for when to send down a formations
        """importing everything in file.imports"""
        if self.file.imports != None:
            for item in self.file.imports:
                the_code = "import modules.characters." + str(item) + " as " + str(item)
                exec(the_code, globals(), self.imports)
        """running the methods that change the formation class"""
        if level == 1: self.file.lvl1()
        elif level==2:self.file.lvl2()
        elif level==3:self.file.lvl3()
        elif level==4:self.file.lvl4()
        else:pass
        howmanychar=0 #howmanychar is a counter that checks how many characters are there, that's it, and its mostly for debug purposes
        size=[0,len(self.file.formation)] # size is the offset made by how large the file is. It will always use this for positioning and bouncing.
        for i in range(len(self.file.formation)):
            if len(self.file.formation[i])>size[0]:
                size[0]=len(self.file.formation[i]) #calculates the width of the formation, appended to SIZE
        self.pos = [(random.randint(50, (600 - (size[0] * self.file.char_distance_x)))),75]  # randomly generating start position

        #CODE FOR SPAWNING CHARACTERS
        for i in range(len(self.file.formation)):
            for j in range(len(self.file.formation[i])):
                """
                HOW ADDING WORKS
                activeformation contains every character's active sprite file and all that sorta stuff, so, instead of a text file just saying the character name, this holds the exact object for pygame
                it is stored in a dictionary, so each is considered a different variable. I am only doing this as a makeshift sprite class due to the fact that these formation enemies are the only ones that need values fed to them.
                The index is (howmanychar) which is how many characters have been put in the formation overall. It starts at zero, but goes up for every character added.
                The blob of code in self.imports[] is the name of the character used within the formation code. So, if it's 'nope' or 'zapp' or 'piranha' it will spawn said character. This is the importance of the imports variable, because the program will crash if the character is not imported.
                """
                try:
                    self.activeformation[howmanychar] = self.imports[self.file.formation[i][j]].Char(allsprites=allsprites, bullets=bullets, player=player,enemies=enemies,formationPos=self.pos, offset=((j*self.file.char_distance_x),(i*self.file.char_distance_y)))
                    allsprites.add(self.activeformation[howmanychar]);enemies.add(self.activeformation[howmanychar])
                    howmanychar+=1
                except KeyError: pass
        self.totalchar=len(self.activeformation) #max character amount
        self.size=size

        self.start=time.time() #this is the start timer. the more time passes, the faster the game goes
        self.speed=0 #speedup/slowdown code
    def update(self):
        """
        This line of code below me runs the function "formationUpdate" for every item in the formation
        This is, if not stated before, because every asset in the game is already "updated" through the pygame sprite class feature
        So this function updates the formation position in the code
        """
        for key,value in self.activeformation.items():value.formationUpdate(self.pos)
        """KILL CODE for if too much TIME has PASSED"""
        if self.timePassed:
            self.exit()
            return #overrides everything else
        """MOVEMENT code for updating CHARACTER POSITIONS"""
        self.formMove()
        """THROWDOWN code for making CHARACTERS ATTACK"""
        self.throwDown()
        """
        The piece of code below this is for removing any dead items from the formation dictionary.
        This is for telling when to move on in the level, to make another formation.
        This COULD be done with a sprite class, but it is just easier and more understandable this way. 
        """
        for key, value in self.activeformation.items():
            if value.state == "dead": self.activeformation.pop(key);break
        if len(self.activeformation)==0: self.finished=True
        if self.file.time!=None: self.timer()

    def attack(self):
        """NEW ATTACK CODE IDEA
        make a list of indexes of characters that are in idle state 
        randomly generate an index and set the character of that index to attack state
        """
        idle_list=[]
        for key in self.activeformation.keys():
            if self.activeformation[key].state=="idle":
                idle_list.append(key)
        if len(idle_list)>0:self.activeformation[idle_list[random.randint(0,(len(idle_list)-1))]].state="attack";return
    def formMove(self):
        if self.pos[0]>=(600-(self.size[0]*self.file.char_distance_x)): self.speed-=self.file.speed*0.025 ;self.dirH='l'
        elif self.pos[0]<=100: self.speed+=self.file.speed*0.025;self.dirH='r'
        else:
            if self.dirH=='l': self.speed=self.speed = self.file.speed*-1
            elif self.dirH == 'r': self.speed = self.speed = self.file.speed
        self.pos[0]+=self.speed
        self.pos[1]=math.sin(self.pos[0]/10)*10 + 100
    def timer(self):
        end=time.time()
        self.clk=(self.file.time-(end-self.start))
        if end-self.start>=self.file.time:self.timePassed=True
        else:pass
            # print(end-self.start)
    def throwDown(self):
        """
        waits for a randomly-calculated time to pass, before making a character attack you
        every frame it will make a random calculation and, if the calculation is correct, it makes a character attack
        this makes the game unpredictable and a unique playthrough every time
        the calculations done are based off the 'spawn time' value given
            the higher the spawn time value, the more likely the character is to attack you
        there is also a 'maxChar' value given that stops characters from attacking if too many are up
            if the value is set to None, there is no maximum
            it constantly checks to make sure the value is below maxChar, by fetching a value of how many characters are in 'attack' mode
        """
        self.curFrame+=1;totalCharAtk=0
        for item in self.activeformation.values():
            if item.state=="attack":totalCharAtk+=1 #tallying how many characters are in the attack state
        # print(totalCharAtk)
        if (totalCharAtk<self.file.maxChar) and (self.curFrame>=(self.file.spawn_time)):#only makes an item attack if there are less characters attacking than the limit, and the timer has been tripped
            self.attack()
            self.curFrame=0
            # print("eligible")
        else:
            pass
            # print("ineligible")


    def exit(self):
        self.exitSpeed-=1
        self.pos[1]+=self.exitSpeed
        if self.dirH.lower()=='r':self.pos[0]+=self.speed/2
        elif self.dirH.lower()=='l':self.pos[0]-=self.speed/2
        if self.pos[1]<=-1000:
            # print(self.pos[1])
            #killing each individual item in the formation
            while len(self.activeformation)>0:
                for key,value in self.activeformation.items():
                    value.state="dead";value.kill()
                    if value.state == "dead":self.activeformation.pop(key);break
            self.finished=True


"""LEVEL ASSET CODE--------------------"""
class Level():
    """
    -PSEUDOCODE

    --START
    FileReader checks the world order.
    FileReader compiles a dictionary for how the level order should go, and writes it to a temporary file.
    FileReader will then check what level number you are on in the save file and it will open the data from the "worlds" folder
    FileReader, using the "worlds" data, will then load several things:
        -background data
        -OST data
        -UI data
        -character formations (from the "worldData" folder)
        
    --UPDATE
    FileReader updates the background (updates the frame):
        It will always do this, even if there is one frame.
        The folder is the name of the background, and each frame is simply "frame[x]"
            So, if there is only a frame 1, it will repeatedly loop back to frame 1
    FileReader updates the music:
        It just checks to see if the music has ended or not and replays it.
        It will also check for a custom command to stop the music.
    FileReader updates the formation (read next section)

    --FORMATION STATES- -- MOVED TO "FORMATION"
    ---FORMING
    The formation position is (TOP-CENTER STAGE) 300,200
    In the order in which the characters are listed, the characters in the formation will zoom onscreen.
        They will either zoom from the left, right, or top.
    This state ends when all characters are onscreen.
    ---ATTACK/IDLE
    The formation position will bounce from side to side.
        It probably only moves around 10 pixels to each side before changing directions.
    As it does this, it will randomly select a character from the formation to send off to attack the player.
        The rate in which they are sent off is most likely an INTENSITY VALUE and RANDOM CHANCE
    ---FORMATION ENDED / TIME OUT
    Each worldData file can contain a time limit value.
        When this time limit is hit, the formation will rise offscreen and will go to the next level.
    However, if you finish off the formation, you will get a bonus.
        There will be a slight fanfare thingy and then you will move onto the next level.
    When a world finishes and moves on, it pretty much keeps everything the same but loads the next level in the worldData file.

    --WORLD TRANSFER
    When a world is over, it simply raises the level counter in the save file and resets itself to load that file.
    The cycle then repeats, from the very top.

    """
    def __init__(self,WIN,allsprites,enemies,bullets,player):

        self.allsprites,self.enemies,self.bullets,self.player,self.level=allsprites, enemies, bullets, player,1
        #WORLD is the WORLD FILE read, LEVEL is the LEVEL IN THE WORLD, imported_world_file is the imported world file

        #figuring out the level
        with open("./assets/tempsave.txt","r") as data:self.world=eval(data.read())["CurrentLevel"]
        with open("./leveldata/worldOrder.txt","r") as data:self.worldName= eval(data.read())[self.world]
        # print(str(self.world) +"|"+ str(self.worldName))
        #opening stage data text file
        with open(("./leveldata/worlds/" + self.worldName + ".txt"),"r") as data: self.worldInfo=eval(data.read())
        # print(self.worldInfo)
        #importing the actual stage data module
        the_code = "import leveldata.worldData." + self.worldInfo['filename'] + " as imported_world_file"
        worldData={}
        exec(the_code,globals(),worldData)
        self.lvl=worldData['imported_world_file'];del worldData #lvl is the world data, level is the number for level, sorry for the confusion
        self.lvl=self.lvl.data()
        # except:print("IMPORT ERROR")

        #loading the music
        sounds.play_song(str(self.worldInfo['songname']))
        #loading the background
        self.bg=BG(WIN, self.worldInfo['bg'])
        # self.bg=BG(WIN,'null')
        """fileReader will then pass off the worldData file to 'formation', as well as the current level"""
        self.form=Formation(self.allsprites, self.enemies, self.bullets, self.player, file=self.lvl, level=self.level) #takes allsprites to handle spawning enemies, enemies to do the same, and bullets to give to the enemies to register hit detectiona

        self.world_ended=False

    def update(self):
        try: #this is a try statement because there will be no form to check later
            self.form.update()  # updates the formation
            if self.form.finished:
                """This is the reset code. It deletes self.form, raises the level by 1, and then re-makes self.form"""
                del self.form
                self.level+=1
                # print("LEVEL IS NOW " + str(self.level))
                self.form = Formation(self.allsprites, self.enemies, self.bullets, self.player, file=self.lvl, level=self.level)
        except AttributeError: pass

        
"""STATES###############################################################"""
"""TITLE ASSETS--------------------"""
def title(WIN=WIN,sounds=sounds,ui=ui):
    # try:
    #IMAGE LOADING, FIRST AND FOREMOST
    #these are not preloaded because they are only needed like once

    run = True

    FPS = 15 #TEST ENABLE
    clock = pygame.time.Clock()
    start = time.time()
    frame = 0
    lockoutenter = False

    index = 1

    #GETS DA SOUNDS TO PLAY
    sounds.play_song('title.mp3')

    #REDRAW_WINDOW IS ONLY FOR GRAPHICS. NO SOUND EFFECTS OR SPRITES.
    #redraw_window will show and hide sprites depending on what menu you're in and what index you have selected
    def redraw_window(index,frame,ui):
        #The main thing that plays in the title screen. The bg, the fizz effect, and the logo.
        WIN.blit(ui.titlebg1, (0,0))
        WIN.blit(ui.titlebglogo[frame], (0,0))

        #"START," "OPTIONS," and "QUIT" only appear during the first part of the title menu
        if index == 1: WIN.blit(ui.START[1],(200,350))
        else: WIN.blit(ui.START[0],(200,350))
        if index == 2: WIN.blit(ui.OPTIONS[1],(200,450))
        else: WIN.blit(ui.OPTIONS[0],(200,450))
        if index == 3: WIN.blit(ui.QUIT[1],(200,550))
        else: WIN.blit(ui.QUIT[0],(200,550))

        pygame.display.update() #TEST ENABLE


    while run:
        # timer code for the yup and logo frames
        end = time.time()
        if end - start >= 0.1:
            start = time.time()
            frame += 1
            if frame > 2: frame = 0

        #tells the clock to tick at the rate of FPS
        clock.tick(FPS)
        print(clock.get_fps()) #TEST ENABLE

        #once it sets all of the current image forms, it will then redraw the window
        redraw_window(index,frame)

        for event in pygame.event.get():

            #Code to end the game if conditions are met.
            if event == pygame.QUIT:
                run = False
                exit()


            #Code that checks for if a key is pressed.
            if event.type == pygame.KEYDOWN:

                #This code checks for an enter press.
                #It will always lock out the enter button if it is being held down. It waits until enter is released to register again.
                if event.key == pygame.K_SPACE:
                    if lockoutenter == False:
                        sounds.select.play()
                        #if you picked the first option, start, the program will set menudepth to 3 and begin the game
                        if index == 1: sounds.stop_song(); return "start"
                        #If you picked options, it will open the options menu
                        elif index == 2: sounds.stop_song(); return "options"
                        # If you pick quit, or something else by some chance, the game will quit.
                        else:sounds.select.play();time.sleep(0.5);run = False;exit()

                #Escape press for quitting game
                if event.key == pygame.K_ESCAPE:
                    sounds.back.play()
                    exit()

                #Item selection; changes index
                if event.key == pygame.K_UP:
                    if index > 1: index -=1
                    sounds.scroll.play()
                if event.key == pygame.K_DOWN:
                    if index < 3: index +=1
                    sounds.scroll.play()

            #Code that checks for a key to be released
            if event.type == pygame.KEYUP:
                #This is what unlocks the enter button
                if event.key == pygame.K_SPACE:
                    lockoutenter = False

"""OPTIONS ASSETS--------------------"""
def options(WIN=WIN,ui=ui):
    def render_text(text):
        font = pygame.font.Font("./assets/font/Setfont-Regular.ttf", 50)
        surface = pygame.transform.scale(font.render(str(text), True, "white"), (75, 40))

        return surface

    settings = {}
    curSong = sounds.play_nonmain_song("pause.mp3")

    # Reads a dictionary, with the index name and the values associated with it
    with open("./assets/settings.txt", "r") as data:
        settings = eval(data.read())
    settings_keys_images = {}

    # Compiling a dictionary of rendered text to be displayed for the items
    for key in settings.keys(): settings_keys_images[key] = render_text(str(key))

    # UI settings
    run = True
    index = 0

    def redraw_window(settings=settings, settings_keys_images=settings_keys_images, index=index,ui=ui):
        # filling the bg and showing the title
        WIN.blit(ui.optionbg, (0, 0))
        # displaying the setting names
        yval = 0
        for value in settings_keys_images.values():
            WIN.blit(value, (50, (yval * 50) + 200))
            yval += 1
        # displaying the setting values
        yval = 0
        for value in settings.values():
            if value[1] == "onoff" and value[0]:
                WIN.blit(ui.yes, (150, ((yval * 50) + 200)))
            elif value[1] == "onoff" and not value[0]:
                WIN.blit(ui.no, (150, ((yval * 50) + 200)))
            elif value[1] == "3060" and value[0]:
                WIN.blit(ui.option_60, (150, ((yval * 50) + 200)))
            elif value[1] == "3060" and not value[0]:
                WIN.blit(ui.option_30, (150, ((yval * 50) + 200)))
            elif value[1] == "slider":
                WIN.blit(ui.slider, (150, ((yval * 50) + 200)))
                WIN.blit(ui.knob, ((130 + (value[0] * 175)), ((yval * 50) + 200)))
            yval += 1
        # displaying the cursor
        WIN.blit(ui.cursor, (0, ((index * 50) + 200)))
        # self-explanatory: updating the display
        pygame.display.update() #TEST ENABLE
    redraw_window()

    clock=pygame.time.Clock()

    while run:
        clock.tick(9999999) #TEST ENABLE
        print(clock.get_fps()) #TEST ENABLE

        # HARD-CODING PART FOR MUTE CODE. ERASE IF RE-USED.
        if settings["MUTE"][0]:
            settings["OST VOL"][0] = 0.0
            settings["SOUND VOL"][0] = 0.0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    sounds.back.play()
                    # writing the settings
                    with open("./assets/settings.txt", "w+") as data: data.write(str(settings))
                    curSong.stop()
                    return "title"

                if event.key == pygame.K_DOWN and index < (len(settings) - 1):
                    sounds.scroll.play()
                    index += 1
                    # print(index)
                if event.key == pygame.K_UP and index > 0:
                    sounds.scroll.play()
                    index -= 1
                    # print(index)
                if event.key == pygame.K_SPACE:
                    sounds.select.play()
                    # list(settings)[index] is the key name
                    keyindex = list(settings)[index]
                    if settings[keyindex][1] == "onoff":
                        if settings[keyindex][0] == False:
                            settings[keyindex][0] = True
                        elif settings[keyindex][0] == True:
                            settings[keyindex][0] = False
                    elif settings[list(settings)[index]][1] == "3060":
                        if settings[keyindex][0] == False:
                            settings[keyindex][0] = True
                        elif settings[keyindex][0] == True:
                            settings[keyindex][0] = False
                    else:
                        sounds.denied.play()
                if event.key == pygame.K_LEFT:
                    sounds.select.play()
                    # list(settings)[index] is the key name
                    keyindex = list(settings)[index]
                    if settings[keyindex][1] == "slider" and settings[keyindex][0] > 0:
                        settings[keyindex][0] -= 0.05
                        settings[keyindex][0] = round(settings[keyindex][0], 2)
                    else:
                        sounds.denied.play()
                    # print(values[index])
                if event.key == pygame.K_RIGHT:
                    sounds.select.play()
                    # list(settings)[index] is the key name
                    keyindex = list(settings)[index]

                    # HARD-CODING PART FOR MUTE CODE. ERASE IF RE-USED.
                    if keyindex == "OST VOL" or keyindex == "SOUND VOL": settings["MUTE"][0] = False

                    # applying settings
                    if settings[keyindex][1] == "slider" and settings[keyindex][0] < 1:
                        settings[keyindex][0] += 0.05
                        settings[keyindex][0] = round(settings[keyindex][0], 2)
                    else:
                        sounds.denied.play()

                if event.key == pygame.K_p:
                    readapply(settings, curSong)
                #only redraws the window when a setting is changed. No FPS needed.    
                redraw_window(index=index)          

"""PAUSE ASSETS--------------------"""
def pause(WIN=WIN, img=None, ui=ui): #it takes in the UI images as an argument to lower RAM usage and prevent leakage :)
    """-----PLEASE NOTE !-----
    pausestate is required to work like a unique MAIN function, seeing that it is a state within a state
    (By "state within a state", I mean that playstate runs pausestate, so pausestate is completely isolated from everything else)
    (On top of that, pausestate has to run separate states in ways that do not affect the original state (playstate), so it has to be specific with the way that it runs states, as well)
    this is why pausestate imports optionstate and runs it separately without requiring MAIN
    """

    curSong=sounds.play_nonmain_song('pause.mp3')


    #sets the values
    FPS=60;run=True;clock = pygame.time.Clock();index = 1
    pauseStart = time.time();graphicStart = time.time()
    graphicFrame = 1
    sounds.select2.play()

    #updates every graphic onscreen
    def dispUpdate(graphicFrame,index,img,ui=ui):
        if img==None:WIN.fill("black")
        else:WIN.blit(img,(0,0))

        WIN.blit(ui.pause[graphicFrame],((300-(ui.pause[graphicFrame].get_width()/2)),100))

        if index == 1: WIN.blit(ui.CONTINUE[1],((300-(ui.CONTINUE[1].get_width()/2)),350))
        else: WIN.blit(ui.CONTINUE[0],((300-(ui.CONTINUE[0].get_width()/2)),350))
        if index == 2: WIN.blit(ui.OPTIONS[1],((300-(ui.OPTIONS[1].get_width()/2)),450))
        else: WIN.blit(ui.OPTIONS[0],((300-(ui.OPTIONS[0].get_width()/2)),450))
        if index == 3: WIN.blit(ui.QUIT[1],((300-(ui.QUIT[1].get_width()/2)),550))
        else: WIN.blit(ui.QUIT[0],((300-(ui.QUIT[0].get_width()/2)),550))
        pygame.display.update()

    while run:
        #sets time values and raises graphic frames according to them
        end = time.time()
        timePassed = end-pauseStart
        graphicTime = end-graphicStart
        if graphicTime >= 0.25 and graphicFrame < 2: graphicFrame += 1;graphicStart=time.time()
        elif graphicTime >= 0.25  and graphicFrame >= 2: graphicFrame = 1; graphicStart = time.time()
        else: pass

        dispUpdate(graphicFrame,index,img)
        clock.tick(FPS)

        for event in pygame.event.get():

            if event == pygame.QUIT:
                sounds.stop_song()
                sounds.select2.play()
                run = False
                return timePassed
            if event.type == pygame.KEYDOWN:

                #UI
                if event.key == pygame.K_UP:
                    if index > 1: index -= 1
                    sounds.scroll.play()
                if event.key == pygame.K_DOWN:
                    if index < 3: index += 1
                    sounds.scroll.play()
                if event.key == pygame.K_SPACE:
                    sounds.select2.play()
                    if index == 1:
                        curSong.stop()
                        run = False
                        return timePassed
                    if index == 2:
                        curSong.stop()
                        options()
                        curSong.play()
                    if index == 3:
                        curSong.stop()
                        return "title"

    curSong.stop();del curSong
    return timePassed

"""GAMEPLAY ASSETS--------------------"""
def play(allsprites=allsprites, playersprite=playersprite, bullets=bullets, enemies=enemies, WIN=WIN, settings=None, controller=None):
    # DEALING WITH SETTINGS:
    if settings == None:
        settings = readapply()

    # CREATING THE PLAYER AND LEVEL INSTANCE DEPENDING ON TEMPSAVE VALUES -PLAYREMOVE
    player = playerguy.Player(enemies, bullets, allsprites, sounds)  # Defines the player
    allsprites.add(player)
    playersprite.add(player)
    with open("./assets/tempsave.txt", "r+") as data:
        readData = data.read()
        readData = eval(readData)
        if readData["NewGame?"]:
            if not readData["LevelSelect?"]:
                level = 1
            else:
                level = readData["CurrentLevel"]
        elif not readData["NewGame?"]:
            player.load_data(readData["PlayerInstance"]) #-PLAYREMOVE
            level = readData["CurrentLevel"]
        else:
            level = 0

    if settings["FPS"][0]==False:
        optimLoop=2
        FPS=30
    else:
        optimLoop = 1
        FPS = 999999 #TEST ENABLE

    graphical=True #this is for debug purposes, where if you turn it off, the display turns off but the framerate rises heavily

    def exit_playstate(player, level, state_list=[enemies, bullets, playersprite, allsprites]):
        with open("./assets/tempsave.txt", "w") as data:
            try:
                if newDict["PlayerInstance"] == None:
                    newDict = {"NewGame?": True, "LevelSelect?": False, "CurrentLevel": 1, "PlayerInstance": None}
                    data.write(str(newDict))
                    # print("data overwritten: player died")
                else:
                    newDict = {"NewGame?": False, "LevelSelect?": False, "CurrentLevel": level,
                               "PlayerInstance": player.pack_data()}
                    data.write(str(newDict))
            except:
                if player == None:
                    newDict = {"NewGame?": True, "LevelSelect?": False, "CurrentLevel": 1, "PlayerInstance": None}
                    data.write(str(newDict))
                    # print("data overwritten: player died")
                else:
                    newDict = {"NewGame?": False, "LevelSelect?": False, "CurrentLevel": level,
                               "PlayerInstance": player.pack_data()}
                    data.write(str(newDict))
        for item in state_list:
            item.empty()
        global run
        run = False

    def redraw_window(graphical):
        bg.display_bg() 
        allsprites.draw(WIN)
        # UI -PLAYREMOVE
        display_bullet(WIN, (0, 0), player.currentweapon) #-PLAYREMOVE
        player.display_health(WIN, (30, 0)) #-PLAYREMOVE
        display_score(player.score, (600, 0), WIN) #-PLAYREMOVE

        # DEBUG 
        debug_displays(allsprites,
                       {"PLAYER": playersprite, "ENEMIES": enemies, "BULLETS": bullets},
                       {"PLAYSTATE": dir(), "PLAYER": dir(playerguy),
                        "FILEREADER": dir(Level), "PYGAME": dir(pygame)},
                       (time.time() - start_time),
                       clock.get_fps(),
                       WIN=None)

        # playersprite.draw(WIN) #-PLAYREMOVE

        # FINISHING WITH AN UPDATE STATEMENT
        if graphical:pygame.display.update() #TEST ENABLE

    def update_sprites():
        allsprites.update()
        bg.update() 

    # VARIABLE DEFINITIONS WHEN THE CODE BEGINS.
    run = True  # Variable that tells the game to loop
    clock = pygame.time.Clock()  # The clock is essentially just a thing that tells the computer to update the screen after a set period of time.
    # LEVEL INITIALIZATION
    levelclass = Level(WIN, allsprites, enemies, bullets, player=player) #-PLAYREMOVE 
    bg = levelclass.bg 


    # VIRTUAL BUTTON CODE
    # spawn_controller(allsprites)
    start_time = time.time()

    while run:


        #TEST PURPOSES: DO NOT LEAVE ENABLED
        player.autoshoot()

        clock.tick(FPS)

        for i in range(optimLoop): update_sprites()
        if player.playerdied: exit_playstate(player, level);return "title"  # player game over state initialization -PLAYREMOVE
        # graphical updates
        redraw_window(graphical)
        levelclass.update() 
        # inputs
        for event in pygame.event.get():

            # QUIT GAME CODE
            if event.type == pygame.QUIT:
                run = False
                exit()
            # PAUSE CODE
            if event.type == pygame.KEYDOWN:
                # pause code
                if event.key == pygame.K_ESCAPE:
                    # freezes everything and opens PAUSESTATE
                    player.reset_movement() #-PLAYREMOVE
                    pygame.mixer.music.pause()
                    timePaused =  pause(img=bg.dir[0])
                    # If an error occurs, or any exit code is brought up, it spits you back at the title
                    if type(timePaused) != float:
                        exit_playstate(None, 1, [enemies, bullets, playersprite, allsprites])
                        return "title"  # Sends the character into "titlestate", removing every single bit of progress made.
                    pygame.mixer.music.unpause()
            # PLAYER CONTROLS
            player.controls(event) #-PLAYREMOVE
            # DEBUG CODE
            if event.type == pygame.KEYDOWN:
                #swaps the graphical setting
                if event.key==pygame.K_1:
                    if graphical:graphical=False
                    else:graphical=True
            #     if event.key == pygame.K_o:
            #         levelclass.form.attack()


exit_commands=["exit","quit","leave","abort","depart"]
while True:
    cmd=input("COMMAND:")
    if cmd.lower() in exit_commands:break
    exec(cmd)
exit()



"MAIN LOOP###############################################################"
next_state = "title"
while True:
    #ADJUSTS THE VOLUME EVERY SINGLE TIME A STATE CHANGES
    shortLoad()
    settings = readapply()

    if type(next_state) == str:

        if next_state == "start":
            LongLoad()
            next_state = play()
            # shortLoad()
            continue

        elif next_state == "title":
            next_state = title()
            continue

        elif next_state == "options":
            # next_state = errorstate.error(WIN, "unknown")
            next_state = options()
            continue

        else:exit()

    elif next_state == None:
        shortLoad(WIN)
        exit()

    else:
        print("invalid state entry")
        exit()

 
